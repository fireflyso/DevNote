# -- coding: utf-8 --
# @Time : 2023/7/21 21:19
# @Author : xulu.liu
import os
from clickhouse_driver import Client
import utils_logger
import xlwt
import pymysql

os.system("rm -rf flow.xls")


def set_style(name, height, bold=False):
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = name
    font.bold = bold
    font.color_index = 4
    font.height = height
    style.font = font
    return style


f = xlwt.Workbook()
sheet = f.add_sheet('flow data', cell_overwrite_ok=True)
row0 = ["pipe", "削峰数量", "削峰总带宽(M)", "最大削峰带宽(M)", "限速带宽(M)", "客户id", "客户名称", "节点", "平均超限(M)", "最大超限比例"]
default_style = set_style('Times New Roman', 220, True)
for i in range(0, len(row0)):
    sheet.write(0, i, row0[i], default_style)

db = pymysql.connect(
    host="write-mysql.gic.local",
    user="resop_20210108",
    password="1snzvbhdEOhfW4LArq$5",
    database="cdscp",
    port=6033,
    charset='utf8'
)

cursor = db.cursor()

logger = utils_logger.get_logger('0721', 'INFO')

CK_HOST = "10.13.133.134"
CK_USER = "flowdata"
CK_PASSWORD = "wVen6RK3KpkpGdsA"
CK_DB_ANME = "flow_snmp"
CK_PORT = 9000
client = Client(host=CK_HOST, port=CK_PORT, user=CK_USER, password=CK_PASSWORD)

pipe_list = []
error_pipe = []
with open("temp.out") as file:
    for line in file:
        pipe_list.append(line.replace('\n', ''))

sheet_row = 1


def get_pipe_info(pipe_id):
    sql = "select a.id, a.qos, b.customer_id, b.name, d.name from cloud_pipe a, account_customer b, cloud_app c, cloud_datacenter d where a.id = '{}' and a.customer_id = b.id and a.app_id = c.id and c.site_id = d.id;".format(
        pipe_id)
    _ = cursor.execute(sql)
    res = cursor.fetchall()
    if not len(res):
        sql = "select a.id, a.qos, c.customer_id, c.name, b.name from cloud_os_bandwidth a, cloud_datacenter b, account_customer c where a.id = '{}' and a.available_zone_id = b.id and a.customer_id = c.id;".format(
            pipe_id)
        _ = cursor.execute(sql)
        res = cursor.fetchall()

    if not len(res):
        sql = "select a.id, a.qos, c.customer_id, c.name, b.name from cloud_pop a, cloud_datacenter b, account_customer c where a.id = '{}' and a.site_id = b.id and a.customer_id = c.id;".format(
            pipe_id)
        _ = cursor.execute(sql)
        res = cursor.fetchall()
    qos = res[0][1]
    customer_id = res[0][2]
    customer_name = res[0][3]
    site_name = res[0][4]

    return qos, customer_id, customer_name, site_name


execpt_data = []
# pipe_list = ['c023aa0a-3fc5-11ed-bdf5-8ae2e7dbd103']
total_pipe_count = len(pipe_list)
check_count = 0
for pipe_id in pipe_list:
    check_count += 1
    try:
        qos, customer_id, customer_name, site_name = get_pipe_info(pipe_id)
        logger.info('开始处理 : {} qos : {}'.format(pipe_id, qos))
        sql = "select in_flow, out_flow, in_bps, out_bps, time from flow_snmp.flow_data WHERE  time >= '2022-07-21 00:00:00' and time <= '2023-07-21 00:00:00' and pipe_id = '{}' order by time;".format(
            pipe_id)
        res = client.execute(sql)
        temp_in_flow = res[0][0]
        temp_out_flow = res[0][1]
        over_count = 0
        total_over_in = 0
        total_over_out = 0
        max_over = 0
        temp_r = 0
        max_over_last = 0
        max_over_now = 0
        max_over_next = 0
        flow_index = -1
        for r in res:
            flow_index += 1
            in_flow = r[0]
            out_flow = r[1]
            in_bps = r[2]
            out_bps = r[3]
            now_in_bps = int((in_flow - temp_in_flow) / 300 * 8)
            now_out_bps = int((out_flow - temp_out_flow) / 300 * 8)
            be_in = int((in_flow - temp_in_flow) / 300 * 8) - in_bps
            be_out = int((out_flow - temp_out_flow) / 300 * 8) - out_bps
            if temp_in_flow == 0 or temp_out_flow == 0:
                temp_in_flow = in_flow
                temp_out_flow = out_flow
                continue
            if in_bps == 0 and out_bps == 0:
                temp_in_flow = in_flow
                temp_out_flow = out_flow
                continue

            if be_in > qos or be_out > qos or be_in > 1000:
                if 2 < flow_index < len(res) - 2:
                    last_two = res[flow_index - 2]
                    last_two_in = last_two[0]
                    last_two_out = last_two[1]
                    last_one_in_bps = int((temp_in_flow - last_two_in) / 300 * 8)
                    last_one_out_bps = int((temp_out_flow - last_two_out) / 300 * 8)

                    next_one = res[flow_index + 1]
                    next_one_in = next_one[0]
                    next_one_out = next_one[1]
                    next_one_in_bps = int((next_one_in - in_flow) / 300 * 8)
                    next_one_out_bps = int((next_one_out - out_flow) / 300 * 8)

                    _temp_in_bps = last_one_in_bps if last_one_in_bps > next_one_in_bps else next_one_in_bps
                    _temp_out_bps = last_one_out_bps if last_one_out_bps > next_one_out_bps else next_one_out_bps
                    if (_temp_in_bps > 0 and now_in_bps > _temp_in_bps * 100) or (_temp_out_bps > 0 and now_out_bps > _temp_out_bps * 100):
                        temp_in_flow = in_flow
                        temp_out_flow = out_flow
                        continue

            if be_in > 0 or be_out > 0:
                over_count += 1
                total_over_in += be_in if be_in > 0 else 0
                total_over_out += be_out if be_out > 0 else 0
                if be_in > max_over or be_out > max_over:
                    max_over_now = r
                    max_over_last = temp_r
                max_over = max_over if max_over > be_in else be_in
                max_over = max_over if max_over > be_out else be_out
                # print(temp_r)
                # print(r)
                # print(res[flow_index + 1])
                # print('be in {} be out {} total {}'.format(be_in, be_out, total_over_in, total_over_out))
                # print()

            temp_in_flow = in_flow
            temp_out_flow = out_flow
            temp_r = r

        total_over = total_over_in if total_over_in > total_over_out else total_over_out
        total_over = int(total_over / 1024 / 1024)
        max_over = int(max_over / 1024 / 1024)
        if over_count > 0 and total_over > 0:
            logger.info('处理进度 : {}/{} - {} , {} 个计量点\n'.format(check_count, total_pipe_count, pipe_id, len(res)))
            logger.error('{}, {}, {}, {}'.format(pipe_id, over_count, total_over, max_over))
            avg_over = int(total_over / over_count)
            if qos:
                max_over_rate = int(max_over / int(qos))
            else:
                max_over_rate = ''
            sheet.write(sheet_row, 0, pipe_id, default_style)
            sheet.write(sheet_row, 1, over_count, default_style)
            sheet.write(sheet_row, 2, total_over, default_style)
            sheet.write(sheet_row, 3, max_over, default_style)
            sheet.write(sheet_row, 4, qos, default_style)
            sheet.write(sheet_row, 5, customer_id, default_style)
            sheet.write(sheet_row, 6, customer_name, default_style)
            sheet.write(sheet_row, 7, site_name, default_style)
            sheet.write(sheet_row, 8, avg_over, default_style)
            sheet.write(sheet_row, 9, max_over_rate, default_style)
            sheet_row += 1
        # print(max_over_last)
        # print(max_over_now)
    except Exception as e:
        error_pipe.append(pipe_id)
        # logger.warn('{} 数据处理异常 : {}'.format(pipe_id, e))
        logger.exception(e)
f.save('flow.xls')
cursor.close()

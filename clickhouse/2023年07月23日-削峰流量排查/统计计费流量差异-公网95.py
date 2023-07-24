# -- coding: utf-8 --
# @Time : 2023/7/23 12:18
# @Author : xulu.liu
import os
from clickhouse_driver import Client
import utils_logger
import xlwt
import pymysql
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from collections import defaultdict

logger = utils_logger.get_logger('flow', 'INFO')


def get_pipe_list():
    pipe_list = []
    with open("public_pipe.out") as file:
        for line in file:
            pipe_list.append(line.replace('\n', ''))
    return pipe_list


def get_old_flow(res):
    start_time = datetime.strptime('2022-07-01 00:00:00', '%Y-%m-%d %H:%M:%S')
    month_flow_dict = {}
    for r in res:
        flow_time = r[0]
        time_str = "{}{}".format(flow_time.year, flow_time.month)
        month_flow_dict.setdefault(time_str, []).append(r)

    month_95_info = {}
    for _ in range(12):
        time_str = "{}{}".format(start_time.year, start_time.month)
        flow_list = month_flow_dict.get(time_str, [])
        if not flow_list:
            start_time += relativedelta(months=1)
            continue

        num = len(flow_list)
        flow_list = [{"time": r[0], 'in_bps': r[1], 'out_bps': r[2]} for r in flow_list]

        index = int(num * 5 / 100)
        res_sort = sorted(flow_list, key=lambda e: e.__getitem__('out_bps'), reverse=True)
        out_bps = res_sort[index]['out_bps']

        res_sort = sorted(flow_list, key=lambda e: e.__getitem__('in_bps'), reverse=True)
        in_bps = res_sort[index]['in_bps']

        value = out_bps if out_bps >= in_bps else in_bps
        month_95_info[start_time] = round(value / 1024 / 1024, 2)
        start_time += relativedelta(months=1)


    return month_95_info


def get_next_five_max_value(real_flow_list, index):
    max_in = 0
    max_out = 0
    for flow_info in real_flow_list[index + 1: index + 5]:
        max_in = max_in if max_in > flow_info.get('in_bps') else flow_info.get('in_bps')
        max_out = max_out if max_out > flow_info.get('out_bps') else flow_info.get('out_bps')

    return max_in, max_out


def get_real_bps(res):
    """
    根据累计值计算出带宽, 并对数据进行核算
    核算规则：
        - 如果一个节点带宽出现过削峰，即和ck里面的bps数值不同
        - 削峰前数值是上一个节点带宽的100倍以上，且同样是后面5个数据节点带宽（削峰前）中最大带宽的100倍以上，则认为次节点数据异常进行丢弃
    注意：根据上面的规则，每个pipe第一个和最后五个数据节点无法进行核算
    """
    last_in_flow = res[0][3]
    last_out_flow = res[0][4]

    # 根据累计值算出bps
    flow_list = []
    for r in res[1:]:
        in_flow = r[3]
        out_flow = r[4]
        in_bps = int((in_flow - last_in_flow) / 300 * 8)
        out_bps = int((out_flow - last_out_flow) / 300 * 8)
        flow_list.append({"time": r[0], 'in_bps': in_bps, 'out_bps': out_bps, 'old_in_bps': r[1], 'old_out_bps': r[2]})
        last_in_flow = in_flow
        last_out_flow = out_flow

    flow_list = sorted(flow_list, key=lambda e: e.__getitem__('time'), reverse=False)

    index = 0
    last_in_bps = flow_list[0].get('in_bps')
    last_out_bps = flow_list[0].get('out_bps')
    # 第一个数据节点不进行校验
    real_flow_list = [flow_list[0]]
    for flow_info in flow_list[1: -5]:
        index += 1
        in_bps = flow_info.get('in_bps')
        out_bps = flow_info.get('out_bps')
        if in_bps != flow_info.get('old_in_bps') and in_bps > last_in_bps * 100:
            next_five_max_in, next_five_max_out = get_next_five_max_value(real_flow_list, index)
            if in_bps > next_five_max_in * 100:
                continue

        if out_bps != flow_info.get('old_out_bps') and out_bps > last_out_bps * 100:
            next_five_max_in, next_five_max_out = get_next_five_max_value(real_flow_list, index)
            if out_bps > next_five_max_out * 100:
                continue

        last_in_bps = in_bps
        last_out_bps = out_bps
        real_flow_list.append(flow_info)

    # 最后五个数据节点不进行校验
    real_flow_list += flow_list[-5:]

    return real_flow_list


def get_real_flow(res):
    start_time = datetime.strptime('2022-07-01 00:00:00', '%Y-%m-%d %H:%M:%S')
    real_flow_list = get_real_bps(res)
    month_flow_dict = {}
    for flow_info in real_flow_list:
        flow_time = flow_info.get('time')
        time_str = "{}{}".format(flow_time.year, flow_time.month)
        month_flow_dict.setdefault(time_str, []).append(flow_info)

    month_95_info = {}
    for _ in range(12):
        time_str = "{}{}".format(start_time.year, start_time.month)
        flow_list = month_flow_dict.get(time_str, [])
        if not flow_list:
            start_time += relativedelta(months=1)
            continue

        num = len(flow_list)

        index = int(num * 5 / 100)
        res_sort = sorted(flow_list, key=lambda e: e.__getitem__('out_bps'), reverse=True)
        out_bps = res_sort[index]['out_bps']

        res_sort = sorted(flow_list, key=lambda e: e.__getitem__('in_bps'), reverse=True)
        in_bps = res_sort[index]['in_bps']

        value = out_bps if out_bps >= in_bps else in_bps
        month_95_info[start_time] = round(value / 1024 / 1024, 2)
        start_time += relativedelta(months=1)

    return month_95_info


def set_style(name, height, bold=False):
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = name
    font.bold = bold
    font.color_index = 4
    font.height = height
    style.font = font
    return style


def init_sheet():
    work_book = xlwt.Workbook()
    sheet = work_book.add_sheet('flow data', cell_overwrite_ok=True)
    row0 = ["pipe", "客户id", "客户名称", "节点", "带宽(M)"]
    start_time = datetime.strptime('2022-07-01 00:00:00', '%Y-%m-%d %H:%M:%S')
    for _ in range(12):
        row0.append(str(start_time).split(' ')[0])
        start_time += relativedelta(months=1)
    row0 += ['总带宽差值(M)']
    default_style = set_style('Times New Roman', 220, True)
    for i in range(0, len(row0)):
        sheet.write(0, i, row0[i], default_style)

    sheet_one = work_book.add_sheet('customer data', cell_overwrite_ok=True)
    sheet_one.write(0, 0, '客户id', default_style)
    sheet_one.write(0, 1, '客户名称', default_style)
    sheet_one.write(0, 2, '累计95带宽差值(M)', default_style)

    return work_book, sheet, sheet_one


def get_db_conn():
    db = pymysql.connect(
        host="write-mysql.gic.local",
        user="resop_20210108",
        password="1snzvbhdEOhfW4LArq$5",
        database="cdscp",
        port=6033,
        charset='utf8'
    )

    return db.cursor()


def get_ck_cilent():
    CK_HOST = "10.13.133.134"
    CK_USER = "flowdata"
    CK_PASSWORD = "wVen6RK3KpkpGdsA"
    CK_PORT = 9000
    client = Client(host=CK_HOST, port=CK_PORT, user=CK_USER, password=CK_PASSWORD)
    return client


def get_pipe_info(pipe_list):
    cursor = get_db_conn()
    sql = "select a.id, a.qos, c.name, d.id, d.name from cloud_pipe a, cloud_app b, cloud_datacenter c, account_customer d where a.app_id = b.id and a.customer_id = d.id and b.site_id = c.id and a.id in {};".format(tuple(pipe_list))
    _ = cursor.execute(sql)
    res = cursor.fetchall()
    pipe_info_dict = {}
    for r in res:
        pipe_info_dict[r[0]] = (r[1], r[2], r[3], r[4])

    cursor.close()
    return pipe_info_dict


if __name__ == '__main__':
    os.system("rm -rf real_flow.xls")
    pipe_list = get_pipe_list()
    total_count = len(pipe_list)
    check_count = 0
    work_book, sheet, sheet_one = init_sheet()
    ck_client = get_ck_cilent()
    pipe_info_dict = get_pipe_info(pipe_list)
    sheet_row = 0
    default_style = set_style('Times New Roman', 220, True)
    customer_flow_dict = defaultdict(int)
    for pipe_id in pipe_list:
        try:
            check_count += 1
            start_time = datetime.strptime('2022-07-01 00:00:00', '%Y-%m-%d %H:%M:%S')
            end_time = datetime.strptime('2023-07-01 00:00:00', '%Y-%m-%d %H:%M:%S')
            query = "SELECT time, in_bps, out_bps, in_flow, out_flow FROM flow_snmp.flow_data where pipe_id  = '{}' " \
                    "and time >= '{}' and time < '{}' order by time".format(pipe_id, start_time, end_time)
            flow_res = ck_client.execute(query)
            if not len(flow_res):
                continue
            old_flow_info = get_old_flow(flow_res)
            real_flow_info = get_real_flow(flow_res)
            # print(old_flow_info)
            # print(real_flow_info)

            sheet_row += 1
            qos, site_name, customer_id, customer_name = pipe_info_dict.get(pipe_id, (0, '', '', ''))
            sheet.write(sheet_row, 0, pipe_id, default_style)
            sheet.write(sheet_row, 1, customer_id, default_style)
            sheet.write(sheet_row, 2, customer_name, default_style)
            sheet.write(sheet_row, 3, site_name, default_style)
            sheet.write(sheet_row, 4, qos, default_style)
            rate_95_value = 0
            line_index = 5
            for _ in range(12):
                old_95 = old_flow_info.get(start_time, 0)
                real_95 = real_flow_info.get(start_time, 0)
                rate_95_value += real_95 - old_95
                sheet.write(sheet_row, line_index, '{}/{}'.format(old_95, real_95), default_style)
                start_time += relativedelta(months=1)
                line_index += 1
            rate_95_value = int(rate_95_value)
            sheet.write(sheet_row, line_index, rate_95_value, default_style)
            customer_flow_dict[(customer_id, customer_name)] += rate_95_value
            logger.info('进度 {}/{} 开始处理 : {}, 95带宽差值 : {}'.format(check_count, total_count, pipe_id, rate_95_value))
        except Exception as e:
            logger.exception(e)
    ck_client.disconnect()
    sheet_row = 1
    for (customer_id, customer_name), rate_95_value in customer_flow_dict.items():
        sheet_one.write(sheet_row, 0, customer_id, default_style)
        sheet_one.write(sheet_row, 1, customer_name, default_style)
        sheet_one.write(sheet_row, 2, rate_95_value, default_style)
        sheet_row += 1
    work_book.save('real_flow.xls')

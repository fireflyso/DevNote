"""
完全按照GIC系统格式进行流量批量导出
（张志景提的需求）
有三个账户：zhimeiwangluo、sanqiwangluo、yingtongwangluo，分别导出这三个账户下的pipe的计量数据
由于每个vdc下只有一个pipe，所以导出的文件名为vdc的名称即可
"""

from clickhouse_driver import Client
import xlwt
import requests
import json

import pymysql

db = pymysql.connect(
    host="write-mysql.gic.local",
    user="resop_20210108",
    password="1snzvbhdEOhfW4LArq$5",
    database="cdscp",
    port=6033,
    charset='utf8'
)

cursor = db.cursor()

CK_HOST = "10.13.133.134"
CK_USER = "flowdata"
CK_PASSWORD = "wVen6RK3KpkpGdsA"
CK_DB_ANME = "flow_snmp"
CK_PORT = 9000
client = Client(host=CK_HOST, port=CK_PORT, user=CK_USER, password=CK_PASSWORD)

def set_style(name, height, bold=False):
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = name
    font.bold = bold
    font.color_index = 4
    font.height = height
    style.font = font
    return style


row0 = ["pipe id", "时间", "入流量(M)", "出流量(M)"]
default_style = set_style('Times New Roman', 220, True)
start_time = '2022-08-01 00:00:00'
end_time = '2022-09-01 00:00:00'
index = 1
user_dict = {
    "zhimeiwangluo": "zhimeiwangluo",
    "656217": "sanqiwangluo",
    "691361": "yingtongwangluo",
}
for user_id, user_name in user_dict.items():
    sql = "SELECT DISTINCT a.id, d.name from cloud_pipe a, bc_bill_resources_price b, bc_billing_scheme c, cloud_app d WHERE a.app_id in (SELECT id from cloud_app WHERE customer_user_id='{}' and is_valid=1) and a.type='public' and a.is_valid=1 and a.id=b.cloud_id and b.end_time>now() and b.billing_scheme_id=c.id and c.`name` like '%95%' and a.app_id = d.id".format(user_id)
    cursor.execute(sql)
    one_res = cursor.fetchall()
    for one_info in one_res:
        pipe_id = one_info[0]
        vdc_name = one_info[1]
        print("查询pipe : {}".format(pipe_id))
        data = {
            "start_time": start_time,
            "cloud_id": pipe_id,
            "end_time": end_time
        }

        try:
            url = 'http://wan-flow-bps.gic.pre/bps_95'
            res = json.loads(requests.post(url, data).content)

            value_95 = res.get('data')[0].get('value')

            url = 'http://wan-flow-bps.gic.pre/max'
            res = json.loads(requests.post(url, data).content)
            max_value = max(res.get('data')[0].get('out_bps_max'), res.get('data')[0].get('in_bps_max'))
            min_value = min(res.get('data')[0].get('out_bps_min'), res.get('data')[0].get('in_bps_min'))

            url = 'http://wan-flow-bps.gic.pre/bps_list'
            res = json.loads(requests.post(url, data).content)
            avg_value = max(res.get('average')[0].get('in_bps'), res.get('average')[0].get('out_bps'))
        except:
            print('数据解析异常：')
            print('url : {}'.format(url))
            continue

        sql = "SELECT size, max_size from bc_bill_resources_price where cloud_id = '{}' and end_time>now() and is_valid = 1".format(pipe_id)
        cursor.execute(sql)
        two_res = cursor.fetchall()[0]
        min_qos = two_res[0]
        max_qos = two_res[1]

        f = xlwt.Workbook()
        sheet = f.add_sheet("95峰值监控图", cell_overwrite_ok=True)
        sheet.write(0, 0, '最高值:{} Mbps'.format(round(float(max_value)/1024/1024, 3)), default_style)
        sheet.write(0, 1, '最低值:{} Mbps'.format(round(float(min_value)/1024/1024, 3)), default_style)
        sheet.write(0, 2, '平均值:{} Mbps'.format(round(float(avg_value)/1024/1024, 3)), default_style)
        sheet.write(0, 3, '95计费值:{} Mbps'.format(round(float(value_95)/1024/1024, 3)), default_style)
        sheet.write(0, 4, '保底带宽:{} Mbps'.format(min_qos), default_style)
        sheet.write(0, 5, '封顶带宽:{} Mbps'.format(max_qos), default_style)
        sheet.write(1, 0, '日期', default_style)
        sheet.write(1, 1, '出网带宽(Mbps)', default_style)
        sheet.write(1, 2, '入网带宽(Mbps)', default_style)

        sql = "select time, in_bps, out_bps from flow_snmp.flow_data where pipe_id = '{}' and time >= '{}' and time < '{}' order by time".format(pipe_id, start_time, end_time)
        data_list = client.execute(sql)
        row = 2
        for data in data_list:
            sheet.write(row, 0, str(data[0]), default_style)
            sheet.write(row, 1, round(float(str(data[2]))/1024/1024, 3), default_style)
            sheet.write(row, 2, round(float(str(data[1]))/1024/1024, 3), default_style)
            row += 1

        f.save('flow_file/{}/{}.xls'.format(user_name, vdc_name))

cursor.close()

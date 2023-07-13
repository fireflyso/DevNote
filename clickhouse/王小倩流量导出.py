# -- coding: utf-8 --
# @Time : 2023/6/26 17:57
# @Author : xulu.liu
from clickhouse_driver import Client
import xlwt

def set_style(name, height, bold=False):
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = name
    font.bold = bold
    font.color_index = 4
    font.height = height
    style.font = font
    return style

CK_HOST = "10.13.133.134"
CK_USER = "flowdata"
CK_PASSWORD = "wVen6RK3KpkpGdsA"
CK_DB_ANME = "flow_snmp"
CK_PORT = 9000
client = Client(host=CK_HOST, port=CK_PORT, user=CK_USER, password=CK_PASSWORD)

start_time = '2023-06-01 00:00:00'
end_time = '2023-06-26 00:00:00'
pipe_list = ['0c6327b0-e570-11ed-89e1-a2a9a35533a5', '63f40dc8-0073-11ee-a4aa-e27800858960', 'ac66640e-01d4-11ee-8007-6e3048f796e3', 'd3f9898e-eb17-11ed-b796-76fc3df52df9', 'e7a629e4-0073-11ee-897b-6a6fa8c8be77', 'fc9a795e-f312-11ed-8dd4-b68111c315ad']
default_style = set_style('Times New Roman', 220, True)
f = xlwt.Workbook()
for pipe_id in pipe_list:
    print('start : {}'.format(pipe_id))
    res = client.execute("select time, in_flow, out_flow from flow_snmp.flow_data where pipe_id = '{}' and time >= '{}' and time < '{}' order by time".format(pipe_id, start_time, end_time))
    temp_in = 0
    temp_out = 0
    sheet = f.add_sheet(pipe_id[:30], cell_overwrite_ok=True)
    sheet.write(0, 0, 'pipe id : {}'.format(pipe_id), default_style)
    sheet.write(1, 0, '时间', default_style)
    sheet.write(1, 1, '入向流量', default_style)
    sheet.write(1, 2, '出向流量', default_style)
    row = 2
    for r in res:
        in_flow = r[1]
        out_flow = r[2]
        # print("{},{},{}".format(r[0], in_flow-temp_in, out_flow-temp_out))
        sheet.write(row, 0, str(r[0]), default_style)
        sheet.write(row, 1, str(in_flow-temp_in), default_style)
        sheet.write(row, 2, str(out_flow-temp_out), default_style)
        row += 1
        temp_in = in_flow
        temp_out = out_flow

f.save('C018970.xls')
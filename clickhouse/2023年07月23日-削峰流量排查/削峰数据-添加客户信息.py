# -- coding: utf-8 --
# @Time : 2023/7/22 11:19
# @Author : xulu.liu
import pymysql
import traceback
import xlwt
import pymysql

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
row0 = ["pipe", "削峰数量", "削峰总带宽", "最大削峰带宽", "限速带宽", "客户id", "客户名称", "节点", "平均超限", "最大超限比例"]
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

execpt_pipe = []
sheet_row = 1
with open("/root/work/log/0721/aa.txt") as file:
    for line in file:
        line = line.replace('\n', '')
        info = line.split(',')
        pipe_id = info[0]
        over_count = int(info[1])
        total_over = int(info[2])
        max_over = int(info[3])
        sql = "select a.id, a.qos, b.customer_id, b.name, d.name from cloud_pipe a, account_customer b, cloud_app c, cloud_datacenter d where a.id = '{}' and a.customer_id = b.id and a.app_id = c.id and c.site_id = d.id;".format(pipe_id)
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

        if len(res):
            qos = res[0][1]
            customer_id = res[0][2]
            customer_name = res[0][3]
            site_name = res[0][4]
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
        else:
            execpt_pipe.append(pipe_id)

print(execpt_pipe)
print(len(execpt_pipe))
f.save('flow.xls')
cursor.close()

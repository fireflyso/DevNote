import time

import requests
from lxml import etree
import utils_logger
import random
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
sheet1 = f.add_sheet('sheet1', cell_overwrite_ok=True)
row0 = ["名称", "简介"]
sheet_list = [sheet1]
default_style = set_style('Times New Roman', 220, True)
for i in range(0, len(row0)):
    for sheet in sheet_list:
        sheet.write(0, i, row0[i], default_style)


# 打开数据库连接
db = pymysql.connect(
    host="103.229.214.35",
    user="firefly",
    password="cds-cloud@2017",
    database="flow_data",
    port=3306
)
cursor = db.cursor()
sql = 'select * from company_info where id > 9060'
res = cursor.execute(sql)
res_list = cursor.fetchall()

print("公司数量： {}".format(len(res_list)))
row = 0
for company_info in res_list:
    sheet.write(row, 0, company_info[1], default_style)
    sheet.write(row, 1, company_info[8], default_style)
    row += 1

f.save('公司介绍.xls')
cursor.close()

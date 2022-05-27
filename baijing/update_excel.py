import xlrd
import pymysql
from xlutils.copy import copy

# 打开数据库连接
db = pymysql.connect(
    host="103.229.214.35",
    user="firefly",
    password="cds-cloud@2017",
    database="flow_data",
    port=3306
)
cursor = db.cursor()
sql = 'select name, address, `desc` from company_info where id < 10000'
res = cursor.execute(sql)
res_list = cursor.fetchall()

print("公司数量： {}".format(len(res_list)))
company_name_dir = {res[0]: res for res in res_list}


new_company_list = []
workbook = xlrd.open_workbook('./company_info.xls')  # 打开工作簿
sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
worksheet = workbook.sheet_by_name(sheets[1])  # 获取工作簿中所有表格中的的第一个表格
new_excel = copy(workbook)
table = new_excel.get_sheet(1)
for i in range(0, worksheet.nrows):
    for j in range(0, worksheet.ncols):
        if j == 2:
            company_name = worksheet.cell_value(i, j)
            res = company_name_dir.get(company_name, ['', '', ''])
            table.write(i, 9, res[1])
            table.write(i, 10, res[2])

new_excel.save("ttt.xls")
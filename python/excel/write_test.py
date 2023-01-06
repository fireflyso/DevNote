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
sheet1 = f.add_sheet('游戏', cell_overwrite_ok=True)
sheet2 = f.add_sheet('电商', cell_overwrite_ok=True)
sheet3 = f.add_sheet('应用', cell_overwrite_ok=True)
sheet4 = f.add_sheet('文化娱乐', cell_overwrite_ok=True)
sheet5 = f.add_sheet('开发者服务', cell_overwrite_ok=True)
sheet6 = f.add_sheet('区块链', cell_overwrite_ok=True)
sheet7 = f.add_sheet('人工智能', cell_overwrite_ok=True)
row0 = ["名称", "全称", "行业", "融资状态", "地区", "公司规模", "网址", "简介", "全名简介"]
sheet_list = [sheet1, sheet2, sheet3, sheet4, sheet5, sheet6, sheet7]
sheet_dir = {
    '游戏': sheet1,
    '电商': sheet2,
    '应用': sheet3,
    '文化娱乐': sheet4,
    '开发者服务': sheet5,
    '区块链': sheet6,
    '人工智能': sheet7,
}
sheet_row_dir = {}
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
sql = 'select * from company_info where id < 10000'
res = cursor.execute(sql)
res_list = cursor.fetchall()

print("公司数量： {}".format(len(res_list)))
for company_info in res_list:
    type_info = company_info[3]
    for type, sheet in sheet_dir.items():
        if type in type_info:
            sheet_row = sheet_row_dir.get(type, 1)
            sheet_row_dir[type] = sheet_row + 1
            for line in range(9):
                sheet.write(sheet_row, line, company_info[line+1], default_style)

print(sheet_row_dir)
f.save('企业名单-简介.xls')
cursor.close()

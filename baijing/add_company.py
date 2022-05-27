import pymysql

# 打开数据库连接
db = pymysql.connect(
    host="103.229.214.35",
    user="firefly",
    password="cds-cloud@2017",
    database="flow_data",
    port=3306
)
cursor = db.cursor()


company_list = "扬帆出海,游戏陀螺,白鲸出海,游戏茶馆,七麦数据,游戏猫,游戏葡萄,App Annie,NewZoo,伽马数据,GPC&IDC,出海独联体,游戏工委,Wind资讯,The Verge中文站,Sensor Tower,Taptap发现好游戏,彭博Bloomberg,GameRes游资网,游戏日报,国海证券,申万宏源研究,艾瑞咨询".split(',')

sql = "INSERT INTO company_info(name, full_name, type_list, financing, address, company_member_count, web_url) VALUES (%s,%s,%s,%s,%s,%s,%s)"

company_info_list = []
for name in company_list:
    company = (name, '', '', '', '', '', '')
    company_info_list.append(company)

try:
    cursor.executemany(sql, tuple(company_info_list))
    db.commit()
except Exception as e:
    db.rollback()
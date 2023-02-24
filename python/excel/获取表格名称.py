# -- coding: utf-8 --
# @Time : 2023/2/15 16:45
# @Author : xulu.liu
# @File : 获取表格名称.py
# @Software: PyCharm

import pandas as pd
bb = pd.ExcelFile('test01.xlsx', None)
sheet_list = bb.sheet_names
print('所有表名', sheet_list)
table_count = len(sheet_list)

pid5_asn = []
pid11_asn = []
pid22_asn = []
pid20_asn = []
pid5_asn = []


all_asn = {}
for index in range(table_count):
    country_name = sheet_list[index]
    df = pd.read_excel('test01.xlsx', sheet_name=index)
    for i in range(len(df)):
        # asn_dict[int(df.values[i, 0])] = df.values[i, 1]
        asn = str(df.values[i, 0]).replace('AS', '')
        all_asn.setdefault(country_name, []).append(asn)

print(all_asn)

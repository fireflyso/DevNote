import datetime
import os

import pymysql
import xlwt
from pymongo import MongoClient

db = pymysql.connect(
    host="write-mysql.gic.local",
    user="resop_20210108",
    password="1snzvbhdEOhfW4LArq$5",
    database="cdscp",
    port=6033,
    charset='utf8'
)

cursor = db.cursor()


MONGO_STR = 'mongodb://10.13.226.20:27017/'
MONGO_DB_NAME = 'flow_mete'
MONGO_DB_COLLECTION_10S = 'flow_data_10s'
MONGO_DB_COLLECTION_30S = 'flow_data_30s'
MONGO_DB_COLLECTION_1M = 'flow_data_1m'
MONGO_DB_maxPoolSize = 100
MONGO_DB_waitQueueMultiple = 5
client = MongoClient(MONGO_STR, maxPoolSize=MONGO_DB_maxPoolSize, waitQueueMultiple=MONGO_DB_waitQueueMultiple,
                     waitQueueTimeoutMS=30000, socketTimeoutMS=30000)
db = client[MONGO_DB_NAME]
collection = db[MONGO_DB_COLLECTION_30S]

gic_list = ['', '', '']
gic_dir = {
    '00ea4818-3049-11e9-8d22-0242ac110002': 'webcdn',
    '4aec932c-787d-11e9-9774-0242ac110002': 'PushApple 100 1000',
    '565c694e-0a4c-11e8-9170-0242ac110002': 'ops 100 250'
}

end = datetime.datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
start = end.replace(month=end.month-1)
print('开始清理历史数据文件')
os.system("rm -rf avg_95.xls")


def set_style(name, height, bold=False):
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = name
    font.bold = bold
    font.color_index = 4
    font.height = height
    style.font = font
    return style

default_style = set_style('Times New Roman', 220, True)
f = xlwt.Workbook()
for gic_id, name in gic_dir.items():
    sheet = f.add_sheet(name, cell_overwrite_ok=True)
    for index in range(1, 32):
        sheet.write(index, 0, '{}号'.format(index), default_style)
    sheet.write(32, 0, '月平均95', default_style)
    sheet.write(33, 0, '保底带宽', default_style)
    sheet.write(34, 0, '超出带宽', default_style)
    sql = "SELECT a.pipe_id, b.name, a.qos, a.min_charge_per from cloud_gic_star_point a, cloud_city b where gic_id ='{}' and a.is_valid = 1 and a.type = 'edge' and a.city_id = b.id".format(gic_id)
    res = cursor.execute(sql)
    pipe_res_list = cursor.fetchall()
    line_num = 0
    for pipe_res in pipe_res_list:
        row_num = 0
        line_num += 1
        pipe_id = pipe_res[0]
        print(pipe_id)
        sheet.write(0, line_num, '{} - {}'.format(pipe_res[1], pipe_id), default_style)
        query = {
            "pipe_id": pipe_id,
            "time": {"$lt": end, "$gte": start},
        }
        res = list(collection.find(query, {'out_bps': 1, 'in_bps': 1, 'time': 1, '_id': 0}))
        num = len(res)
        if num != 0:
            date_dir = {}
            for flow in res:
                time = flow['time'].date()
                date_dir.setdefault(time, []).append(flow)

            list_95 = []
            for time, flow_list in date_dir.items():
                row_num += 1
                flow_dir = {flow['time']: flow for flow in flow_list}
                temp_time = datetime.datetime.combine(time, datetime.time())
                five_minutes_list = []
                for _ in range(288):
                    five_minutes_value = -1
                    for _ in range(5):
                        flow = flow_dir.get(temp_time, {})
                        first_out_bps = flow.get('out_bps', -1)
                        first_in_bps = flow.get('in_bps', -1)
                        temp_time += datetime.timedelta(seconds=30)
                        flow = flow_dir.get(temp_time, {})
                        second_out_bps = flow.get('out_bps', -1)
                        second_in_bps = flow.get('in_bps', -1)
                        if second_out_bps >= 0:
                            avg_out_bps = (first_out_bps + second_out_bps) / 2 if first_out_bps >= 0 else second_out_bps
                            avg_in_bps = (first_in_bps + second_in_bps) / 2 if first_in_bps >= 0 else second_in_bps
                        else:
                            avg_out_bps = first_out_bps
                            avg_in_bps = first_in_bps

                        five_minutes_value = max(five_minutes_value, avg_out_bps, avg_in_bps)
                    if five_minutes_value >= 0:
                        five_minutes_list.append(five_minutes_value)

                if five_minutes_list:
                    # 之前是降序排列取5%的点，下面的公式存在问题，假如有10个点，会取第一个点作为95
                    # index = int(len(five_minutes_list) * 5 / 100)
                    index = int(len(five_minutes_list) * 95 / 100)
                    five_minutes_list.sort()
                    temp_value = round(five_minutes_list[index]/1000/1000, 2)
                    list_95.append(temp_value)
                    sheet.write(row_num, line_num, '{}M'.format(temp_value), default_style)

            row_num += 1
            avg_value = 0
            if list_95:
                avg_value = round(sum(list_95) / len(list_95), 2)
                sheet.write(row_num, line_num, '{}'.format(avg_value), default_style)

            min_value = float(pipe_res[2]) * float(pipe_res[3])
            beyond_value = avg_value - min_value
            beyond_value = beyond_value if beyond_value > 0 else 0
            sheet.write(33, line_num, '{}'.format(min_value), default_style)
            sheet.write(34, line_num, beyond_value, default_style)

f.save('avg_95.xls')
cursor.close()

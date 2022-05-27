# coding=utf-8
# 20210702的一个需求，将某个pipe超过250M带宽流量的信息导出到Excel
from pymongo import MongoClient
from datetime import datetime, timedelta
import xlwt

MONGO_STR = 'mongodb://10.13.2.111:27017,10.13.2.112:27017/flow_snmp'
MONGO_DB_maxPoolSize = 100
MONGO_DB_waitQueueMultiple = 5
client = MongoClient(MONGO_STR, maxPoolSize=MONGO_DB_maxPoolSize, waitQueueMultiple=MONGO_DB_waitQueueMultiple,
                     waitQueueTimeoutMS=30000, socketTimeoutMS=30000)
MONGO_DB_NAME = 'flow_snmp'
db = client[MONGO_DB_NAME]
MONGO_DB_COLLECTION = 'flow_data'
collection = db[MONGO_DB_COLLECTION]

end_time = datetime.strptime(str(datetime.now().date()), '%Y-%m-%d') + timedelta(-1)
start_time = end_time + timedelta(-30)

pipe_id = 'a4d78fe4-6ddc-11e6-92ad-0242ac100602'
query = {
    "pipe_id": pipe_id,
    "time": {"$lte": end_time, "$gte": start_time},
}
res_list = list(collection.find(query, {'out_bps': 1, 'in_bps': 1, 'time': 1, '_id': 0}))


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
sheet1 = f.add_sheet('flow_data', cell_overwrite_ok=True)
row0 = ["pipe_id", u"时间", u"出网流量", u"入网流量"]
for i in range(0, len(row0)):
    sheet1.write(0, i, row0[i], set_style('Times New Roman', 220, True))

index = 1
mbps = 1024 * 1024
for res in res_list:
    if res.get('out_bps', 0) > 250*1024*1024 or res.get('in_bps', 0) > 250*1024*1024:
        time = res.get('time', '').strftime('%y-%m-%d %I:%M:%S')
        print("time : {}".format(time))
        sheet1.write(index, 0, pipe_id, set_style('Times New Roman', 220, True))
        sheet1.write(index, 1, time, set_style('Times New Roman', 220, True))
        sheet1.write(index, 2, round(res.get('out_bps', 0) / mbps, 2), set_style('Times New Roman', 220, True))
        sheet1.write(index, 3, round(res.get('in_bps', 0) / mbps, 2), set_style('Times New Roman', 220, True))
        index += 1

f.save('test.xls')

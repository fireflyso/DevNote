# -- coding: utf-8 --
# @Time : 2023/7/2 12:06
# @Author : xulu.liu

# 5分钟库
from pymongo import MongoClient
from datetime import datetime, timedelta
MONGO_STR = 'mongodb://10.13.2.112:27017/'
MONGO_DB_NAME = 'flow_snmp'
MONGO_TABLE_NAME = 'flow_data'
MONGO_DB_maxPoolSize = 100
MONGO_DB_waitQueueMultiple = 5
client = MongoClient(MONGO_STR, maxPoolSize=MONGO_DB_maxPoolSize, waitQueueMultiple=MONGO_DB_waitQueueMultiple,
                     waitQueueTimeoutMS=30000, socketTimeoutMS=30000)
db = client[MONGO_DB_NAME]
collection = db[MONGO_TABLE_NAME]

pipe_id = 'f69a5bfa-f45c-11ed-a219-e24846a47d7c'
start_time = datetime.strptime('2023-06-01 00:00:00', '%Y-%m-%d %H:%M:%S')
end_time = datetime.strptime('2023-07-01 19:20:00', '%Y-%m-%d %H:%M:%S')

query = {
    'pipe_id': pipe_id,
    "time": {"$lte": end_time, "$gte": start_time}
}
# list(collection.find(query).sort([('time', 1)]))
# collection.delete_many(query)

def get_data_list():
    flow_list = []
    max_time = datetime.strptime('2023-06-01 00:00:00', '%Y-%m-%d %H:%M:%S')
    for line in open("2001.out"):
        time_str = line.split('.csv')[0]
        flow_time = '{}-{}-{} {}:{}:00'.format(time_str[:4], time_str[4:6], time_str[6:8], time_str[9:11], time_str[12:14])
        out_bps = float(line.split(',')[-2])
        in_bps = float(line.split(',')[-1].replace('\n', ''))
        # logger.info('time : {}, in : {}, out : {}'.format(flow_time, in_bps, out_bps))
        flow_list.append((datetime.strptime(flow_time, '%Y-%m-%d %H:%M:%S'), in_bps, out_bps))
        if datetime.strptime(flow_time, '%Y-%m-%d %H:%M:%S') > max_time:
            max_time = datetime.strptime(flow_time, '%Y-%m-%d %H:%M:%S')
    print(max_time)
    return flow_list

flow_list = get_data_list()
insert_data = []
for flow_data in flow_list:
    time, in_bps, out_bps = flow_data
    insert_data.append({
        'pipe_id': pipe_id, 'time': time,
        'in_flow': 1.0, 'out_flow': 1.0, 'in_bps': in_bps, 'out_bps': out_bps
    })

print('count : {}'.format(len(insert_data)))
result = collection.insert_many(insert_data)
print('insert : {}'.format(len(result.inserted_ids)))
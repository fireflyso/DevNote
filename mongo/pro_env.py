# 30s库
from pymongo import MongoClient
from datetime import datetime, timedelta

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
start_time = datetime.strptime('2023-07-11 13:55:16', '%Y-%m-%d %H:%M:%S')
list(collection.find({'pipe_id': 'd9641931-2ca3-4940-9100-b31f5459130a', 'time': {"$gt": start_time}}).sort([('time', 1)]).limit(3))


start_time = datetime.strptime('2022-04-15 10:55:27', '%Y-%m-%d %H:%M:%S')
end_time = datetime.strptime('2022-04-15 11:17:02', '%Y-%m-%d %H:%M:%S')
query = {
    'pipe_id': '3a9a9ff8-b710-11ec-9bfc-8252cbfa8cce',
    "time": {"$lte": end_time, "$gt": start_time}
}
res_list = list(collection.find(query).sort([('time', 1)]))

for info in list(collection.find(query, {'_id': 0}).limit(30)):
    print(info)

pipe_list = ['2891320e-f1c1-11e7-96f3-0242ac110002','eca9cadc-9dea-11e7-b9b0-0242ac110002','16c5a4ca-bd98-11e9-ad3c-0242ac110002','c169caa0-f1c0-11e7-9908-0242ac110002','2891320e-f1c1-11e7-96f3-0242ac110002','a9cd68f0-eb30-11e9-a8e3-0242ac110002','c169caa0-f1c0-11e7-9908-0242ac110002','0940b37e-c8ca-11ea-a47a-0242ac110002','74097ee4-04cb-11e9-9a97-0242ac110002','a66bfaec-6954-11ec-a237-a6cf2cd47dab','b150a32e-8bb7-11e7-be82-0242ac110002','484ec8e0-4196-11e6-bf47-0050569b1b91','b55fdbfc-c32f-11e6-8ad6-0242ac110002','1deab2ee-a6ea-11e6-8a77-0242ac110002','e2ceb6ce-f1c0-11e7-ad1b-0242ac110002','484ec8e0-4196-11e6-bf47-0050569b1b91','88c3c156-f1c0-11e7-b540-0242ac110002','e2ceb6ce-f1c0-11e7-ad1b-0242ac110002','2bad4fb0-9b36-11ea-9258-e6b573eee7ea']
res_list = []
for pipe in pipe_list:
    query = {
        'pipe_id': pipe,
        "time": {"$lt": end_time, "$gte": start_time}
    }
    count = collection.find(query).count()
    if count > 0:
        print('pipe : {}, count : {}'.format(pipe, count))
        res_list.append(pipe)






start_time = datetime.strptime('2021-12-08 00:00:00', '%Y-%m-%d %H:%M:%S')
end_time = datetime.strptime('2021-12-09 00:00:00', '%Y-%m-%d %H:%M:%S')
query = {
    "pipe_id": '82cfef9a-3369-11e9-9814-0242ac110002',
    "time": {"$lte": end_time, "$gte": start_time},
}
list(collection.find(query).sort([('time', -1)]).limit(10))

res_list = list(collection.find({'pipe_id': '01b6965e-8e2c-11ec-9bc2-aaf80d791f30'}, {'in_flow': 1, 'out_flow': 1, 'out_bps': 1, 'in_bps': 1, 'time': 1, '_id': 0}).sort([('time', -1)]))
list(collection.find({'pipe_id': '01b6965e-8e2c-11ec-9bc2-aaf80d791f30'}, {'in_flow': 1, 'out_flow': 1, 'out_bps': 1, 'in_bps': 1, 'time': 1, '_id': 0}).sort([('time', -1)]))
for res in res_list:
    res['pipe_id'] = '50b945ba-8836-11ea-a35a-82fc29d74e44'

res_list = sorted(res_list, key=lambda l: l['time'])
result = collection.insert_many(res_list)

res_list = list(collection.find({'pipe_id': 'a1ebf59e-8e11-11ec-a274-aaf80d791f30'}, {'in_flow': 1, 'out_flow': 1, 'out_bps': 1, 'in_bps': 1, 'time': 1, '_id': 0}).sort([('time', -1)]))
for res in res_list:
    res['pipe_id'] = '5a9aa7b4-bffd-11ea-8115-0242ac110002'

res_list = sorted(res_list, key=lambda l: l['time'])
result = collection.insert_many(res_list)
# print("pipe : {} insert res : {}".format(pipe_id, len(result.inserted_ids)))


start_time = datetime.strptime('2022-05-11 07:07:05', '%Y-%m-%d %H:%M:%S')
end_time = datetime.strptime('2022-05-11 16:37:05', '%Y-%m-%d %H:%M:%S')
query = {
    "pipe_id": '30aa2a22-0653-11ec-9ca9-0a0d265d6421',
    "time": {"$lte": end_time, "$gte": start_time},
}
list(collection.find(query))
# collection.remove(query)





end_time = datetime.now() + timedelta(-1)
start_time = end_time + timedelta(-30)
query = {
    'pipe_id': '1edfb184-0a5f-11e8-9330-0242ac110002',
    "time": {"$lte": end_time, "$gte": start_time}
}
res_list = list(collection.find().sort([('time', -1)]).limit(10))
res_list = list(collection.find().sort([('time', -1)]).limit(10))
list(collection.find({'pipe_id': '2f602040-28c7-11ec-92c6-4aa9b5806a6a'}).limit(10))

collection.find({'pipe_id': '50b945ba-8836-11ea-a35a-82fc29d74e44'}).count()
collection.find({'pipe_id': 'c780f801-62f1-4c58-8c5b-4623125892ea'}).count()
res_list = list(collection.find({'pipe_id': '50b945ba-8836-11ea-a35a-82fc29d74e44'}, {'in_flow':1, 'out_flow':1,'out_bps': 1, 'in_bps': 1, 'time': 1, '_id': 0}).sort([('time', -1)]).limit(10))

collection.find({'pipe_id': '5a9aa7b4-bffd-11ea-8115-0242ac110002'}).count()
collection.find({'pipe_id': '9b2c873e-cb5c-446f-8163-3eb54e4f6c27'}).count()
res_list = list(collection.find({'pipe_id': '5a9aa7b4-bffd-11ea-8115-0242ac110002'}, {'in_flow':1, 'out_flow':1,'out_bps': 1, 'in_bps': 1, 'time': 1, '_id': 0}).sort([('time', -1)]).limit(1))


import time
start_at = time.perf_counter()
res_list = list(collection.find(query))
print(time.perf_counter() - start_at)
print()
list(collection.find({'pipe_id': '3a9a9ff8-b710-11ec-9bfc-8252cbfa8cce', 'time': datetime.strptime('2022-04-08 17:25:27', '%Y-%m-%d %H:%M:%S')}))


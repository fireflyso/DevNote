from pymongo import MongoClient
from datetime import datetime, timedelta
import pymongo

MONGO_STR = 'mongodb://10.2.10.23:27017'
MONGO_DB_maxPoolSize = 100
MONGO_DB_waitQueueMultiple = 5
client = MongoClient(MONGO_STR, maxPoolSize=MONGO_DB_maxPoolSize, waitQueueMultiple=MONGO_DB_waitQueueMultiple,
                     waitQueueTimeoutMS=30000, socketTimeoutMS=30000)
MONGO_DB_NAME = 'flow_snmp'
db = client[MONGO_DB_NAME]
MONGO_DB_COLLECTION = 'flow_data'
collection = db[MONGO_DB_COLLECTION]


end_time = datetime.now() + timedelta(-90)
start_time = end_time + timedelta(-3)
pipe_id = 'a240bca6-ca7f-11eb-a6a9-421c197ea2ab'
query = {
    "pipe_id": pipe_id,
    "time": {"$lte": end_time, "$gte": start_time},
}
res_list = list(collection.find(query, {'out_bps': 1, 'in_bps': 1, 'time': 1, '_id': 0}))


# 30s库
from pymongo import MongoClient
from datetime import datetime, timedelta
MONGO_STR = 'mongodb://10.2.10.23:27017'
MONGO_DB_maxPoolSize = 100
MONGO_DB_waitQueueMultiple = 5
client = MongoClient(MONGO_STR, maxPoolSize=MONGO_DB_maxPoolSize, waitQueueMultiple=MONGO_DB_waitQueueMultiple,
                     waitQueueTimeoutMS=30000, socketTimeoutMS=30000)
MONGO_DB_NAME = 'flow_mete'
db = client[MONGO_DB_NAME]
MONGO_DB_COLLECTION = 'flow_data_30s'
collection = db[MONGO_DB_COLLECTION]


# 数据插入
# time = datetime(2021, 7, 3, 17, 12)
# for _ in range(864):
#     data_list = []
#     for _ in range(100):
#         time = time + timedelta(seconds=30)
#         data = {
#             'out_bps': 693446.862,
#             'pipe_id': 'bcd219de-79dd-11e8-8746-0242ac110002',
#             'in_bps': 10485760.0,
#             'time': time
#         }
#         data_list.append(data)
#     collection.insert(data_list)

end_time = start_time + timedelta(30)
start_time = datetime(2021, 7, 3, 17, 12)
query = {
    "pipe_id": 'bcd219de-79dd-11e8-8746-0242ac110002',
}
res = list(collection.find(query, {'out_bps': 1, 'in_bps': 1, 'time': 1, '_id': 0}))
res = list(collection.find(query, {'out_bps': 1, 'in_bps': 1, 'time': 1, '_id': 0}))
collection.find(query, {'out_bps': 1, 'in_bps': 1, 'time': 1, '_id': 0}).count()
print(len(res))

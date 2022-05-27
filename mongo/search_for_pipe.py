# coding=utf-8
# 20210705的一个需求，pipe计量缺失
from pymongo import MongoClient
from datetime import datetime, timedelta
import pymongo

MONGO_STR = 'mongodb://10.13.2.111:27017,10.13.2.112:27017/flow_snmp'
MONGO_DB_maxPoolSize = 100
MONGO_DB_waitQueueMultiple = 5
client = MongoClient(MONGO_STR, maxPoolSize=MONGO_DB_maxPoolSize, waitQueueMultiple=MONGO_DB_waitQueueMultiple,
                     waitQueueTimeoutMS=30000, socketTimeoutMS=30000)
MONGO_DB_NAME = 'flow_snmp'
db = client[MONGO_DB_NAME]
MONGO_DB_COLLECTION = 'flow_data'
collection = db[MONGO_DB_COLLECTION]


end_time = datetime.now()
start_time = end_time + timedelta(-3)
pipe_id = '9a230d14-a192-11eb-8b35-5aba238cc421'
query = {
    "pipe_id": pipe_id,
    "time": {"$lte": end_time, "$gte": start_time},
}
res_list = list(collection.find(query, {'out_bps': 1, 'in_bps': 1, 'time': 1, '_id': 0}))


start_time = datetime(2021, 7, 23, 15, 00, 00)
end_time = datetime(2021, 7, 23, 16, 30, 00)

query = {
    "pipe_id": "4fcefafa-76ee-11e9-811d-0242ac110002",
    "time": {"$lte": end_time, "$gte": start_time},
}
list(collection.find(query).limit(10))

query = {"pipe_id": 'ecf9c2e4-41bf-11e7-a836-0242ac110002', 'time': {"$gte": datetime(2021, 7, 10, 10, 00, 00)}}
list(collection.find(query).sort("time", pymongo.DESCENDING).limit(1))
list(collection.find({"pipe_id": '1485d36e-306b-11e6-8ecd-0050569b1b91'}).sort("time", pymongo.DESCENDING).limit(1))

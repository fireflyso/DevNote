from pymongo import MongoClient
from datetime import datetime, timedelta
import pymongo

MONGO_STR = 'mongodb://10.2.10.126:27017'
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
pipe_id = '0f75a5e4-c11e-11ec-bc93-8a89b578c8ab'
query = {
    "pipe_id": pipe_id
}
res_list = list(collection.find(query, {'out_bps': 1, 'in_bps': 1, 'time': 1, '_id': 0}))
print(res_list)


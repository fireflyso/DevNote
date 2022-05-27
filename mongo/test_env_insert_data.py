# -*- coding: utf-8 -*-
"""
11月26：静子姐测需要给pipe插入30s计量数据
"""

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
time = datetime(2021, 12, 15, 16)
for _ in range(30):
    data_list = []
    for _ in range(100):
        time = time + timedelta(seconds=30)
        data = {
            'out_bps': 314572800,
            'pipe_id': 'f86edbb0-5d84-11ec-b190-22e3437a7c37',
            'in_bps': 304572800,
            'time': time
        }
        data_list.append(data)
    collection.insert_many(data_list)
    print(time)

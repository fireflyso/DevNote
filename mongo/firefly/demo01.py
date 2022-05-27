from pymongo import MongoClient
import random

MONGO_STR = 'mongodb://49.232.142.109:10086'
MONGO_DB_maxPoolSize = 100
MONGO_DB_waitQueueMultiple = 5
client = MongoClient(MONGO_STR, maxPoolSize=MONGO_DB_maxPoolSize, waitQueueMultiple=MONGO_DB_waitQueueMultiple,
                     waitQueueTimeoutMS=30000, socketTimeoutMS=30000)
MONGO_DB_NAME = 'firefly'
db = client[MONGO_DB_NAME]
MONGO_DB_COLLECTION = 'index_test'
collection = db[MONGO_DB_COLLECTION]

for _ in range(100):
    data_list = []
    for _ in range(100):
        data_list.append({
            'name': ''.join(random.sample('zyxwvutsrqponmlkjihgfedcba', 5)),
            'age': random.randint(10, 100)
        })
    collection.insert_many(data_list)
    print('insert 100 record')

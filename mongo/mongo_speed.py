# coding=utf-8
# 测试 MongoDB 中数据查询的速度
from pymongo import MongoClient
from datetime import datetime

MONGO_STR = 'mongodb://10.13.2.111:27017,10.13.2.112:27017/flow_snmp'
MONGO_DB_maxPoolSize = 100
MONGO_DB_waitQueueMultiple = 5
client = MongoClient(MONGO_STR, maxPoolSize=MONGO_DB_maxPoolSize, waitQueueMultiple=MONGO_DB_waitQueueMultiple,
                     waitQueueTimeoutMS=30000, socketTimeoutMS=30000)
MONGO_DB_NAME = 'flow_snmp'
db = client[MONGO_DB_NAME]
MONGO_DB_COLLECTION = 'flow_data'
collection = db[MONGO_DB_COLLECTION]

start_time = datetime(2021, 6, 1, 12, 00, 00)
end_time = datetime(2021, 7, 1, 12, 00, 00)
start_at = datetime.now()
pipe_list = [u'03d3dba8-ca70-11ea-ad09-0242ac110002', u'0d869dd4-6765-11ea-b9cf-0242ac110002', u'12958824-f4ee-11e9-8bb8-0242ac110002', u'130784fc-3894-11eb-b518-328084c04ff8', u'15c9eafe-45b9-11eb-9fde-0242ac110002', u'1dfd11c6-6fca-11ea-a962-0242ac110002', u'1eba8bfa-d7b4-11ea-b9a5-0242ac110002', u'200bde2a-3892-11eb-a240-ae85a3e8b545', u'21c0f828-1e6f-11eb-88bc-ee01faa01328', u'227aaf26-9dd5-11eb-a328-bab06bef90c4', u'271ff9ca-d92b-11e9-888c-0242ac110002', u'28ece92e-1be8-11eb-8f3c-0242ac110002', u'2a7c7ea6-cb36-11ea-b6e8-0242ac110002', u'2ea9adfe-650c-11ea-bd5f-0242ac110002', u'2fc28a8c-db53-11e9-904e-0242ac110002', u'3459ee22-a0bf-11eb-82a9-263fb62c0c20', u'3499ea6e-9164-11eb-a1e5-9651aa804926', u'368072ca-7b35-11eb-b2dc-b258b63f39bb', u'43e2ed5a-6766-11ea-a7ce-0242ac110002', u'4653bac4-311f-11ea-a2e2-0242ac110002', u'486b64c0-75c9-11eb-b15d-a2887cb00478', u'4c91324e-9ccc-11eb-a3a5-5650210ee312', u'4de5bc68-9151-11eb-a1e5-9651aa804926', u'50d6e278-48d9-11eb-b512-0242ac110002', u'59493fc8-a676-11eb-b808-9602cbfa07f9', u'5d3d1f6e-74f3-11eb-a477-824d8deb889f', u'612bd1e6-8629-11eb-97cf-eaa94a9340c5', u'71c53996-3892-11eb-b7b6-eafd1894081f', u'7d82d0f6-8629-11eb-8f08-9e0e86057d5b', u'828f7480-c286-11ea-b707-0242ac110002', u'891bae2a-91f4-11eb-9b5c-eaf65954996e', u'a183ac06-e336-11e9-a9e5-0242ac110002', u'b25ecf08-ca6f-11ea-a47a-0242ac110002', u'b6199cca-914f-11eb-a274-de1bc61eba37', u'b66d6498-68e4-11ea-86ce-0242ac110002', u'b69e8296-e336-11e9-a9e5-0242ac110002', u'bd34ebe0-cb25-11ea-ad09-0242ac110002', u'cd45fdf0-3892-11eb-b20b-0e92233f6a6d', u'd3176fb0-a17f-11eb-802d-3a567f57275f', u'e5c449da-3f96-11eb-b5e7-469c342fc54b', u'eca7f2d6-1e6e-11eb-b9c6-36e694c4446b', u'ecf0caf6-018b-11eb-830c-0242ac110002', u'edea9f64-01f8-11eb-8d68-e26ff08c7e79', u'ee004b02-8c81-11eb-99f8-5a11cc4b85ab', u'fdd042b2-abdb-11ea-b03b-0242ac110002', u'fe55d69c-f0d8-11ea-941d-0242ac110002', u'fe6233cc-75c8-11eb-b15d-a2887cb00478', u'ff7902be-ccf3-11ea-8b52-122153e7696b', u'00aa68ac-001f-11e8-ba18-0242ac110002', u'02079888-32f2-11eb-96a4-0242ac110002']
count = 0
for pipe_id in pipe_list:
    print('开始查询 ： {}'.format(pipe_id))
    query = {"pipe_id": pipe_id, "time": {"$lte": end_time, "$gte": start_time}}
    res_list = list(collection.find(query, {'out_bps': 1, 'in_bps': 1, 'time': 1, '_id': 0}))
    count += len(res_list)

print("MongoDB 查询用时：{} s, 共计查询结果 {} 条".format((datetime.now() - start_at).seconds, count))

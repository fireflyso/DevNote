# -*- coding: utf-8 -*-
import pymongo
from datetime import datetime


MONGO_STR = "mongodb://10.13.226.20:27017/"
MONGO_DB_NAME = "flow_mete"
MONGO_DB_COLLECTION_30S = "flow_data_30s"
MONGO_DB_COLLECTION_1M = "flow_data_1m"
client = pymongo.MongoClient(MONGO_STR)
db = client[MONGO_DB_NAME]
pipe_list = ['1485d36e-306b-11e6-8ecd-0050569b1b91', '23fd84f8-3fc1-11eb-935b-6a26c47a3f1b',
             '4fcefafa-76ee-11e9-811d-0242ac110002', 'f9efdf82-90ab-11e9-8baf-0242ac110002']


def import_data(mongo_conn):
    collection = db[mongo_conn]

    for pipe_id in pipe_list:
        start_time = datetime(2021, 5, 12, 23, 22, 00)
        end_time = datetime(2021, 5, 13, 9, 22, 00)
        # end_time = datetime(2021, 5, 10, 23, 23, 00)
        # res = list(collection.find({'pipe_id': '1edfb184-0a5f-11e8-9330-0242ac110002','time': {'$gt': start_time, '$lt': end_time}}))
        # res = list(collection.find({'pipe_id': pipe_id,'time': {'$gt': start_time, '$lt': end_time}}))
        # print("第一天的数据: {}".format(res))

        res_list = []
        for _ in range(5):
            start_time += datetime.timedelta(days=1)
            end_time += datetime.timedelta(days=1)
            res_data = list(collection.find({'pipe_id': pipe_id, 'time': {'$gt': start_time, '$lt': end_time}}))
            res_list.append(res_data)

        ret = {}
        for res_day in res_list:
            for rd in res_day:
                t = '%s:%s:%s' % (rd['time'].hour, rd['time'].minute, rd['time'].second)
                if t not in ret:
                    ret[t] = {"in_bps": rd["in_bps"], "out_bps": rd["out_bps"], "count": 1}
                else:
                    ret[t]["in_bps"] += rd["in_bps"]
                    ret[t]["out_bps"] += rd["out_bps"]
                    ret[t]["count"] += 1
        fin_ret = []
        for k, v in ret.items():
            if k.startswith("23"):
                t = datetime(year=2021, month=5, day=18, hour=int(k.split(":")[0]), minute=int(k.split(":")[1]),
                             second=int(k.split(":")[2]))
            else:
                t = datetime(year=2021, month=5, day=19, hour=int(k.split(":")[0]), minute=int(k.split(":")[1]),
                             second=int(k.split(":")[2]))
            fin_ret.append({
                "time": t,
                "in_bps": float(format(v["in_bps"] / v["count"], '.3f')),
                "out_bps": float(format(v["out_bps"] / v["count"], '.3f')),
                "pipe_id": pipe_id
            })
        fin_ret = sorted(fin_ret, key=lambda l: l['time'])
        print('-----------', len(fin_ret))
        for i in fin_ret[:10]:
            print(i)
        for i in fin_ret[-10:]:
            print(i)

        # for idx, val in enumerate(res):
        #     in_bps = val['in_bps']
        #     out_bps = val['out_bps']
        #     for res_info in res_list:
        #         # print("时间： {}, in_bps子数据： {}".format(res_info[idx]['time'], res_info[idx]['in_bps']))
        #         # print("时间： {}, out_bps子数据： {}".format(res_info[idx]['time'], res_info[idx]['out_bps']))
        #         in_bps += res_info[idx]['in_bps']
        #         out_bps += res_info[idx]['out_bps']
        #
        #
        #     res[idx]['in_bps'] = format(in_bps/5, '.3f')
        #     res[idx]['out_bps'] = format(out_bps/5, '.3f')
        #     res[idx]['time'] = res[idx]['time'] + datetime.timedelta(days=8)
        #     del res[idx]['_id']
        #     # print("时间： {}, in_bps总和： {}, avg: {}".format(res[idx]['time'], in_bps, format(in_bps/5, '.3f')))
        #     # print("时间： {}, out_bps总和： {}, avg: {}\n".format(res[idx]['time'], out_bps, format(out_bps/5, '.3f')))
        #
        # # print("调整后的数据： {}".formaT(res))
        result = collection.insert_many(fin_ret)
        print(result)


import_data(MONGO_DB_COLLECTION_30S)
import_data(MONGO_DB_COLLECTION_1M)

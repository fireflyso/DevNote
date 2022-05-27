# -*- coding: utf-8 -*-
"""
2021年07月25日需求：为pipe补充5分钟计量缺失数据
脚本执行路径：/data/mongo
"""
import pymongo
from datetime import datetime, timedelta

MONGO_DB_COLLECTION_30S = {
    'mongo_str': 'mongodb://10.13.226.20:27017/',
    'db': 'flow_mete',
    'conn_name': "flow_data_30s",
    'time': 30
}
MONGO_DB_COLLECTION_1M = {
    'mongo_str': 'mongodb://10.13.226.20:27017/',
    'db': 'flow_mete',
    'conn_name': "flow_data_1m",
    'time': 60
}

MONGO_DB_COLLECTION = {
    'mongo_str': 'mongodb://10.13.2.111:27017,10.13.2.112:27017/flow_snmp',
    'db': 'flow_snmp',
    'conn_name': "flow_data",
    'time': 300
}

pipe_list = ['f9efdf82-90ab-11e9-8baf-0242ac110002', '1485d36e-306b-11e6-8ecd-0050569b1b91', '23fd84f8-3fc1-11eb-935b-6a26c47a3f1b', '4fcefafa-76ee-11e9-811d-0242ac110002']


def add_data(conn_info, pipe_id):
    """通过start_time开始自动查找需要补充的数据节点，并取出前一周对应时间节点上的流量数据进行补充

    Args:
        db_name ([type]): [description]
        conn ([type]): [description]
        pipe_id ([type]): [description]
    """
    client = pymongo.MongoClient(conn_info.get('mongo_str'))
    db = client[conn_info.get('db')]
    collection = db[conn_info.get('conn_name')]

    start_time = datetime(2021, 7, 22, 17, 00, 00)
    # 获取指定时间之后的第一个计量数据信息（指定的时间不一定是计量时间节点）
    res_data = list(collection.find({'pipe_id': pipe_id, 'time': {"$gte": start_time}}).sort(
        "time", pymongo.ASCENDING).limit(1))

    if not res_data:
        print("MongoDB中没有找到pipe ： {} ,在 {} 之后的任何数据，请检查数据！".format(pipe_id, start_time))
        return

    # 将指定时间之后的第一组计量数据作为起点开始进行数据检查
    start_time = res_data[0].get('time')

    time_interval = conn_info.get('time')
    next_time = start_time + timedelta(seconds=time_interval)
    end_time = datetime.now()
    while next_time < end_time:
        res_data = list(collection.find({'pipe_id': pipe_id, 'time': next_time}).limit(1))
        if not res_data:
            res_data = list(collection.find({'pipe_id': pipe_id, 'time': {"$gte": next_time}}).sort(
                "time", pymongo.ASCENDING).limit(1))
            if res_data:
                end_time = res_data[0].get('time')

            print('pipe : {} ,从 {} 到 {} 区间的计量缺失需要补充'.format(pipe_id, next_time, end_time))
            break

        next_time += timedelta(seconds=time_interval)

    # 开始补充next_time到end_time之间的数据
    data_list = []
    while next_time < end_time:
        time_list = [next_time + timedelta(days=0-index) for index in range(1, 8)]
        flow_list = list(collection.find(
            {'pipe_id': pipe_id, 'time': {'$in': time_list}}, {'out_bps': 1, 'in_bps': 1, 'time': 1, '_id': 0}))

        if not res_data:
            print("pipe ： {} 找不到历史计量数据 : {}".format(pipe_id, time_list))
            break

        out_bps_total = 0
        in_bps_total = 0
        for flow in flow_list:
            out_bps_total += flow.get('out_bps')
            in_bps_total += flow.get('in_bps')

        # print("pipe : {}, 历史数据为 : {}".format(pipe_id, flow_list))

        in_bps = float(format(in_bps_total / len(flow_list), '.3f'))
        out_bps = float(format(out_bps_total / len(flow_list), '.3f'))
        data_list.append({
            "time": next_time,
            "in_bps": in_bps,
            "out_bps": out_bps,
            "pipe_id": pipe_id
        })
        # print("pipe : {} time : {} 计算完成 in : {}, out : {}".format(pipe_id, next_time, in_bps, out_bps))
        # print("pipe : {} time : {} 数据为 in : {}, out : {}\n".format(pipe_id, flow_list[0].get('time'), flow_list[0].get('in_bps'), flow_list[0].get('out_bps')))
        next_time += timedelta(seconds=time_interval)

    data_list = sorted(data_list, key=lambda l: l['time'])
    print('pipe : {} 将会补充 {} 组数据!'.format(pipe_id, len(data_list)))
    # result = collection.insert_many(data_list)
    # print("pipe : {} insert res : {}".format(pipe_id, len(result.inserted_ids)))


for pipe_id in pipe_list:
    add_data(MONGO_DB_COLLECTION, pipe_id)


"""  
2021-07-25 18:06:35执行结果：
pipe : 1485d36e-306b-11e6-8ecd-0050569b1b91 ,从 2021-07-22 17:24:35 到 2021-07-24 00:05:44 区间的计量缺失需要补充
pipe : 1485d36e-306b-11e6-8ecd-0050569b1b91 将会补充 369 组数据!
pipe : 1485d36e-306b-11e6-8ecd-0050569b1b91 insert res : <pymongo.results.InsertManyResult object at 0x7fbd32354e60>
pipe : 23fd84f8-3fc1-11eb-935b-6a26c47a3f1b ,从 2021-07-23 14:19:35 到 2021-07-24 00:05:44 区间的计量缺失需要补充
pipe : 23fd84f8-3fc1-11eb-935b-6a26c47a3f1b 将会补充 118 组数据!
pipe : 23fd84f8-3fc1-11eb-935b-6a26c47a3f1b insert res : <pymongo.results.InsertManyResult object at 0x7fbd32354e60>
pipe : 4fcefafa-76ee-11e9-811d-0242ac110002 ,从 2021-07-23 14:19:35 到 2021-07-24 00:05:44 区间的计量缺失需要补充
pipe : 4fcefafa-76ee-11e9-811d-0242ac110002 将会补充 118 组数据!
pipe : 4fcefafa-76ee-11e9-811d-0242ac110002 insert res : <pymongo.results.InsertManyResult object at 0x7fbd32354f50>
pipe : f9efdf82-90ab-11e9-8baf-0242ac110002 ,从 2021-07-23 02:04:35 到 2021-07-24 00:05:44 区间的计量缺失需要补充
pipe : f9efdf82-90ab-11e9-8baf-0242ac110002 将会补充 265 组数据!
pipe : f9efdf82-90ab-11e9-8baf-0242ac110002 insert res : <pymongo.results.InsertManyResult object at 0x7fbd32354f50>
"""


# -*- coding: utf-8 -*-
"""
2021年07月25日需求：为pipe补充5分钟计量缺失数据
脚本执行路径：/data/mongo
"""
import pymongo
from datetime import datetime, timedelta
import utils_logger

logger = utils_logger.get_logger('test')

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
FLOW_TABLE_NAME = "flow_data_local_new"

# with open("pipes.txt") as file:
#     pipe_list = [item.replace('\n', '') for item in file]
pipe_list = ['02a533ba-63f5-11ec-81f0-6ae2afe11c1c','0dfcc7e4-00c9-11ec-bbc6-42e686a712e2','12958824-f4ee-11e9-8bb8-0242ac110002','1b76ce66-b257-11ec-8ea0-829efbb011f7','1db3f74c-8d74-11ec-9ec0-e611aa3f142c','1eba8bfa-d7b4-11ea-b9a5-0242ac110002','271ff9ca-d92b-11e9-888c-0242ac110002','28ece92e-1be8-11eb-8f3c-0242ac110002','2fc28a8c-db53-11e9-904e-0242ac110002','3499ea6e-9164-11eb-a1e5-9651aa804926','35f90b9a-7527-11ec-bee9-1ef2df7c7a9d','382c3d36-dbea-11ec-ad88-eefc54e3be1e','4280c40a-6015-11ed-add2-0e8a407a24fa','4653bac4-311f-11ea-a2e2-0242ac110002','4c91324e-9ccc-11eb-a3a5-5650210ee312','50b037fc-6af8-11ed-9a91-2e9d76359266','612bd1e6-8629-11eb-97cf-eaa94a9340c5','7d82d0f6-8629-11eb-8f08-9e0e86057d5b','8157058e-88a9-11ec-8028-cea1757a60a8','a183ac06-e336-11e9-a9e5-0242ac110002','a80d08d0-c87e-11ec-99c8-5e1b35c7b1eb','aa8aa760-ded3-11eb-81f5-0a451bcb0c0c','b66d6498-68e4-11ea-86ce-0242ac110002','b69e8296-e336-11e9-a9e5-0242ac110002','bb9c569a-6252-11ec-bdd3-2e8cb5685b8f','bd34ebe0-cb25-11ea-ad09-0242ac110002','c023aa0a-3fc5-11ed-bdf5-8ae2e7dbd103','c12ed956-421e-11ec-bd38-9e6560e0aaae','cba5a7a8-5f36-11ed-a6a2-122f5a1fca60','ecf0caf6-018b-11eb-830c-0242ac110002','f49dd1e6-c809-11eb-97e6-1e87532ba5d2','f80532d6-6bbc-11ed-b0c9-3687119db6b3','fe55d69c-f0d8-11ea-941d-0242ac110002']
logger.info('pipe list len : {}'.format(len(pipe_list)))


def add_data(conn_info, pipe_id):
    """通过start_time开始自动查找需要补充的数据节点，并取出前一周对应时间节点上的流量数据进行补充

    Args:
        db_name ([type]): [description]
        conn ([type]): [description]
        pipe_id ([type]): [description]
    """
    from clickhouse_driver import Client
    CK_HOST = "10.13.133.135"
    CK_USER = "flowdata"
    CK_PASSWORD = "wVen6RK3KpkpGdsA"
    CK_DB_ANME = "flow_snmp"
    CK_PORT = 9000
    ck_client = Client(host=CK_HOST, port=CK_PORT, user=CK_USER, password=CK_PASSWORD)


    client = pymongo.MongoClient(conn_info.get('mongo_str'))
    db = client[conn_info.get('db')]
    collection = db[conn_info.get('conn_name')]

    start_time = datetime(2022, 11, 25, 8, 00, 00)
    end_time = datetime(2022, 11, 25, 19, 00, 00)
    # 获取指定时间之后的第一个计量数据信息（指定的时间不一定是计量时间节点）
    res_data = list(collection.find({'pipe_id': pipe_id, 'time': {"$gte": start_time}}).sort(
        "time", pymongo.ASCENDING).limit(1))

    if not res_data:
        logger.info("MongoDB中没有找到pipe ： {} ,在 {} 之后的任何数据，请检查数据！".format(pipe_id, start_time))
        return

    # 将指定时间之后的第一组计量数据作为起点开始进行数据检查
    start_time = res_data[0].get('time')

    time_interval = conn_info.get('time')
    next_time = start_time
    fix_list = []
    while next_time < end_time:
        res_data = list(collection.find({'pipe_id': pipe_id, 'time': {
            "$gt": next_time,
            "$lte": next_time + timedelta(seconds=time_interval)
        }}).limit(1))
        if not res_data:
            res_data = list(collection.find({'pipe_id': pipe_id, 'time': {"$gt": next_time}}).sort(
                "time", pymongo.ASCENDING).limit(1))
            if res_data:
                temp_time = res_data[0].get('time')

            logger.info('pipe : {} ,从 {} 到 {} 区间的计量缺失需要补充'.format(pipe_id, next_time, temp_time))
            fix_list.append((next_time, temp_time))
            next_time = temp_time
            continue

        next_time += timedelta(seconds=time_interval)

    # 开始补充next_time到end_time之间的数据
    mongo_data_list = []
    ck_data_list = []
    for fix in fix_list:
        next_time = fix[0] + timedelta(seconds=time_interval)
        end_time = fix[1]
        while next_time < end_time:
            time_list = [next_time + timedelta(days=0-index) for index in range(1, 8)]
            flow_list = list(collection.find(
                {'pipe_id': pipe_id, 'time': {'$in': time_list}}, {'out_bps': 1, 'in_bps': 1, 'time': 1, '_id': 0}))

            if not flow_list:
                logger.info("pipe : {} 找不到历史计量数据 : {}".format(pipe_id, next_time))
                next_time += timedelta(seconds=time_interval)
                continue

            out_bps_total = 0
            in_bps_total = 0
            for flow in flow_list:
                out_bps_total += flow.get('out_bps')
                in_bps_total += flow.get('in_bps')

            # logger.info("pipe : {}, 历史数据为 : {}".format(pipe_id, flow_list))

            in_bps = float(format(in_bps_total / len(flow_list), '.3f'))
            out_bps = float(format(out_bps_total / len(flow_list), '.3f'))
            mongo_data_list.append({
                "time": next_time,
                "in_bps": in_bps,
                "out_bps": out_bps,
                "pipe_id": pipe_id
            })
            ck_data_list.append([pipe_id, next_time, in_bps, out_bps])
            # logger.info("pipe : {} time : {} 计算完成 in : {}, out : {}".format(pipe_id, next_time, in_bps, out_bps))
            # logger.info("pipe : {} time : {} 数据为 in : {}, out : {}\n".format(pipe_id, flow_list[0].get('time'), flow_list[0].get('in_bps'), flow_list[0].get('out_bps')))
            next_time += timedelta(seconds=time_interval)

        if mongo_data_list:
            count = (fix[1] - fix[0]).seconds/300 + 1
            logger.info('pipe : {} 应该补充 {} 组数据，实际会补充 {} 组数据, 时间区间 ： {} - {}!'.format(
                pipe_id, count, len(mongo_data_list), fix[0], fix[1]))

            # logger.info('pipe : {} 将会补充 {} 组数据, 截止时间为 ： {}!'.format(pipe_id, len(mongo_data_list), mongo_data_list[-1].get('time')))
            insert_sql = f"insert into {CK_DB_ANME}.{FLOW_TABLE_NAME} (pipe_id, time, in_bps, out_bps) VALUES"
            ck_client.execute(insert_sql, ck_data_list)
            result = collection.insert_many(mongo_data_list)
            logger.info("pipe : {} insert res : {}".format(pipe_id, len(result.inserted_ids)))
            ck_data_list = []
            mongo_data_list = []

    # insert_sql = f"insert into {CK_DB_ANME}.{FLOW_TABLE_NAME} (pipe_id, time, in_bps, out_bps) VALUES"
    # ck_client.execute(insert_sql, ck_data_list)
    # result = collection.insert_many(mongo_data_list)
    # logger.info("pipe : {} insert res : {}".format(pipe_id, len(result.inserted_ids)))
    ck_client.disconnect()



for pipe_id in pipe_list:
    add_data(MONGO_DB_COLLECTION, pipe_id)

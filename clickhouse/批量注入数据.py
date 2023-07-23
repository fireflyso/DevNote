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

pipe_list = ['d9641931-2ca3-4940-9100-b31f5459130a']
logger.info('pipe list len : {}'.format(len(pipe_list)))

from clickhouse_driver import Client
CK_HOST = "10.13.133.135"
CK_USER = "flowdata"
CK_PASSWORD = "wVen6RK3KpkpGdsA"
CK_DB_ANME = "flow_snmp"
CK_PORT = 9000
ck_client = Client(host=CK_HOST, port=CK_PORT, user=CK_USER, password=CK_PASSWORD)

client = pymongo.MongoClient(MONGO_DB_COLLECTION.get('mongo_str'))
db = client[MONGO_DB_COLLECTION.get('db')]
collection = db[MONGO_DB_COLLECTION.get('conn_name')]


def add_data(pipe_id):
    """通过start_time开始自动查找需要补充的数据节点，并取出前一周对应时间节点上的流量数据进行补充

    Args:
        db_name ([type]): [description]
        conn ([type]): [description]
        pipe_id ([type]): [description]
    """
    logger.info('开始处理pipe : {}'.format(pipe_id))
    start_time = datetime(2023, 11, 1, 00, 00, 00)
    end_time = datetime(2028, 7, 1, 00, 00, 00)
    next_time = start_time
    mongo_data_list = []
    ck_data_list = []
    while next_time < end_time:
        in_bps = float(0)
        out_bps = float(0)
        mongo_data_list.append({
            "time": next_time,
            "in_bps": in_bps,
            "out_bps": out_bps,
            "pipe_id": pipe_id
        })
        ck_data_list.append([pipe_id, next_time, in_bps, out_bps])
        next_time += timedelta(seconds=300)

        if len(mongo_data_list) > 1000:
            insert_sql = f"insert into {CK_DB_ANME}.{FLOW_TABLE_NAME} (pipe_id, time, in_bps, out_bps) VALUES"
            ck_client.execute(insert_sql, ck_data_list)

            result = collection.insert_many(mongo_data_list)
            logger.info("pipe : {} insert res : {}".format(pipe_id, len(result.inserted_ids)))
            logger.info("next_time : {}".format(next_time))
            ck_data_list = []
            mongo_data_list = []


for pipe_id in pipe_list:
    add_data(pipe_id)

ck_client.disconnect()

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
pipe_list = ['c5eddf08-d086-11ed-b7cc-1eda3381ec65', 'e71d0d0c-d086-11ed-a881-46aa502f5daf', '1cf130cc-660a-11e7-bab8-0242ac110002', '3501c516-9be4-11e9-8812-0242ac110002', '4fb49b62-dd39-11ea-b9c0-0242ac110002', '7a88cd1a-29ca-11ed-8967-8ef9009614ee', '8b10b378-6272-11e9-9773-0242ac110002', '33a4fe9c-82a6-11e9-96d2-0242ac110002', '0ac0492e-1d49-11e7-ac87-0242ac110002', '9fd88912-b668-11e9-a140-0242ac110002', 'fc31340e-2222-11ea-9c39-0242ac110002', '650e252e-2794-11ea-b513-0242ac110002', '078cf6da-500e-11ea-8a95-0242ac110002', '77cba178-bc83-11e8-b056-0242ac110002', '24f1eb20-6ce4-11ea-bf7f-0242ac110002', 'f003a22c-6ff5-11ea-b971-0242ac110002', 'fa7feb10-7965-11ea-a080-0242ac110002', '59f736f4-9c00-11ea-a783-f206082eadb4', '7fd7bf50-d095-11ea-b4bc-0242ac110002', 'f2074ffa-dc61-11ea-a6ce-0242ac110002', 'ea3f2c9e-dd50-11ea-ac81-0242ac110002', '4265de10-6a94-11e6-a7fa-0242ac102160', '498d303e-225b-11eb-b723-0242ac110002', 'cc0e4d46-a421-11e8-b5d8-0242ac1100fb', '4db0c620-54f0-11e8-96e9-0242ac110002', 'f025b2b4-38f8-11eb-9511-9a8cda111679', '7464ce76-1774-11eb-b5ec-0242ac110002', '862af69a-5288-11eb-b039-7a571d7813a7', 'f2494fae-6474-11eb-8570-c288d273374c', '014d0b70-65e3-11eb-8570-c288d273374c', '9299945a-75af-11eb-ac69-869a7f8fc36f', '548e03e6-7c92-11eb-97cf-eaa94a9340c5', '3934fe82-83e1-11eb-97cf-eaa94a9340c5', '32fba51c-252c-11ea-a04e-0242ac110002', 'd64354d8-8861-11eb-8f08-9e0e86057d5b', 'e5e1fc8c-aa6a-11e8-84f2-0242ac110002', 'bc663ac6-aa6a-11e8-ad79-0242ac110002', 'ef09e33a-7e1a-11ea-99df-0242ac110002', '5d78ad44-aa67-11e8-a813-0242ac110002', '4cde84e0-aa67-11e8-b5e4-0242ac110002', '046162be-aa67-11e8-88ef-0242ac110002', 'f98f6148-aa6a-11e8-b54b-0242ac110002', '54fcb148-b6b6-11eb-9523-66b53a7ef3ab', 'e0ccf044-b8bb-11ed-a330-de1854b7af6c', '6654239c-b4c8-11ed-9eaf-8aa26b983c79', 'dee6204e-b5c2-11ed-b160-4e37d05f2ceb', '1cbaef00-b968-11ed-8854-c2ec58d888d8', '944f692a-ba48-11ed-a920-eeb5f693549e', '252ada64-be4b-11ed-821f-f65be369b593', 'c19d7138-ec49-11ec-84a7-c645ac6efaf0', '4f072d44-b229-11ec-8cf6-dee884356195', '1e8633a8-2a66-11ed-9be2-7a4d1b50eb70', '4de911d2-5ccc-11ec-90e9-3260887fa0d0', 'f929eafa-82e7-11ea-8c7d-0242ac110002', '2f1e8606-8438-11ea-bfa7-0242ac110002', 'f3194aa4-46d8-11ed-a22b-ba45f0c8136b', 'f0185fc4-a8e5-11ed-b19f-12edbc9dde8a', '8b1ea066-2419-11ed-8450-56f56f661a52', '7f638198-fbf2-11ea-9a8a-5ec6077c2d44', '3bed6f50-c30a-11ed-bdfc-aa5b09f00e64', '46dbfdda-2834-11ed-9be2-7a4d1b50eb70', '7033c6d6-1c63-11ed-9649-dac151a667eb', '58057e86-0d5b-11ed-b153-3295b654f4a1', '4debb174-fc29-11ec-8409-32d5a887c781', '62eb5432-d28d-11ec-9ed2-7a1ff6496884', '88dbd072-45c0-11ec-a3ee-46d2623fca4b', '1d5a2960-8161-11ed-86bb-5ace9107494d', '03532432-8165-11ed-a4df-a2e95ee32ffd', 'f4f9664e-8164-11ed-b59c-4229750f9d0c', '1704ff46-8165-11ed-86bb-5ace9107494d', '3508e1fa-8161-11ed-8b48-1aa04e16007a', 'ec0db9d8-8158-11ed-89b5-760fae1110e3', 'a06cbdb4-8160-11ed-8b48-1aa04e16007a', 'b06df0c0-d421-11ed-ae87-d67bba1e5d0e', 'e94da578-6f97-11ed-a9fe-2297c76c4e4d', '28430d28-d531-11ed-8868-1e0200e1da37', '1232938e-d5e8-11ed-b7cc-1eda3381ec65', '2eff5384-da99-11ed-8a1b-ae483e53749c', '6d979c0c-ddad-11ed-827c-7a736ff4bdeb', '4f53d3c2-45c0-11ec-8cca-f61f6759ac3c', 'cdc7a43c-fcd0-11ec-a50e-e2541fddabbe', 'c4b01bac-e4ad-11ed-a626-02f0daf5ea89', 'bbf7acb4-eee4-11ed-84e2-4afb93dc55b6', '6248e132-f48f-11ed-84e2-4afb93dc55b6', '5fbef798-f86e-11ed-b33a-66538039aae2', 'a86a159e-e686-11ed-8dd4-b68111c315ad', '18ede74a-6863-11e6-92ad-0242ac100602', 'f18747e2-e253-11ed-9253-42081e6cc1c6', '6f2038c8-fba2-11ed-b7de-fe2dad5de2ca', '6a465dc0-fde4-11ed-897b-6a6fa8c8be77', 'df3bfed0-ff8f-11ed-af70-4aae3864723e', 'd9eda202-fb99-11ed-b7de-fe2dad5de2ca', 'b666a5ec-06a5-11ee-8980-9215d2647d01', 'b9cfeef4-fdc8-11ed-a4aa-e27800858960', '59989d76-0906-11ee-a019-1e8f3b7b400a', '2da3beaa-0e7c-11ee-a076-4e004f8e3663', 'e43b9a12-13d0-11ee-a076-4e004f8e3663', 'aea919fa-1575-11ee-9f44-b2fd376f4652', '710666f2-803d-11ed-b0c2-8eae3fce7e41', '4bdf0b58-afff-11ed-b0a1-2ac4a78e9e4b', '61618bda-d468-11ed-91aa-0aa2801fde7c', '3d46fd9a-7a54-11eb-a38f-da9cc3b792d7', 'bd2dd3d8-fa80-11eb-97f5-562e7f031744', 'd7187c92-de35-11eb-af9f-ea07a495bb82', '9f598ee4-c365-11eb-9925-d65d5621190c', 'c400d490-82ad-11ea-8ed6-0242ac110002', '472362aa-efbc-11e9-8ecc-0242ac110002', 'c9a44948-047c-11ec-b6d7-7e710254e7b9', '9bc90c00-21a7-11ec-a3f6-8ed5add65b67', '0a737ede-1730-11eb-a2f0-56bc7cc20f3e', 'fa04898a-32db-11ec-be89-32f298f4feb1', 'ab35a708-24d1-11eb-a010-0242ac110002', 'cc8450a0-a1e6-11e8-808c-0242ac110002', 'd84efa8c-defc-11e7-b329-0242ac110002', 'c04f4260-caac-11e8-9d82-0242ac110002', 'b668cb48-24d4-11eb-8d36-0242ac110002', '5b858bec-24d1-11eb-8b99-0242ac110002', 'e30b3c4a-24d3-11eb-b3fd-0242ac110002', '121edc18-d1d8-11e8-9d69-0242ac110002', '0b6ccc12-24d4-11eb-82cc-0242ac110002', '43aa27d0-ed65-11e8-bd2e-0242ac110002', '9bf3b818-a1ee-11ea-aa7a-9a374888fa2d', '6eb32f40-4262-11e6-ad40-0050569b1b91', '3f418388-5d78-11ec-af74-1a18b172d239', '84a6385c-5ee9-11ec-b21f-4e2f023009ad', '649b13ac-5bc4-11ec-a2f3-5a154554716b', 'e997920e-ba73-11ea-a03b-0242ac110002', 'f5045586-45bf-11ec-8a31-721b06e4bfff', '2f9d63e2-b90b-11ea-a89f-0242ac110002', 'd5e44cf4-1e11-11e7-87e3-0242ac110002', '8c0be10c-7853-11e9-9b6c-0242ac110002', 'b5c01c5e-c5f6-11ec-ba64-76d2d671f151', '3532a8d6-ba39-11ec-856e-b27a12bc8f2e', '444d482e-cc65-11ec-8149-66123e3d7735', '24d56e0a-4033-11eb-b1cd-0242ac110002', '753cb55c-4b35-11ec-964b-dab0cc25944f', 'b1093d98-a5bd-11ec-9d9e-52194df22c9a', 'f7ee30e6-d4da-11ec-9699-c660f872a1f9', '3f1d1a86-eb29-11ec-996c-c605a3fd97ae', 'ef52ee28-0332-11ed-b5e1-267269b7a323', 'a3a29248-0d74-11ed-93da-c67802f9b99a', '3926c9de-b5ad-11e8-8733-0242ac110002', '8cdcd87a-22b8-11e9-9952-0242ac110002', '017463b4-e25a-11e8-9eee-0242ac110002', 'f78e6368-b5c7-11e8-887e-0242ac110002', 'c52cab18-a1ca-11eb-b6cc-b6b1d2df5ac3', 'bf1328fa-1d36-11e7-87e3-0242ac110002', 'bd4e1b08-14a4-11e9-aa8e-0242ac110002', '02a6485a-a1de-11e7-a6fc-0242ac110002', '039dd126-299f-11ed-91ee-ea4cc8b6801c', 'd575ebec-294d-11eb-9843-0242ac110002', 'da8125fc-259a-11e8-af9e-0242ac110002', 'fa09cbba-ae6f-11e7-b528-0242ac110002', 'b88eb712-1aee-11e9-b060-0242ac110002', 'b757bfe0-9e7d-11e7-a798-0242ac110002', '19ce885a-22a6-11e8-a2af-0242ac110002', '419fd706-259b-11e8-a1eb-0242ac110002', 'ca5e3d38-185a-11ed-8286-caa164d3e4cb', '1aaf681a-3337-11ed-80c4-0687bc0e9967', '3740b4bc-3412-11ed-80c4-0687bc0e9967', '6f2b85dc-4862-11ed-8fdd-063f067542bd', '9a033034-4862-11ed-900d-8a38819db1db', '2c21cf1c-486c-11ed-939d-1a6c52be81d3', '490633ec-4d09-11ed-8c83-a2fac1c05eb5', '09d9f04c-4d0d-11ed-bf09-06d909c35ff0', 'cf340128-4d14-11ed-8b40-a67130f7a09f', '02854370-4d15-11ed-8c83-a2fac1c05eb5', '85e3f104-945f-11e7-957a-0242ac110002', 'a6aefc62-ef86-11e7-8795-0242ac110002', '338b03ba-c39f-11e7-815a-0242ac110002', '9bf56498-51d6-11ed-8b40-a67130f7a09f', '0c67eba4-e0a5-11ec-a976-0ac79e7a7add', '0a70b4b0-405b-11ec-bc4e-46a9583b1631', '196c7636-3bc7-11ec-9222-825f3d08345c', '1f4e22e8-3bc7-11ec-8e29-ba6016034d9c', '44e67038-7500-11ec-8618-02622ce0b4ee', '4d03e0f6-3bc7-11ec-8e29-ba6016034d9c', '3fd99294-3bc8-11ec-9a67-52fe0c1638a7', '6e1d676c-3bc7-11ec-95ee-c61b40fbb02d', 'e5dd2ba6-405a-11ec-9d61-0a37c67934a4', 'db0a3298-4aa2-11ed-9e6c-125755bee9e0', '247628ee-6711-11ed-895b-3ab56b140780', '5444c33c-75d5-11ed-bd35-76d3548cdb9b', '632d66fe-7abe-11ed-9fcb-1ad50f9d99b5', 'dc8707b4-81a6-11ed-a7b3-b602b0a62ebb', 'fbf4e478-483e-11ed-88df-4669407ff986', 'f700b190-8d8f-11ed-a00f-e6bc8c4ebe17', '9fbc6b6c-ba37-11ec-8518-8a1fe6614947', '8a48ac3c-992b-11ec-802d-72f37e1c83f3', 'ea94bca8-8fbf-11ed-aded-b635a9fce096', 'f16c04e2-9f91-11ec-b69c-029fc8c1ad04', 'ff8bcd70-8fbc-11ed-9ceb-ea0ed99f2599', '5e4d1de4-a39c-11ed-993b-02b309726a99', '4674f9a0-a75a-11ed-83d3-12853257c7c9', '8af1498a-ace1-11ed-8124-6eecfdbe78d2', 'e491137a-172f-11eb-b9f8-5636e21bb209', '78be05c4-b32a-11ed-93b7-16d8176a224c', 'f88b7d3a-b330-11ed-93b7-16d8176a224c', 'adef470e-cd33-11e7-b0c5-0242ac110002', 'fb444086-92e6-4a57-9c0c-2740c109c8e6', 'a899d09c-f5ee-11e7-b540-0242ac110002', '7e7851e0-f516-11e7-b680-0242ac110002', 'fd3ed1e4-8160-11ed-89b5-760fae1110e3', '06714764-d531-11ed-8b60-226bcf6660ce', '5f1acc2c-b7ff-11ed-8287-f67d46aa43f8', '5e90b25c-f54a-11ed-9bbb-6ad6717282d4', '3012eefa-ef09-11ed-89e1-a2a9a35533a5', '50888fd0-be4b-11ed-b290-9ec5a008b636', '2f4a86e2-c968-11e9-a13c-0242ac110002', 'add4b98e-050d-11ea-96d0-0242ac110002', '375ef6fe-24f8-11e7-87e3-0242ac110002']
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

    start_time = datetime(2023, 7, 3, 6, 00, 00)
    end_time = datetime(2023, 7, 3, 20, 00, 00)
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
    temp_time = end_time
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

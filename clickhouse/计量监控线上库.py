from clickhouse_driver import Client

CK_HOST = "10.13.133.135"
CK_USER = "flowdata"
CK_PASSWORD = "wVen6RK3KpkpGdsA"
CK_DB_ANME = "flow_snmp"
CK_PORT = 9000
client = Client(host=CK_HOST, port=CK_PORT, user=CK_USER, password=CK_PASSWORD)

client.execute("SELECT time, in_bps, out_bps FROM flow_snmp.flow_data_first_all where pipe_id  = '6c6d7e6a-2375-11e9-9cc0-0242ac110002' and time >= '2021-06-30 12:30:00' and time <= '2021-06-30 16:55:00' order by time")


sql = "CREATE TABLE flow_snmp.flow_data_local_new_second (`pipe_id` String,`time` DateTime,`in_flow` Float64,`out_flow` Float64,`in_bps` Float64,`out_bps` Float64) ENGINE=Log"
ans = client.execute(sql)

client.execute("SHOW TABLES FROM  flow_snmp")
client.execute("SHOW databases")
client.execute("SHOW GRANTS")
client.execute("SELECT * FROM system.clusters")

client.execute("SELECT time, in_bps, out_bps FROM flow_snmp.flow_data where pipe_id  = '3a9a9ff8-b710-11ec-9bfc-8252cbfa8cce' and time >= '2022-04-13 17:45:01' and time < '2022-04-13 17:46:01' order by time")
# 查看表中数据条数以及空间占用情况
client.execute("SELECT sum(rows), formatReadableSize(sum(data_uncompressed_bytes)), formatReadableSize(sum(data_compressed_bytes)) from system.parts WHERE (database IN ('flow_snmp')) AND (table IN ('flow_data_local_new'))")
client.execute("SELECT pipe_id from flow_snmp.flow_data_local_new where time > '2021-05-01 12:00:00' order by time limit 50")
client.execute("SELECT pipe_id, COUNT(pipe_id) FROM flow_snmp.flow_data_local_new where time > '2021-07-06 11:00:00' group by pipe_id")
client.execute("SELECT pipe_id, COUNT(pipe_id) FROM flow_snmp.flow_data_local_new where time > '2020-10-06 11:00:00' and time > '2020-10-06 12:00:00' group by pipe_id")
client.execute("SHOW CREATE flow_snmp.flow_data_local_new")
client.execute("SELECT time, in_bps, out_bps from flow_snmp.flow_data WHERE pipe_id  = '06be7cce-c55d-11e9-82db-0242ac110002' and time > '2021-06-06 12:30:00' and time < '2021-07-06 12:30:00' order by time")

client.execute("select partition, sum(rows), formatReadableSize(sum(data_uncompressed_bytes)) from system.parts where table = 'flow_data_first_local' GROUP BY partition")
client.execute("select formatReadableSize(sum(data_uncompressed_bytes)), formatReadableSize(sum(data_compressed_bytes)) from system.parts where table = 'flow_data_local_new'")

client.execute("select count(*) from flow_snmp.flow_data")
client.execute("select count(*) from flow_snmp.flow_data_second_all")
client.execute("select count(*) from flow_snmp.flow_data_local_new")
client.execute("SELECT time, in_bps, out_bps FROM flow_snmp.flow_data_first_all where pipe_id  = '6c6d7e6a-2375-11e9-9cc0-0242ac110002' and time >= '2021-06-30 12:30:00' and time <= '2021-06-30 16:55:00' order by time")
client.execute("SELECT PARTITION,sum(rows),formatReadableSize (sum(data_uncompressed_bytes)),formatReadableSize (sum(data_compressed_bytes)) FROM system.parts WHERE (DATABASE IN ('flow_snmp')) AND (TABLE IN ('flow_data_first_local01')) GROUP BY PARTITION ORDER BY PARTITION ASC")


# 线上新建表结构
client.execute("CREATE TABLE flow_snmp.flow_data_first_local ON CLUSTER cluster_1shards_3replicas (`pipe_id` UUID,`time` DateTime,`in_flow` Float64,`out_flow` Float64,`in_bps` Float64,`out_bps` Float64) ENGINE=ReplicatedMergeTree ('/clickhouse/tables/{shard}/flow_data_first_local','{replica}') PARTITION BY toYYYYMM (time) ORDER BY (pipe_id,time) SETTINGS index_granularity=8192")
client.execute("CREATE TABLE flow_snmp.flow_data_first_all ON CLUSTER cluster_1shards_3replicas AS flow_snmp.flow_data_first_local ENGINE=Distributed ('cluster_1shards_3replicas','flow_snmp','flow_data_first_local',rand())")
client.execute("CREATE TABLE flow_snmp.flow_data_second_local ON CLUSTER cluster_1shards_3replicas (`pipe_id` UUID,`time` DateTime,`in_flow` Float64,`out_flow` Float64,`in_bps` Float64,`out_bps` Float64) ENGINE=ReplicatedMergeTree ('/clickhouse/tables/{shard}/flow_data_second_local','{replica}') PARTITION BY toYYYYMM (time) ORDER BY (pipe_id,time) SETTINGS index_granularity=8192")
client.execute("CREATE TABLE flow_snmp.flow_data_second_all ON CLUSTER cluster_1shards_3replicas AS flow_snmp.flow_data_second_local ENGINE=Distributed ('cluster_1shards_3replicas','flow_snmp','flow_data_second_local',rand())")

client.execute("INSERT INTO flow_snmp.flow_data_second_local (pipe_id, `time`, in_flow, out_flow, in_bps, out_bps) VALUES('e44bc7aa-6f6e-11ec-a6a9-b240c10b0009', '2021-07-05 15:55:00', 32674.0, 0.0, 0.0, 1.0)")
client.execute("select count(*) from flow_snmp.flow_data ")
client.execute("select * from flow_snmp.flow_data where pipe_id = '30aa2a22-0653-11ec-9ca9-0a0d265d6421' and time < '2022-07-01 11:00:00' order by time desc limit 3")
client.execute("select * from flow_snmp.flow_data where pipe_id = '06fc21a8-fc48-11ec-aa28-563722c44a2c' order by time desc limit 3")

client.execute("show create table flow_snmp.flow_data")
client.execute("SELECT * from flow_snmp.flow_data where pipe_id = '8a727b4c-3540-11ec-ab9c-ea82af98404f' and time > '2021-10-31 11:00:00' and time < '2021-10-31 12:00:00'")
# client.execute("ALTER TABLE flow_snmp.flow_data_first_local DROP PARTITION '202107'")
client.execute("select partition, sum(rows), formatReadableSize(sum(data_uncompressed_bytes)) from system.parts where table = 'flow_data_local_new' GROUP BY partition")
# client.execute("DROP TABLE flow_snmp.flow_data_first_local01 ON CLUSTER cluster_1shards_3replicas")


client.execute("select distinct pipe_id from flow_snmp.flow_data where time > '2022-08-12 00:00:00' and time < '2022-08-12 01:00:00'")
client.execute("select pipe_id from flow_snmp.flow_data where time > '2022-08-12 00:00:00' and time < '2022-08-12 01:00:00' group by pipe_id")
client.execute("select * from flow_snmp.flow_data_second_all where pipe_id = '2dac62a1-1fb3-40d3-af4b-74c260ec1e8a' order by time desc limit 3")

pipe_list = ['2891320e-f1c1-11e7-96f3-0242ac110002','eca9cadc-9dea-11e7-b9b0-0242ac110002','16c5a4ca-bd98-11e9-ad3c-0242ac110002','c169caa0-f1c0-11e7-9908-0242ac110002','2891320e-f1c1-11e7-96f3-0242ac110002','a9cd68f0-eb30-11e9-a8e3-0242ac110002','c169caa0-f1c0-11e7-9908-0242ac110002','0940b37e-c8ca-11ea-a47a-0242ac110002','74097ee4-04cb-11e9-9a97-0242ac110002','a66bfaec-6954-11ec-a237-a6cf2cd47dab','b150a32e-8bb7-11e7-be82-0242ac110002','484ec8e0-4196-11e6-bf47-0050569b1b91','b55fdbfc-c32f-11e6-8ad6-0242ac110002','1deab2ee-a6ea-11e6-8a77-0242ac110002','e2ceb6ce-f1c0-11e7-ad1b-0242ac110002','484ec8e0-4196-11e6-bf47-0050569b1b91','88c3c156-f1c0-11e7-b540-0242ac110002','e2ceb6ce-f1c0-11e7-ad1b-0242ac110002','2bad4fb0-9b36-11ea-9258-e6b573eee7ea']
for pipe in pipe_list:
    res = client.execute(
        "select * from flow_snmp.flow_data where pipe_id = '{}' order by time limit 1".format(pipe))
    print("pipe : {} , data : {}".format(pipe, res))
    # res = client.execute("select count(*) from flow_snmp.flow_data where pipe_id = '{}' and time >= '2020-07-01 00:00:00' and time < '2020-10-01 00:00:00'".format(pipe))
    if res[0][0] >= 1:
        print(pipe)


res = client.execute("select pipe_id, count(0) as num from flow_data where time >= '' and time < '' and pipe_id = '';")

client.execute("select * from flow_snmp.flow_data where pipe_id = 'e75a82fa-b80d-11ec-9a42-22791a61f08c' and time >= '2022-04-14 16:00:00' and time < '2022-04-14 16:30:00'")




import pymysql
import traceback

db = pymysql.connect(
    host="write-mysql.gic.local",
    user="resop_20210108",
    password="1snzvbhdEOhfW4LArq$5",
    database="cdscp",
    port=6033,
    charset='utf8'
)

cursor = db.cursor()

info_list = client.execute("select pipe_id, out_bps from flow_snmp.flow_data where pipe_id in ('af0f71b8-ba37-11ec-a414-c66285652eaa','35631dca-300f-11e9-8d22-0242ac110002','b9c15012-c087-11ec-87fd-6e0d4b982ad5','3c6d58aa-fe76-11eb-aba8-0e16eef25193','14793edc-ee5e-11ea-9587-4226b22ceef4','bdad5608-331a-11ec-b427-4a2c9149e281','16466b60-bcd4-11ea-b26a-fa7ae99f6685','0f88af96-c604-11ec-bd1b-5e0e8ae9f52e','f1a4cc10-4481-11e8-b6c5-0242ac110002','3b59c7e2-a2f0-11ea-b713-0242ac110002','961aef60-6d4e-11ec-b2af-0e89447b8ee2','7c3a60da-eef7-11e9-9e64-0242ac110002','415c7a9a-1c95-11ea-a9ba-0242ac110002','f5118f6c-b9cf-11ea-9e09-0242ac110002','84c9d4ea-25c4-11e8-9afd-0242ac110002','743c3094-d0b7-11e7-94b2-0242ac110002','2a8374b2-528e-11e9-8e14-0242ac110002','29e7558a-a176-11e6-9857-0242ac102197','3fb4b690-c39f-11e7-b642-0242ac110002','c420571e-38f4-11ea-8f7f-0242ac110002','a86111b8-7076-11e9-ac6c-0242ac110002','470babaa-9e4f-11ea-b9e5-0242ac110002','455963fc-a79d-11ec-bab2-92baa902f4a8','21a04382-91ef-11eb-9309-fef0d1d18793','38eb5eb8-bddf-11e9-a5c5-0242ac110002','2153a04a-dcb7-11ec-8818-4e297d7cbb7c','f4dc24b0-ee61-11e9-842c-0242ac110002','d4f9f46e-4357-11eb-bd48-b6a066c5fc94','89b223ac-aed1-11ea-ba46-0242ac110002','caf7a132-6807-11e9-98a2-0242ac110002','641dc508-bf7c-11eb-87c0-6a633d0575d8','6cca842e-90a9-11e9-8baf-0242ac110002','18d3ce2a-629a-11ea-87f6-0242ac110002','c9537582-c087-11ec-a176-12ba9996a4f9','21c0ce8e-d532-11e9-97aa-0242ac110002','1180a216-32fe-11ec-a626-02e12117a9dc','2b6f9a6a-4033-11eb-91ab-0242ac110002','e39ce8f0-3217-11ec-be89-32f298f4feb1','1b2e1a04-3b71-11ea-8a95-0242ac110002','f5251e88-b9cf-11ea-bdee-0242ac110002','1a26484e-fe65-11eb-a02b-1e38f27fdb02','648bb36e-1b28-11ea-bd0d-0242ac110002','f451075e-851a-11ea-b7e7-0242ac110002','e9396cf2-4d2e-11ec-af2d-62e96eb38216','e4a116f6-6923-11e8-bcfc-0242ac110002','3b41135e-94cc-11e6-a16d-0242ac100602','8f5d5aca-43f9-11eb-865b-0242ac110002','87908d4e-5516-11ea-85aa-0242ac110002','a6538cb8-e026-11ea-b7ba-0242ac110002','7937420e-4f2b-11e7-afad-0242ac110002','c75d9e74-de68-11e8-aa43-0242ac110002','2afc35d8-d6a0-11e8-8c1b-0242ac110002','6c174044-d6a0-11e8-a2b0-0242ac110002','b04ac69e-96ff-11e9-8baf-0242ac110002','72db559e-fbe0-11e9-9a34-0242ac110002','bb954226-4c25-11ec-ba13-e24155c2136f','42adf544-6639-11e9-8806-0242ac110002','913667b8-e954-11e7-a664-0242ac110002','317d5ad6-c899-11e9-8f2e-0242ac110002','ec0886ca-b406-11e9-8e60-0242ac110002','3974706c-6ed7-11ec-962c-52f1064b3d9b','202905b6-bcb2-11e9-b67a-0242ac110002','20914228-cc07-11e6-9980-0242ac110002','27f8921a-1ad4-11e8-b6dd-0242ac110002','f3f30c94-6cba-11ea-ad23-0242ac110002','0167e2ae-e942-11e7-89e5-0242ac110002','1508ea5c-3735-11e7-8860-0242ac110002','cd0e6f62-ba7e-11ea-93c0-2e8aec4f3b6c','3aebcbb2-26b7-11ea-9782-0242ac110002','117f0e62-593c-11ea-9d4e-0242ac110002','08c47a06-6924-11ec-a6a9-b240c10b0009','4c8ffe10-8098-11eb-ba2a-a211abb5865e','1bf402e4-7255-11ea-ac48-7a1ae9c5896b','7093d29e-e054-11ea-ac27-0242ac110002','512260a0-1bad-11e9-9f85-0242ac110002','02026ecc-9f92-11ec-903c-e22a7879871b','560de562-a372-11ec-b22f-2e41545e0d04','93989340-d6ff-11e6-b3d4-0242ac110002','258e4f36-8a1c-11ec-b1ed-4e829e0439ab','7484117c-bca1-11ec-a860-72f82dc1dc46','4f76ac9c-2b9c-11e6-871e-0050569b1b91','cb483cd4-817b-11eb-b015-1e5aa05ba8f7','a3b292ec-6485-11e9-8806-0242ac110002','c26d525c-93b3-11ec-bf7e-e2c0ad57d64b','44c25cb6-80f7-11e9-932a-0242ac110002','0fcad918-8961-11e8-b50e-0242ac110002','7d0c80d0-6dd8-11ec-84e7-2a91651dd208','62e1c300-54f0-11e8-9955-0242ac110002','e313d0c8-1e13-11e7-87e3-0242ac110002','79a431d8-79f0-11e9-8e8a-0242ac110002','ca8690d0-9ea3-11eb-ae3d-768e7352a735','18a5bf78-1aac-11e7-ac87-0242ac110002','c404177a-38f4-11ea-b4bf-0242ac110002','25f6cfe0-8108-11e9-86af-0242ac110002','3550a17e-b0b6-11ec-9b45-56b99978e07b','2e3f66d2-a5dd-11e8-b54b-0242ac110002','dbff190e-93c1-11ec-9d9e-52194df22c9a','6c1b8e60-9e2d-11e9-be55-0242ac110002','61dd3544-4353-11eb-9ba4-0242ac110002','23130c80-b7fb-11ec-a790-769e29ec26b5','05bbabb2-de9b-11e7-8fb1-0242ac110002','f235dc3e-1861-11ec-a5f1-42330aefd4e3','503a8f3a-3dea-11eb-9ba4-0242ac110002','17805552-d58a-11eb-9be5-6a32d350c612','9a100f18-af31-11ec-b8a6-d657ade4c296','d4ead5de-771d-11eb-9236-aa0939aaab3a','dfc53cc0-884e-11e9-907a-0242ac110002','69f04f9a-80f0-11e9-a0f4-0242ac110002','37c23d46-2314-11ea-ae07-0242ac110002','76c51d3c-82b0-11ea-9fe7-8e27766fe61a','c22016d8-74d1-11e6-b7a7-0242ac103690','4a236d2a-1766-11ea-bbad-0242ac110002','4587d48c-69cb-11eb-8198-dacdf26e1c91','fb9a529c-6e2c-11e8-8125-0242ac110002','0a061284-87b8-11ea-b58c-f653e1b3e322','a79e7af4-16a0-11ec-8e12-16cc13125ce8','d86064f0-9ef0-11ea-8bc7-0242ac110002','fc07094e-3e1a-11e6-9184-0050569b1b91','e15768ea-9f54-11ec-a908-aa07576076e6','97874ef2-d9f3-11e9-b701-0242ac110002','446daa58-0580-11ec-b933-068953fe9429','4d9404f2-ec2f-11eb-a613-525153309411','58d9dfba-5952-11ea-b87c-0242ac110002','a67e09a2-a6c7-11ec-b69c-029fc8c1ad04','9f0bded8-7141-11e9-a5ea-0242ac110002','891b6508-c6a3-11e6-8ad6-0242ac110002','8f96c01c-d095-11ea-91c8-0242ac110002','29cc35f2-77c0-11e9-8e8a-0242ac110002','874cd6d6-c0c7-11ea-a149-0242ac110002','62f265e8-2928-11e6-8b5d-0050569b1b91','91bb0e06-7e7d-11ec-93c7-4a04fecb13de','c110239a-c987-11e6-8ad6-0242ac110002','9a8b8ab8-44f1-11eb-83c1-5e62c83e5908','9e3ddefc-cf4e-11ec-93f5-561b183afaf1','97de01ea-c3ad-11e9-b373-0242ac110002','6b9b12a4-85cb-11ea-bd98-7207da4452b9','0ff53a00-e258-11e8-9eee-0242ac110002','63e9dd00-286f-11e6-8a38-0050569b1b91','9e57d440-a8c8-11eb-bf03-f63f7e4eb1c1','21e40b56-4403-11eb-9c9b-0242ac110002','e73f22d4-7874-11e9-9774-0242ac110002','15934020-6384-11ea-ba02-0242ac110002','c7ad821e-4133-11ec-aa56-4eb24abdae64','436dacb2-fa2d-11e9-9a34-0242ac110002','795aed56-fb31-11eb-844a-120c1bbf1f19','e13c228e-1afd-11ea-884e-0242ac110002','4fe32f8e-6543-11e7-bab8-0242ac110002','c6067eea-b18e-11ec-aaac-5e0b60d0c8ba','be35222a-c444-11ec-a49e-fe3d5eb3c7c2','bc137752-dcbe-11ec-940a-f265a347c968','cb6d0b58-c3a7-11ec-b908-0242ac1100bd','d7771f88-c3a7-11ec-a7b8-0242ac1100b8','71e372b2-4b65-11ec-964b-dab0cc25944f','62dadf5a-769c-11e7-b6b0-0242ac110002','51f55622-0f31-11ea-8878-0242ac110002','631c8a60-05e0-11ea-95ca-0242ac110002','a1ca69f4-2b9a-11e6-af6b-0050569b1b91','5739fa70-2e39-11eb-a8c2-0242ac110002','d01d6874-5a38-11ec-84f9-325a1a2d6631') and time >= '2022-05-28 20:00:00' and time < '2022-05-28 23:00:00' group by pipe_id order by total desc limit 20")
for info in info_list:
    pipe_id = info[0]
    sql = "select a.id, a.name, c.id, c.gpn_name, d.name from cloud_pipe a, cloud_gic_app_network b, cloud_gic c, account_customer d where a.id = '{}' and a.id = b.pipe_id and b.gic_id = c.id and a.customer_id = d.id;".format(pipe_id)
    _ = cursor.execute(sql)
    res = cursor.fetchall()[0]
    text = '{}, {}, {}, {}, {}, {}'.format(info[0], round(info[1]/1000/1000/1000, 2), res[1], res[2], res[3], res[4])
    print(text)

pipe_list = ['af0f71b8-ba37-11ec-a414-c66285652eaa','35631dca-300f-11e9-8d22-0242ac110002','b9c15012-c087-11ec-87fd-6e0d4b982ad5','3c6d58aa-fe76-11eb-aba8-0e16eef25193','14793edc-ee5e-11ea-9587-4226b22ceef4','bdad5608-331a-11ec-b427-4a2c9149e281','16466b60-bcd4-11ea-b26a-fa7ae99f6685','0f88af96-c604-11ec-bd1b-5e0e8ae9f52e','f1a4cc10-4481-11e8-b6c5-0242ac110002','3b59c7e2-a2f0-11ea-b713-0242ac110002','961aef60-6d4e-11ec-b2af-0e89447b8ee2','7c3a60da-eef7-11e9-9e64-0242ac110002','415c7a9a-1c95-11ea-a9ba-0242ac110002','f5118f6c-b9cf-11ea-9e09-0242ac110002','84c9d4ea-25c4-11e8-9afd-0242ac110002','743c3094-d0b7-11e7-94b2-0242ac110002','2a8374b2-528e-11e9-8e14-0242ac110002','29e7558a-a176-11e6-9857-0242ac102197','3fb4b690-c39f-11e7-b642-0242ac110002','c420571e-38f4-11ea-8f7f-0242ac110002','a86111b8-7076-11e9-ac6c-0242ac110002','470babaa-9e4f-11ea-b9e5-0242ac110002','455963fc-a79d-11ec-bab2-92baa902f4a8','21a04382-91ef-11eb-9309-fef0d1d18793','38eb5eb8-bddf-11e9-a5c5-0242ac110002','2153a04a-dcb7-11ec-8818-4e297d7cbb7c','f4dc24b0-ee61-11e9-842c-0242ac110002','d4f9f46e-4357-11eb-bd48-b6a066c5fc94','89b223ac-aed1-11ea-ba46-0242ac110002','caf7a132-6807-11e9-98a2-0242ac110002','641dc508-bf7c-11eb-87c0-6a633d0575d8','6cca842e-90a9-11e9-8baf-0242ac110002','18d3ce2a-629a-11ea-87f6-0242ac110002','c9537582-c087-11ec-a176-12ba9996a4f9','21c0ce8e-d532-11e9-97aa-0242ac110002','1180a216-32fe-11ec-a626-02e12117a9dc','2b6f9a6a-4033-11eb-91ab-0242ac110002','e39ce8f0-3217-11ec-be89-32f298f4feb1','1b2e1a04-3b71-11ea-8a95-0242ac110002','f5251e88-b9cf-11ea-bdee-0242ac110002','1a26484e-fe65-11eb-a02b-1e38f27fdb02','648bb36e-1b28-11ea-bd0d-0242ac110002','f451075e-851a-11ea-b7e7-0242ac110002','e9396cf2-4d2e-11ec-af2d-62e96eb38216','e4a116f6-6923-11e8-bcfc-0242ac110002','3b41135e-94cc-11e6-a16d-0242ac100602','8f5d5aca-43f9-11eb-865b-0242ac110002','87908d4e-5516-11ea-85aa-0242ac110002','a6538cb8-e026-11ea-b7ba-0242ac110002','7937420e-4f2b-11e7-afad-0242ac110002','c75d9e74-de68-11e8-aa43-0242ac110002','2afc35d8-d6a0-11e8-8c1b-0242ac110002','6c174044-d6a0-11e8-a2b0-0242ac110002','b04ac69e-96ff-11e9-8baf-0242ac110002','72db559e-fbe0-11e9-9a34-0242ac110002','bb954226-4c25-11ec-ba13-e24155c2136f','42adf544-6639-11e9-8806-0242ac110002','913667b8-e954-11e7-a664-0242ac110002','317d5ad6-c899-11e9-8f2e-0242ac110002','ec0886ca-b406-11e9-8e60-0242ac110002','3974706c-6ed7-11ec-962c-52f1064b3d9b','202905b6-bcb2-11e9-b67a-0242ac110002','20914228-cc07-11e6-9980-0242ac110002','27f8921a-1ad4-11e8-b6dd-0242ac110002','f3f30c94-6cba-11ea-ad23-0242ac110002','0167e2ae-e942-11e7-89e5-0242ac110002','1508ea5c-3735-11e7-8860-0242ac110002','cd0e6f62-ba7e-11ea-93c0-2e8aec4f3b6c','3aebcbb2-26b7-11ea-9782-0242ac110002','117f0e62-593c-11ea-9d4e-0242ac110002','08c47a06-6924-11ec-a6a9-b240c10b0009','4c8ffe10-8098-11eb-ba2a-a211abb5865e','1bf402e4-7255-11ea-ac48-7a1ae9c5896b','7093d29e-e054-11ea-ac27-0242ac110002','512260a0-1bad-11e9-9f85-0242ac110002','02026ecc-9f92-11ec-903c-e22a7879871b','560de562-a372-11ec-b22f-2e41545e0d04','93989340-d6ff-11e6-b3d4-0242ac110002','258e4f36-8a1c-11ec-b1ed-4e829e0439ab','7484117c-bca1-11ec-a860-72f82dc1dc46','4f76ac9c-2b9c-11e6-871e-0050569b1b91','cb483cd4-817b-11eb-b015-1e5aa05ba8f7','a3b292ec-6485-11e9-8806-0242ac110002','c26d525c-93b3-11ec-bf7e-e2c0ad57d64b','44c25cb6-80f7-11e9-932a-0242ac110002','0fcad918-8961-11e8-b50e-0242ac110002','7d0c80d0-6dd8-11ec-84e7-2a91651dd208','62e1c300-54f0-11e8-9955-0242ac110002','e313d0c8-1e13-11e7-87e3-0242ac110002','79a431d8-79f0-11e9-8e8a-0242ac110002','ca8690d0-9ea3-11eb-ae3d-768e7352a735','18a5bf78-1aac-11e7-ac87-0242ac110002','c404177a-38f4-11ea-b4bf-0242ac110002','25f6cfe0-8108-11e9-86af-0242ac110002','3550a17e-b0b6-11ec-9b45-56b99978e07b','2e3f66d2-a5dd-11e8-b54b-0242ac110002','dbff190e-93c1-11ec-9d9e-52194df22c9a','6c1b8e60-9e2d-11e9-be55-0242ac110002','61dd3544-4353-11eb-9ba4-0242ac110002','23130c80-b7fb-11ec-a790-769e29ec26b5','05bbabb2-de9b-11e7-8fb1-0242ac110002','f235dc3e-1861-11ec-a5f1-42330aefd4e3','503a8f3a-3dea-11eb-9ba4-0242ac110002','17805552-d58a-11eb-9be5-6a32d350c612','9a100f18-af31-11ec-b8a6-d657ade4c296','d4ead5de-771d-11eb-9236-aa0939aaab3a','dfc53cc0-884e-11e9-907a-0242ac110002','69f04f9a-80f0-11e9-a0f4-0242ac110002','37c23d46-2314-11ea-ae07-0242ac110002','76c51d3c-82b0-11ea-9fe7-8e27766fe61a','c22016d8-74d1-11e6-b7a7-0242ac103690','4a236d2a-1766-11ea-bbad-0242ac110002','4587d48c-69cb-11eb-8198-dacdf26e1c91','fb9a529c-6e2c-11e8-8125-0242ac110002','0a061284-87b8-11ea-b58c-f653e1b3e322','a79e7af4-16a0-11ec-8e12-16cc13125ce8','d86064f0-9ef0-11ea-8bc7-0242ac110002','fc07094e-3e1a-11e6-9184-0050569b1b91','e15768ea-9f54-11ec-a908-aa07576076e6','97874ef2-d9f3-11e9-b701-0242ac110002','446daa58-0580-11ec-b933-068953fe9429','4d9404f2-ec2f-11eb-a613-525153309411','58d9dfba-5952-11ea-b87c-0242ac110002','a67e09a2-a6c7-11ec-b69c-029fc8c1ad04','9f0bded8-7141-11e9-a5ea-0242ac110002','891b6508-c6a3-11e6-8ad6-0242ac110002','8f96c01c-d095-11ea-91c8-0242ac110002','29cc35f2-77c0-11e9-8e8a-0242ac110002','874cd6d6-c0c7-11ea-a149-0242ac110002','62f265e8-2928-11e6-8b5d-0050569b1b91','91bb0e06-7e7d-11ec-93c7-4a04fecb13de','c110239a-c987-11e6-8ad6-0242ac110002','9a8b8ab8-44f1-11eb-83c1-5e62c83e5908','9e3ddefc-cf4e-11ec-93f5-561b183afaf1','97de01ea-c3ad-11e9-b373-0242ac110002','6b9b12a4-85cb-11ea-bd98-7207da4452b9','0ff53a00-e258-11e8-9eee-0242ac110002','63e9dd00-286f-11e6-8a38-0050569b1b91','9e57d440-a8c8-11eb-bf03-f63f7e4eb1c1','21e40b56-4403-11eb-9c9b-0242ac110002','e73f22d4-7874-11e9-9774-0242ac110002','15934020-6384-11ea-ba02-0242ac110002','c7ad821e-4133-11ec-aa56-4eb24abdae64','436dacb2-fa2d-11e9-9a34-0242ac110002','795aed56-fb31-11eb-844a-120c1bbf1f19','e13c228e-1afd-11ea-884e-0242ac110002','4fe32f8e-6543-11e7-bab8-0242ac110002','c6067eea-b18e-11ec-aaac-5e0b60d0c8ba','be35222a-c444-11ec-a49e-fe3d5eb3c7c2','bc137752-dcbe-11ec-940a-f265a347c968','cb6d0b58-c3a7-11ec-b908-0242ac1100bd','d7771f88-c3a7-11ec-a7b8-0242ac1100b8','71e372b2-4b65-11ec-964b-dab0cc25944f','62dadf5a-769c-11e7-b6b0-0242ac110002','51f55622-0f31-11ea-8878-0242ac110002','631c8a60-05e0-11ea-95ca-0242ac110002','a1ca69f4-2b9a-11e6-af6b-0050569b1b91','5739fa70-2e39-11eb-a8c2-0242ac110002','d01d6874-5a38-11ec-84f9-325a1a2d6631']

client.execute("select time, sum(in_bps), sum(out_bps) from flow_snmp.flow_data where '2022-06-29 10:50:00' < time and time < '2022-06-30 11:50:00' and pipe_id in ('386a1c14-6ee3-11e8-86f1-0242ac110002','3972b498-38d0-11e8-9462-0242ac110002','3b3acfc8-e769-11ea-aab9-0242ac110002','472de396-8857-11e9-8ab8-0242ac110002','47e0d610-8419-11e8-a2bc-0242ac110088','489b2866-b57f-11e8-8d90-0242ac110002','503ddad4-916f-11e8-8be2-0242ac110002','51564b4e-90ad-11e8-a86f-0242ac110002','52091130-3afc-11e9-a28d-0242ac110002','5250f1ce-82b0-11ea-9773-4e66bc94f8f4','5392fc10-ec81-11e8-bd2e-0242ac110002','5395259e-ec81-11e8-ae70-0242ac110002','58143346-e19f-11ec-9bcd-82537b07fb7e','5b0b2892-7893-11ea-87de-0242ac110002','5cb9d316-d225-11e8-8523-0242ac110002','5cfbeb88-909a-11e8-a8ec-0242ac110002','5d8818d6-9727-11e8-a86f-0242ac110002','5ed653a4-77b1-11e9-8e8a-0242ac110002','63059580-b7df-11e8-a89e-0242ac110002','653d1bfe-f1d6-11ec-9cc5-0a052df0a09d','658d608c-9ea3-11eb-b808-9602cbfa07f9','66f478f8-6098-11e8-8713-0242ac110002','68225d6e-a7b3-11e8-ad79-0242ac110002','698292e4-8859-11eb-991c-3a855a2ea340','6f7fa540-8f02-11e8-8337-0242ac110002','7191abe8-9afc-11e8-95c5-0242ac110002','721cfeb4-8f62-11e8-95ff-0242ac110002','727e7fdc-c094-11e8-b612-0242ac110002','7412ca64-39f6-11eb-b1cd-0242ac110002','78ecb4f2-3c81-11e8-9462-0242ac110002','7c7332b0-857c-11e8-a6a5-0242ac110002','7e49a73a-db68-11e8-812d-0242ac110002','7f7e38e0-7c63-11e9-b59a-0242ac110002','7fa7381e-90bc-11e8-8be2-0242ac110002','8010c574-6554-11e8-a6d1-0242ac110002','847ba394-0522-11ea-9a62-0242ac110002','89fba41e-89ec-11ea-97ca-ca9d4098a4de','8cce552a-0581-11e8-9d81-0242ac110002','8ebc44ae-38f7-11ea-a96f-0242ac110002','8f59dab2-324f-11e8-b09b-0242ac110002','909d1eb2-ae3d-11eb-b750-7ab07ed53196','920ef1b4-dbaf-11ea-a6ce-0242ac110002','925c9978-f44f-11eb-97f5-562e7f031744','94755d0a-4d06-11e9-a73c-0242ac110002','9591adac-2f21-11eb-aa8b-2a77df0588e5','96c7754a-2b23-11ec-afaf-dab17babe188','96ca0d92-ccfc-11e8-ad6b-0242ac110002','99ac5022-e19f-11ec-9bcd-82537b07fb7e','9d7ac576-1bb4-11e9-bc1a-0242ac110002','9f020812-91fa-11e8-95c5-0242ac110002','a198d212-398b-11e8-8607-0242ac110002','a30160fa-cdf7-11e8-8411-0242ac110002','a307aafc-ae05-11e9-aec6-0242ac110002','a6223a2e-c87a-11e9-92a4-0242ac110002','a78d6b02-89a3-11e8-a6a5-0242ac110002','a7c8324a-fbe5-11e9-bf16-0242ac110002','a7cac038-d02f-11e8-9b72-0242ac110002','ae9860ac-8645-11e8-bdb2-0242ac110002','b111f0d2-99ff-11e8-be04-0242ac110002','b39b7d2e-638f-11e8-8713-0242ac110002','b4cef55a-f555-11e9-8d61-0242ac110002','b4faa4ba-367b-11e8-8e91-0242ac110002','b6988bd0-90bb-11e8-8be2-0242ac110002','b7a778e4-cdf8-11e9-96d9-0242ac110002','b7b760aa-9afb-11e8-9f25-0242ac110002','b8c55928-bf3d-11e8-93c4-0242ac110002','b923f002-cb70-11e8-ad6b-0242ac110002','bb2555a4-bfa4-11ec-833e-3610d6e9682c','bbcaeba2-a933-11e9-b251-0242ac110002','be3b467c-b8f9-11e9-98ee-0242ac110002','c00a4e7a-9245-11e8-8be2-0242ac110002','c362d0f6-0d09-11eb-947b-0242ac110002','c7a73d72-172d-11eb-8f3c-0242ac110002','c85a3b7a-fbe5-11e9-9240-0242ac110002','ca68d084-f986-11eb-834a-963f594f9341','caeca690-d678-11e8-b286-0242ac110002','caf8fd64-d678-11e8-aa43-0242ac110002','cb2a052e-54ec-11e9-8e14-0242ac110002','cc761c0c-36b5-11e8-b9c4-0242ac110002','cf2c0f00-d67b-11ec-813c-e21c73997c29','d194db50-28f6-11e8-b112-0242ac110002','d5224dac-485e-11e8-925f-0242ac110002','d6d42bf4-b359-11e9-833f-0242ac110002','d83b4170-9022-11ea-837c-0242ac110002','d8603f30-96ef-11e8-88f9-0242ac110002','e0659f98-46d8-11e8-b822-0242ac110002','e5ae78f0-e4a1-11e8-9597-0242ac110002','e9c5f4e4-6052-11ea-a263-0605050f716b','e9dd5276-8645-11e8-9d93-0242ac110002','e9fd6764-625a-11e8-8db8-0242ac110002','ea5f891a-8853-11e9-8ab8-0242ac110002','ea88dbc8-8645-11e8-b50e-0242ac110002','eb48269c-801c-11e8-84fc-0242ac110002','eca34f72-c89a-11e9-bfba-0242ac110002','ed3fcf1c-ab04-11ea-9a2e-0242ac110002','edf3d100-37f8-11e8-98b0-0242ac110002','ee974062-54ec-11e9-9d18-0242ac110002','efe4213c-e67a-11e8-98f5-0242ac110002','f1290d80-816e-11e8-bc6e-0242ac110002','f1f57870-9e0f-11e9-b78b-0242ac110002','f52666ae-59b2-11e9-8e14-0242ac110002','f55a438c-5aa4-11e9-a6fb-0242ac110002','f8738926-991f-11e8-9ff2-0242ac1100c0','f9d6fe6a-71c9-11e8-adab-0242ac110002','fa9ea836-396e-11e8-90bd-0242ac110002','fcacb3f2-ec7e-11e8-bd2e-0242ac110002','fcb01984-ec7e-11e8-ae70-0242ac110002','fd13e45c-cb8e-11e8-92fe-0242ac110002') group by time")
# client.execute("alter table flow_snmp.flow_data_local_new delete where time > '2022-05-11 07:07:05' and time < '2022-05-12 07:07:05' and pipe_id = '30aa2a22-0653-11ec-9ca9-0a0d265d6421'")

res = client.execute("select time, in_bps from flow_snmp.flow_data where pipe_id = '4d9404f2-ec2f-11eb-a613-525153309411' order by time desc limit 3")
from datetime import datetime
datetime.timestamp()


res = client.execute("select distinct pipe_id from flow_snmp.flow_data where time > '2022-08-12 00:00:00' and time < '2022-08-12 01:00:00'")
with open('{}.txt'.format('pipes'), 'w+') as f1:
    for r in res:
        f1.write('{}\n'.format(r[0]))

with open("pipes.txt") as file:
    pipes = [item.replace('\n', '') for item in file]


from datetime import datetime, timedelta
from random import randint
start_time = datetime(2022, 8, 3, 2, 00, 00)
end_time = datetime(2022, 8, 12, 11, 00, 00)
ck_data_list = []
FLOW_TABLE_NAME = "flow_data_local_new"
while start_time < end_time:
    ck_data_list.append(['8a67d02a-fb79-11ec-a4f8-0a6807bdebf2', start_time, int(randint(400, 800)/100*1000*1000), int(randint(800, 1300)/100*1000*1000)])
    start_time += timedelta(seconds=300)


insert_sql = f"insert into {CK_DB_ANME}.{FLOW_TABLE_NAME} (pipe_id, time, in_bps, out_bps) VALUES"
client.execute(insert_sql, ck_data_list)


client.execute("select * from flow_snmp.flow_data where time = '2022-09-01 10:25:00' and pipe_id = 'f4a29bf2-2827-11ed-9830-aa0c93599854'")
client.execute("select * from flow_snmp.flow_data_second_all where time = '2022-09-01 10:25:00' and pipe_id = 'f4a29bf2-2827-11ed-9830-aa0c93599854'")
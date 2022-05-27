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
client.execute("select * from flow_snmp.flow_data where pipe_id = '0832a41e-3dff-11ec-ad5f-aa9751aacb94' order by time desc limit 3")

client.execute("show create table flow_snmp.flow_data")
client.execute("SELECT * from flow_snmp.flow_data where pipe_id = '8a727b4c-3540-11ec-ab9c-ea82af98404f' and time > '2021-10-31 11:00:00' and time < '2021-10-31 12:00:00'")
# client.execute("ALTER TABLE flow_snmp.flow_data_first_local DROP PARTITION '202107'")
client.execute("select partition, sum(rows), formatReadableSize(sum(data_uncompressed_bytes)) from system.parts where table = 'flow_data_local_new' GROUP BY partition")
# client.execute("DROP TABLE flow_snmp.flow_data_first_local01 ON CLUSTER cluster_1shards_3replicas")


client.execute("select * from flow_snmp.flow_data where pipe_id = '271ff9ca-d92b-11e9-888c-0242ac110002' order by time desc limit 3")
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
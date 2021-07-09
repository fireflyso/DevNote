from clickhouse_driver import Client

CK_HOST = "10.13.133.134"
CK_USER = "flowdata"
CK_PASSWORD = "wVen6RK3KpkpGdsA"
CK_DB_ANME = "flow_snmp"
CK_PORT = 9000
client = Client(host=CK_HOST, port=CK_PORT, user=CK_USER, password=CK_PASSWORD)


sql = "CREATE TABLE flow_snmp.flow_data_local_new_second (`pipe_id` String,`time` DateTime,`in_flow` Float64,`out_flow` Float64,`in_bps` Float64,`out_bps` Float64) ENGINE=Log"
ans = client.execute(sql)
client.execute("show databases")
client.execute("SHOW TABLES FROM  flow_snmp")
client.execute("SHOW GRANTS")
client.execute("SELECT * FROM system.clusters")
client.execute("SELECT sum(rows), formatReadableSize(sum(data_uncompressed_bytes)), formatReadableSize(sum(data_compressed_bytes)) from system.parts WHERE (database IN ('flow_snmp')) AND (table IN ('flow_data_first_local'))")
client.execute("SELECT pipe_id from flow_snmp.flow_data_local_new where time > '2021-05-01 12:00:00' order by time limit 50")
client.execute("SELECT pipe_id, COUNT(pipe_id) FROM flow_snmp.flow_data_local_new where time > '2021-07-06 11:00:00' group by pipe_id")
client.execute("SELECT pipe_id, COUNT(pipe_id) FROM flow_snmp.flow_data_local_new where time > '2020-10-06 11:00:00' and time > '2020-10-06 12:00:00' group by pipe_id")
client.execute("SHOW CREATE flow_snmp.flow_data_local_new")
client.execute("SELECT time, in_bps, out_bps from flow_snmp.flow_data WHERE pipe_id  = '06be7cce-c55d-11e9-82db-0242ac110002' and time > '2021-06-06 12:30:00' and time < '2021-07-06 12:30:00' order by time")

client.execute("select partition, sum(rows), formatReadableSize(sum(data_uncompressed_bytes)) from system.parts where table = 'flow_data_first_local' GROUP BY partition")
client.execute("select formatReadableSize(sum(data_uncompressed_bytes)), formatReadableSize(sum(data_compressed_bytes)) from system.parts where table = 'flow_data_local_new'")

client.execute("select count(*) from flow_snmp.flow_data_first_local")
client.execute("select count(*) from flow_snmp.flow_data_local_new")
client.execute("SELECT PARTITION,sum(rows),formatReadableSize (sum(data_uncompressed_bytes)),formatReadableSize (sum(data_compressed_bytes)) FROM system.parts WHERE (DATABASE IN ('flow_snmp')) AND (TABLE IN ('flow_data_first_local01')) GROUP BY PARTITION ORDER BY PARTITION ASC")


# 线上新建表结构
client.execute("CREATE TABLE flow_snmp.flow_data_first_local ON CLUSTER cluster_1shards_3replicas (`pipe_id` UUID,`time` DateTime,`in_flow` Float64,`out_flow` Float64,`in_bps` Float64,`out_bps` Float64) ENGINE=ReplicatedMergeTree ('/clickhouse/tables/{shard}/flow_data_first_local','{replica}') PARTITION BY toYYYYMM (time) ORDER BY (pipe_id,time) SETTINGS index_granularity=8192")
client.execute("CREATE TABLE flow_snmp.flow_data_first_all ON CLUSTER cluster_1shards_3replicas AS flow_snmp.flow_data_first_local ENGINE=Distributed ('cluster_1shards_3replicas','flow_snmp','flow_data_first_local',rand())")
client.execute("CREATE TABLE flow_snmp.flow_data_second_local ON CLUSTER cluster_1shards_3replicas (`pipe_id` UUID,`time` DateTime,`in_flow` Float64,`out_flow` Float64,`in_bps` Float64,`out_bps` Float64) ENGINE=ReplicatedMergeTree ('/clickhouse/tables/{shard}/flow_data_second_local','{replica}') PARTITION BY toYYYYMM (time) ORDER BY (pipe_id,time) SETTINGS index_granularity=8192")
client.execute("CREATE TABLE flow_snmp.flow_data_second_all ON CLUSTER cluster_1shards_3replicas AS flow_snmp.flow_data_second_local ENGINE=Distributed ('cluster_1shards_3replicas','flow_snmp','flow_data_second_local',rand())")

client.execute("INSERT INTO flow_snmp.flow_data_second_local (pipe_id, `time`, in_flow, out_flow, in_bps, out_bps) VALUES('059719dc-dd66-11eb-b05b-1e3805d0e445', '2021-07-05 15:55:00', 32674.0, 0.0, 0.0, 1.0)")
client.execute("select count(*) from flow_snmp.flow_data_first_local")
client.execute("select * from flow_snmp.flow_data_second_all")
client.execute("select partition, sum(rows), formatReadableSize(sum(data_uncompressed_bytes)) from system.parts where table = 'flow_data_first_local' GROUP BY partition")
# client.execute("DROP TABLE flow_snmp.flow_data_first_local01 ON CLUSTER cluster_1shards_3replicas")



ck_cluster = [
    {
        "host": "10.13.133.133",
        "user": "flowdata",
        "password": "wVen6RK3KpkpGdsA",
        "port": 9000,
    },
    {
        "host": "10.13.133.134",
        "user": "flowdata",
        "password": "wVen6RK3KpkpGdsA",
        "port": 9000,
    },
    {
        "host": "10.13.133.135",
        "user": "flowdata",
        "password": "wVen6RK3KpkpGdsA",
        "port": 9000,
    },
]

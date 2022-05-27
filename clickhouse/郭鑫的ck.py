from clickhouse_driver import Client

CK_HOST = "103.52.173.183"
CK_USER = "flowdata"
CK_PASSWORD = "wVen6RK3KpkpGdsA"
CK_DB_ANME = "flow_snmp"
CK_PORT = 9000
client = Client(host=CK_HOST, port=CK_PORT, user=CK_USER, password=CK_PASSWORD)

client.execute("SELECT time, in_bps, out_bps FROM flow_snmp.flow_data_first_all where pipe_id  = '6c6d7e6a-2375-11e9-9cc0-0242ac110002' and time >= '2021-06-30 12:30:00' and time <= '2021-06-30 16:55:00' order by time")


sql = "CREATE TABLE flow_snmp.flow_data_local_new_second (`pipe_id` String,`time` DateTime,`in_flow` Float64,`out_flow` Float64,`in_bps` Float64,`out_bps` Float64) ENGINE=Log"
ans = client.execute(sql)
client.execute("show databases")
from clickhouse_driver import Client

CK_HOST = "10.13.133.135"
CK_USER = "flowdata"
CK_PASSWORD = "wVen6RK3KpkpGdsA"
CK_DB_ANME = "flow_snmp"
CK_PORT = 9000
client = Client(host=CK_HOST, port=CK_PORT, user=CK_USER, password=CK_PASSWORD)

end_time = '2023-08-14 16:05:00'

dst_pipe_id = 'e98620fe-3a78-11ee-aad7-c2488d702a72'

ck_sql = "Alter table flow_snmp.flow_data_local_new DELETE where pipe_id = '{}' and time < '{}'".format(
    dst_pipe_id, end_time)
client.execute(ck_sql)

client.execute("select * from flow_snmp.flow_data_local_new where pipe_id = 'e98620fe-3a78-11ee-aad7-c2488d702a72' order by time limit 1")




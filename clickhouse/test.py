import clickhouse_connect
client = clickhouse_connect.get_client(host='10.13.133.133', username="flowdata", password="wVen6RK3KpkpGdsA")
client.command("""ALTER TABLE flow_snmp.flow_data_local_new UPDATE in_bps = 2110148916.0,out_bps = 85141233354.0 WHERE pipe_id = '4eaf5570-f45d-11ed-bb3b-fac1491bd8ed' and time = '2023-07-01 03:10:00';""")
client.execute("SELECT pipe_id, time, in_bps, out_bps FROM flow_snmp.flow_data_local_new where pipe_id = '4eaf5570-f45d-11ed-bb3b-fac1491bd8ed' and time = '2023-07-01 03:10:00'")
client.query("SELECT pipe_id, time, in_bps, out_bps FROM flow_snmp.flow_data_local_new where pipe_id = '4eaf5570-f45d-11ed-bb3b-fac1491bd8ed' and time = '2023-07-01 03:10:00'").result_set
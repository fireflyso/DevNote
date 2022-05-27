from clickhouse_driver import Client
CK_HOST = "10.2.10.28"
CK_USER = "default"
CK_PASSWORD = "cds-china"
CK_PORT = 9000
client = Client(host=CK_HOST, port=CK_PORT, user=CK_USER, password=CK_PASSWORD)

# client.execute("show databases")
# res = client.execute("SELECT * FROM flow_snmp.flow_data_first_all  where pipe_id = '8d902306-4e5e-11ec-993b-42b493c33671' order by time limit 10")
print('read update')
res = client.execute("SELECT time, in_bps, out_bps FROM flow_snmp.flow_data where pipe_id  = '3a9a9ff8-b710-11ec-9bfc-8252cbfa8cce' and time >= '2022-04-13 17:45:01' and time < '2022-04-13 17:46:01' order by time")
print(res)
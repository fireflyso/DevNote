from clickhouse_driver import Client


def get_ch_client():
    CK_HOST = "10.2.10.30"
    CK_USER = "default"
    CK_PASSWORD = "cds-china"
    CK_PORT = 9000
    client = Client(host=CK_HOST, port=CK_PORT, user=CK_USER, password=CK_PASSWORD, database='wan_fping')
    return client


ip = '180.167.3.12'
client = get_ch_client()
sql = "select * from wan_fping.fping_data where dst_ip = toIPv4('{}') order by ping_time;".format(ip)
res_list = client.execute(sql)
for res in res_list:
    print(res)

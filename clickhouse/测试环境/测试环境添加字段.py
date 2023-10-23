# -- coding: utf-8 --
# @Time : 2023/10/10 18:03
# @Author : xulu.liu
from clickhouse_driver import Client
# host 10.4.19.108,10.4.19.109,10.4.19.112
host_list = ['10.4.19.108', '10.4.19.109', '10.4.19.112']
for host in host_list:
    CK_HOST = host
    CK_USER = "default"
    CK_PASSWORD = ""
    CK_PORT = 9000
    client = Client(host=CK_HOST, port=CK_PORT, user=CK_USER, password=CK_PASSWORD)

    # client.execute("show databases")
    # client.execute("select version()")
    # client.execute("select * from system.clusters")
    # client.execute("SELECT name FROM system.tables WHERE database = 'slb_monitor'")
    # client.execute("show create table slb_monitor.slb_listen_ping_local")
    sql = """
    alter table slb_monitor.slb_listen_ping_local ADD COLUMN ip_port String comment 'ip:port' AFTER listen_id
    """

    client.execute(sql)

    sql = """
    alter table slb_monitor.slb_listen_ping_all ADD COLUMN ip_port String comment 'ip:port' AFTER listen_id
    """
    client.execute(sql)

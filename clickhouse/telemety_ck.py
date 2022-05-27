from clickhouse_driver import Client

CK_HOST = "10.13.133.134"
CK_USER = "flowdata"
CK_PASSWORD = "wVen6RK3KpkpGdsA"
CK_DB_ANME = "flow_snmp"
CK_PORT = 9000
client = Client(host=CK_HOST, port=CK_PORT, user=CK_USER, password=CK_PASSWORD)
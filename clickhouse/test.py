import clickhouse_driver
from datetime import datetime, timedelta
ip = '164.52.2.166'
end_time = datetime.now().replace(microsecond=0)
start_time = end_time - timedelta(minutes=60)


CK_HOST = "10.13.124.35"
CK_USER = "default"
CK_PASSWORD = "$nM*Jgkx%DmU"
connection = clickhouse_driver.connect(host=CK_HOST, port=9000, user=CK_USER, password=CK_PASSWORD,database='wan_fping')

# query = "select count(*) from wan_fping.mtr_time_all where mtr_time > %(time)s;"
query = "select country_code from wan_fping.fping_data_all where src_ip = toIPv4(%(ip)s) and ping_time >= %(start_time)s and ping_time <= %(end_time)s group by country_code;"

# params = {'time': '2023-02-20 14:00:41'}
params = {'ip': ip, 'start_time': start_time, 'end_time': end_time}

cursor = connection.cursor()
cursor.execute(query, params)

for row in cursor:
    print(row)

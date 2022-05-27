import time

start = time.perf_counter()
info = '2021-08-22 21:52:19 +0800 juniperNetworks: {"interface_info.if_name":"xe-0/1/4.16386","interface_info.init_time":1629283166,"interface_info.snmp_if_index":733,"interface_info.egress_stats.if_packets":0,"interface_info.egress_stats.if_octets":0,"device":"GW01:172.10.10.1","host":"snmp-agent","sensor_name":"jnprLogicalInterfaceExt","time":1629640339728}'
for _ in range(100000):
    pass

for _ in range(100000):
    pass
for _ in range(100000):
    pass
for _ in range(100000):
    pass
for _ in range(100000):
    pass

print('用时： {}'.format(time.perf_counter() - start))

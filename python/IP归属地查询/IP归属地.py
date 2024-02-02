# -- coding: utf-8 --
# @Time : 2023/11/9 14:13
# @Author : xulu.liu
import geoip2.database

# 加载IP数据文件
reader = geoip2.database.Reader('/Users/liuxulu/workspace/DevNote/python/IP归属地查询/GeoLite2-City.mmdb')

# 读取要查询的IP列表
with open('/Users/liuxulu/workspace/DevNote/python/IP归属地查询/ips.txt') as f:
    ip_list = f.read().splitlines()

address_list = []
# 查询每个IP的归属地信息
for ip in ip_list:
    try:
        response = reader.city(ip)
        # 处理响应数据，例如输出城市名和国家码
        # print(response.city.name, response.country.iso_code)
        address_list.append((ip, response.country.iso_code, response.country.names.get('zh-CN'), response.city.names.get('zh-CN'), response.city.name))
    except geoip2.errors.AddressNotFoundError:
        # 处理未找到IP地址的情况
        print(ip, 'Not found')

with open('/Users/liuxulu/workspace/DevNote/python/IP归属地查询/address.txt', 'w') as f:
    for address in address_list:
        f.write('{},{}({}),{}({})\n'.format(address[0], address[1], address[2], address[3], address[4]))

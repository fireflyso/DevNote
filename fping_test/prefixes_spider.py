import requests
import json
import redis
r = redis.Redis(host='10.2.10.126', port=6379, decode_responses=True, password='000415')

asn = 4812
url = 'https://api.bgpview.io/asn/{}/prefixes'.format(asn)

res = json.loads(requests.get(url).content)
prefix_list = res.get('data').get('ipv4_prefixes')
all_prefix = set()
parent_prefix = set()
for prefix in prefix_list:
    all_prefix.add(prefix.get('prefix', ''))
    parent_prefix.add(prefix.get('parent', {}).get('prefix', ''))

print('总数量为：{}'.format(len(all_prefix)))
print('父prefixes数量为：{}'.format(len(parent_prefix)))
print('子prefixes数量为：{}'.format(len(all_prefix - parent_prefix)))

for prefix in list(all_prefix - parent_prefix):
    r.lpush('prefix_list', prefix)

print("Redis key prefix_list 的元素个数 {}".format(r.llen('prefix_list')))

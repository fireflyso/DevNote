# -- coding: utf-8 --
# @Time : 2023/6/7 14:24
# @Author : xulu.liu
import redis


def get_public_redis_conn(host):
    return redis.Redis(
        host=host,
        port=7936,
        decode_responses=True,
        password='cds-cloud@2022'
    )


old_redis = get_public_redis_conn('164.52.25.158')

old_redis.set('test', '123')
print(old_redis.get('test'))


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


product_list = [5, 10, 11, 20, 22]

old_redis = get_public_redis_conn('106.3.133.42')
new_redis = get_public_redis_conn('164.52.47.110')

for pid in product_list:
    COMPARE_FPING_TASK_SET = "fping_pro{}_task_set".format(pid)
    compare_task = old_redis.smembers(COMPARE_FPING_TASK_SET)
    pipeline = new_redis.pipeline()
    for task in compare_task:
        pipeline.sadd(COMPARE_FPING_TASK_SET, task)
    pipeline.execute()

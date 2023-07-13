import requests
import json
import pymysql
from datetime import datetime, timedelta

db = pymysql.connect(
    host="write-mysql.gic.local",
    user="resop_20210108",
    password="1snzvbhdEOhfW4LArq$5",
    database="cdscp",
    port=6033,
    charset='utf8'
)

cursor = db.cursor()


def send_req(url: str, data: dict):
    status = False
    res = requests.post(url=url, data=data)
    if res.status_code == 200:
        res_data = json.loads(res.content)['data'][0]
        if 'max' in url:
            print('api : {} 接口请求成功，尝试解析数据完成, out_bps_max 为 ： {}!'.format(url, res_data['out_bps_max']))
        else:
            print('api : {} 接口请求成功，尝试解析数据完成, value 为 ： {}!'.format(url, res_data['value']))
        status = True
    else:
        print('\napi : {} 请求失败，返回状态码为 : {}, data : {}'.format(url, res.status_code, data))

    return status


def get_pipe() -> dict:
    """
    取出7天前最新创建的三个公网、三个带宽资源、三个slb公网
    :return:
    """
    pipe_dict = {}
    create_time = (datetime.now() - timedelta(days=2)).replace(microsecond=0)

    sql = "select id from cloud_pipe where type = 'public' and create_time < '{}' and is_valid = 1 order by create_time desc limit 3;".format(create_time)
    _ = cursor.execute(sql)
    res = cursor.fetchall()
    for r in res:
        pipe_dict[r[0]] = '公网'

    sql = "select id from automatic_product.vpc_eip_bandwidth where master_route_id != '' and create_time < '{}' and is_valid = 1 order by create_time desc limit 3;".format(create_time)
    _ = cursor.execute(sql)
    res = cursor.fetchall()
    for r in res:
        pipe_dict[r[0]] = 'EIP'

    sql = "select pipe_id from cloud_slb_network where is_valid = 1 and type = 'master' and create_time < '{}' order by create_time desc limit 3;".format(create_time)
    _ = cursor.execute(sql)
    res = cursor.fetchall()
    for r in res:
        pipe_dict[r[0]] = 'SLB公网'

    print('自动从数据库中获取到 {} 个资源 : {}'.format(len(pipe_dict), pipe_dict))
    return pipe_dict


if __name__ == '__main__':
    """
    对计量底层项目的接口进行调用测试，以保证基础功能没有问题
    TODO 月95接口和slb存储功能未测试
    """
    api_list = [
        'bps_list',         # 接口
        'bps_95',           # 接口
        'hour_bps_list',    # 接口
        'flow',             # 接口
        'data_list',        # 接口
        'max',              # 接口
        'bps_5th',          # 接口

        'vpc_bps_list',
        'vpc_bps_95',
        'vpc_hour_bps_list',
        'vpc_flow',
        'vpc_data_list',
        'vpc_max',
        'vpc_bps_5th',
    ]
    host = 'http://localhost:9999'
    pipe_info = get_pipe()
    start_time = (datetime.now() - timedelta(days=1)).replace(microsecond=0)
    mid_time = start_time + timedelta(hours=1)
    end_time = start_time + timedelta(hours=2)
    data = {
        "start_time": str(start_time),
        "mid_time": str(mid_time),
        "end_time": str(end_time)
    }
    fail_list = []
    for pipe, p_type in pipe_info.items():
        data['cloud_id'] = pipe
        for api in api_list:
            res_status = False
            try:
                res_status = send_req("{}/{}".format(host, api), data)
            except Exception as e:
                print(e)

            if not res_status:
                fail_list.append((pipe, p_type, api, data))

    print('测试结果：失败的API数量：{} ，详细信息为:'.format(len(fail_list)))
    for f in fail_list:
        print(f)


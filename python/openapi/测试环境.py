# -- coding: utf-8 --
# @Time : 2023/8/11 16:50
# @Author : xulu.liu

import base64
import hmac
import json
import sys
import urllib
import uuid
import time
from hashlib import sha1

import requests

AK = '6618eac2372011eeb36ae22f8165fe95'
AccessKeySecret = '32fc229a69ed918db88ce8384d4d07c0'

# NETWORK_URL = 'http://cdsapi.capitalonline.net/vpc'
# NETWORK_URL = 'http://cdsapi.gic.pre/vpc'
NETWORK_URL = 'http://openapi.gic.test/vpc'


def percentEncode(str):
    """将特殊转义字符替换"""
    res = urllib.parse.quote(str.encode('utf-8').decode(sys.stdin.encoding).encode('utf8'), '')
    res = res.replace('+', '%20')
    res = res.replace('*', '%2A')
    res = res.replace('%7E', '~')
    return res


def get_signature(action, ak, access_key_secret, method, url, param={}):
    """
    @params: action: 接口动作
    @params: ak: ak值
    @params: access_key_secret: ak秘钥
    @params: method: 接口调用方法(POST/GET)
    @params: param: 接口调用Query中参数(非POST方法Body中参数)
    @params: url: 接口调用路径
    @return: 请求的url可直接调用
    """
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    D = {
        'Action': action,
        'AccessKeyId': ak,
        'SignatureMethod': 'HMAC-SHA1',
        'SignatureNonce': str(uuid.uuid1()),
        'SignatureVersion': "1.0",
        "Timestamp": timestamp,
        'Version': '2019-08-08',
        "CustomerId": "E020912",
        "UserId": "713094"
    }
    if param:
        D.update(param)
    sortedD = sorted(D.items(), key=lambda x: x[0])
    canstring = ''
    for k, v in sortedD:
        canstring += '&' + percentEncode(k) + '=' + percentEncode(v)
    stringToSign = method + '&%2F&' + percentEncode(canstring[1:])
    key_bytes = bytes(access_key_secret, 'utf-8')  # Commonly 'latin-1' or 'utf-8'
    data_bytes = bytes(stringToSign, 'utf-8')  # Assumes `data` is also a string.
    h = hmac.new(key_bytes, data_bytes, sha1)
    Signature = base64.encodebytes(h.digest()).strip()
    D['Signature'] = Signature
    url = url + '/?' + urllib.parse.urlencode(D)
    print(url)
    return url


def listen_clear():
    action = 'VpcSlbClearListen'
    method = "POST"
    param = {}
    url = get_signature(action, AK, AccessKeySecret, method, NETWORK_URL, param=param)
    body = {
        "SlbId": "8a87c54a-34d7-11ee-9d57-860f13187611"
    }
    res = requests.post(url, json=body)
    result = json.loads(res.content)
    return result


def slb_detail():
    action = "DescribeVpcSlb"
    method = "GET"
    param = {
        "SlbId": "1963f28e-3fc8-11ee-baf3-162664d58161",
        "SlbName": ""
    }
    url = get_signature(action, AK, AccessKeySecret, method, NETWORK_URL, param)
    res = requests.get(url)
    result = json.loads(res.text)
    return result


def batch_update_listen():
    action = 'VpcSlbUpdateListen'
    method = "POST"
    param = {}
    url = get_signature(action, AK, AccessKeySecret, method, NETWORK_URL, param=param)
    body = {
        "SlbId": "1963f28e-3fc8-11ee-baf3-162664d58161",
        "Platform": "eks",
        "OperatorType": "full",
        "UserId": "713094",
        "CustomerId": "E020912",
        "ListenList": [
            {
                "ListenIp": "140.210.70.136",
                "ListenPort": 80,
                "ListenProtocol": "TCP",
                "Scheduler": "rr",
                "ListenName": "监听测试11",
                "Timeout": 10,
                "HealthCheck": {
                    "Protocol": "TCP",
                    "Virtualhost": "",
                    "Port": 0,
                    "Path": "",
                    "StatusCode": 10,
                    "ConnectTimeout": 10,
                    "DelayLoop": 10,
                    "Retry": 2,
                    "DelayBeforeRetry": 100
                },
                "RsList": [
                    {
                        "RsId": "ins-1f2c75dsd9mc40mb",
                        "RsName": "rs-002",
                        "RsType": "eks",
                        "RsWanIp": "",
                        "RsLanIp": "10.22.1.8",
                        "RsPort": 80,
                        "Weight": 120
                    },
                    {
                        "RsId": "ins-1f2c75dsd9mc40mb",
                        "RsName": "rs-003",
                        "RsType": "eks",
                        "RsWanIp": "",
                        "RsLanIp": "10.22.1.9",
                        "RsPort": 80,
                        "Weight": 120
                    }
                ]
            }
        ]
    }
    res = requests.post(url, json=body)
    result = json.loads(res.content)
    return result


def query_vpc_slb_rs_port():
    action = "QueryVpcSLBRsPort"
    method = "POST"
    param = {}
    url = get_signature(action, AK, AccessKeySecret, method, NETWORK_URL, param=param)
    body = {
        "ListenId": "ab24bf50-53b4-11ee-9d9f-feb5ec439909",
        "Keyword": "",
        "Page": 1,
        "PageSize": 20
    }
    res = requests.post(url, json=body)
    result = json.loads(res.content)
    return result


def update_vpc_slb_rs_port():
    action = "UpdateVpcSLBRsPort"
    method = "POST"
    param = {}
    url = get_signature(action, AK, AccessKeySecret, method, NETWORK_URL, param=param)
    body = {
        "RsPortList": [
            {
                "RsPortId": "c63d54f0-53b4-11ee-9d9f-feb5ec439909",
                "Ip": "1.1.1.1",
                "Port": "80",
                "Weight": "100"
            }
        ]
    }
    res = requests.post(url, json=body)
    result = json.loads(res.content)
    return result


def delete_vpc_slb_rs_port():
    action = "DeleteVpcSLBRsPort"
    method = "POST"
    param = {}
    url = get_signature(action, AK, AccessKeySecret, method, NETWORK_URL, param=param)
    body = {
        "RsPortIds": ["c63d54f0-53b4-11ee-9d9f-feb5ec439909"]
    }
    res = requests.post(url, json=body)
    result = json.loads(res.content)
    return result


def create_vpc_slb_rs_port():
    action = "QueryVpcSLBRsPort"
    method = "POST"
    param = {}
    url = get_signature(action, AK, AccessKeySecret, method, NETWORK_URL, param=param)
    body = {
        "ListenId": "ab24bf50-53b4-11ee-9d9f-feb5ec439909",
        "RsList": [
            {
                "VmId": "",
                "VmName": "",
                "VmPublicIp": "",
                "VmType": "kvm",
                "VmPrivateIp": "1.1.1.2",
                "Port": "8000",
                "Weight": "100"
            }
        ]
    }
    res = requests.post(url, json=body)
    result = json.loads(res.content)
    return result


def create_vpc_slb_listen():
    action = "QueryVpcSLBRsPort"
    method = "POST"
    param = {}
    url = get_signature(action, AK, AccessKeySecret, method, NETWORK_URL, param=param)
    body = {
        "SlbId": "1963F28E-3Fc8-11Ee-Baf3-162664D58161",
        "ListenName": "新建监听",
        "Vip": "140.210.70.136",
        "VipId": "0Ae70172-3Fca-11Ee-Baf3-162664D58161",
        "VipType": "wan_eip",
        "ListenProtocol": "TCP",
        "ListenPort": 8000,
        "AclId": "",
        "ListenTimeout": 10,
        "Scheduler": "rr",
        "HealthCheckInfo": {
            "Protocol": "TCP",
            "Virtualhost": "",
            "Port": 0,
            "Path": "",
            "StatusCode": 200,
            "ConnectTimeout": 5,
            "DelayLoop": 10,
            "Retry": 2,
            "DelayBeforeRetry": 150
        }
    }
    res = requests.post(url, json=body)
    result = json.loads(res.content)
    return result


def query_vpc_slb_listen():
    action = "QueryVpcSLBListen"
    method = "GET"
    param = {
        "ListenId": "ab24bf50-53b4-11ee-9d9f-feb5ec439909"
    }
    url = get_signature(action, AK, AccessKeySecret, method, NETWORK_URL, param)
    res = requests.get(url)
    result = json.loads(res.text)
    return result


def update_vpc_slb_listen():
    action = "QueryVpcSLBRsPort"
    method = "POST"
    param = {}
    url = get_signature(action, AK, AccessKeySecret, method, NETWORK_URL, param=param)
    body = {
        "SlbId": "1963F28E-3Fc8-11Ee-Baf3-162664D58161",
        "ListenId": "2E2C2281-512D-11Ee-9Ee3-D3E8Ee1C0957",
        "ListenName": "更新监听Test",
        "AclId": "",
        "ListenTimeout": 10,
        "Scheduler": "rr",
        "HealthCheckInfo": {
            "Protocol": "TCP",
            "Virtualhost": "",
            "Port": 0,
            "Path": "",
            "StatusCode": 200,
            "ConnectTimeout": 5,
            "DelayLoop": 10,
            "Retry": 2,
            "DelayBeforeRetry": 150
        }
    }
    res = requests.post(url, json=body)
    result = json.loads(res.content)
    return result


def delete_vpc_slb_listen():
    action = "QueryVpcSLBRsPort"
    method = "POST"
    param = {}
    url = get_signature(action, AK, AccessKeySecret, method, NETWORK_URL, param=param)
    body = {
        "ListenIds": ["b56413c0-511c-11ee-ac10-7c10c9b7d22b"]
    }
    res = requests.post(url, json=body)
    result = json.loads(res.content)
    return result


if __name__ == '__main__':
    # 新增的接口
    # a = listen_clear()
    # res = slb_detail()
    # a = batch_update_listen()

    # vpc负载均衡监听服务器端口信息查询
    # res = query_vpc_slb_rs_port()
    # vpc负载均衡监听批量修改服务器端口
    # res = update_vpc_slb_rs_port()
    # vpc负载均衡监听批量解绑服务器端口
    # res = delete_vpc_slb_rs_port()
    # vpc负载均衡监听批量绑定服务器端口
    # res = create_vpc_slb_rs_port()

    # 查询vpc负载均衡监听
    res = query_vpc_slb_listen()
    # 更新vpc负载均衡监听
    # res = update_vpc_slb_listen()
    # 删除vpc负载均衡监听
    # res = delete_vpc_slb_listen()
    # 创建vpc负载均衡监听
    # res = create_vpc_slb_listen()

    print(json.dumps(res))

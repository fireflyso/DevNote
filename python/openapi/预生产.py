# -*- coding: utf-8 -*-
# @Time:    2022/4/25 11:13

import base64
import hmac
import json
import sys
import urllib
import uuid
import time
from hashlib import sha1

import requests

NETWORK_URL = 'http://cdsapi-gateway.gic.pre/openapi/vpc'
AK = '38bc80ae369611eaabc00242ac110002'
AccessKeySecret = '808db82b32e28be06d1879ef0c635f9c'

def percentEncode(str):
    """将特殊转义字符替换"""
    res = urllib.parse.quote(str.encode('utf-8').decode(sys.stdin.encoding).encode('utf8'), '')
    res = res.replace('+', '%20')
    res = res.replace('*', '%2A')
    res = res.replace('%7E', '~')
    return res


def get_signature(action, ak, access_key_secret, method, url, param=None):
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
        "CustomerId": "E104616",
        "UserId": "630387"
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


def scheme():
    # NETWORK_URL = 'http://cdsapi.capitalonline.net/vpc'
    NETWORK_URL = 'http://cdsapi-gateway.gic.pre/openapi/vpc'
    action = 'VpcSlbBillingScheme'
    method = "POST"
    body = {
        "AvailableZoneCode": "CN_Suqian_B",
        "BillingMethod": "0",
        "NetType": "wan"
    }
    AK = '38bc80ae369611eaabc00242ac110002'
    AccessKeySecret = '808db82b32e28be06d1879ef0c635f9c'
    url = get_signature(action, AK, AccessKeySecret, method, NETWORK_URL)
    res = requests.post(url, json=body)
    result = json.loads(res.content)
    return result


def slb_detail():
    action = "DescribeVpcSlb"
    method = "GET"
    param = {
        "SlbId": "a88399f0-4253-11ee-9dd0-c2e5e223b0cb",
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
        "SlbId": "8a87c54a-34d7-11ee-9d57-860f13187611",
        "Platform": "eks",
        "OperatorType": "full",
        "UserId": "713094",
        "CustomerId": "E020912",
        "ListenList": [
            {
                "ListenIp": "140.210.70.141",
                "ListenPort": 80,
                "ListenProtocol": "TCP",
                "Scheduler": "rr",
                "ListenName": "监听测试11",
                "Timeout": 10,
                "RsList": [
                    {
                        "RsId": "ins-1f2c75dsd9mc40mb",
                        "RsName": "rs-002",
                        "RsType": "eks",
                        "RsWanIp": "",
                        "RsLanIp": "10.22.1.8",
                        "RsPort": 80
                    }
                ]
            }
        ]
    }
    res = requests.post(url, json=body)
    result = json.loads(res.content)
    return result


if __name__ == '__main__':
    # a = scheme()
    a = slb_detail()
    print(json.dumps(a))



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
        #主账户
        # "CustomerId": "E036042",
        # "UserId": "18600529015"
        #子用户
        "CustomerId": "E036042",
        "UserId": "10000000909w"


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


def get_pipe_utilization():
    NETWORK_URL = 'http://cdsapi.capitalonline.net/vpc'  # 生产
    # NETWORK_URL = 'http://cdsapi-gateway.gic.pre/openapi/vpc'  # 预生产
    action = 'DescribePipeUtilization'
    method = "POST"
    body = {}

    #10000000909w子用户
    # AK = '1c658cd8d10411ec9293b27b4f6749fa'
    # AccessKeySecret = '694e032816f4f3c64a79bf590ee11346'
    # #18600529015主账户
    AK = '38bc80ae369611eaabc00242ac110002'
    AccessKeySecret = '808db82b32e28be06d1879ef0c635f9c'


    url = get_signature(action, AK, AccessKeySecret, method, NETWORK_URL)
    res = requests.post(url, json=body)
    result = json.loads(res.content)
    return result



if __name__ == '__main__':
    a = get_pipe_utilization()
    print(json.dumps(a))
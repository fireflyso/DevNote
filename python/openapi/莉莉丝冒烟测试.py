# -- coding: utf-8 --
# @Time : 2023/10/10 12:00
# @Author : xulu.liu
import base64
import hmac
import sys
import urllib
import uuid
import time
from hashlib import sha1
import requests
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

NETWORK_URL_BASE = "http://cdsapi.capitalonline.net/"
# 线上测试账号
AK = "60ddeed84d3011eea49236c0febc4cd1"
AccessKeySecret = "54fd2f65cb0c36cbb8c1eaa8c1942253"


# 企业微信机器人发送消息
def send_msg():
    url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=5fb529e0-6a95-4033-9741-fd7cdc222f87'
    # 测试机器人
    # url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=fb12e3ab-35bb-4c77-90e5-87928572866f'
    title = '莉莉丝冒烟测试告警（网络组）'
    content = 'OpenAPI DescribeVdc和GetIpInfoBySegment 冒烟测试调用异常，请联系网络组值班人员检查!'
    logger.info('调用企业微信webhook url: %s', url)
    try:
        data_info = {
            "msgtype": "text",
            "text": {
                "content": "首云云监控 {}\n "
                           "监控详情：{}".format(title, content),
                "mentioned_list": ["xulu.liu", "zhiwen.yang", "zhixin.hao", "yong.liu"],
            },
        }
        logger.info('webhook data_info:%s', data_info)
        headers = {'Content-Type': 'application/json;charset=utf-8'}
        res = requests.post(url, data=json.dumps(data_info), headers=headers).json()
        logger.info('企业微信调用结果 : {}'.format(res))
    except Exception as e:
        logger.error("send webhook to weixin failed: {}".format(e))


def percentEncode(str):
    """将特殊转义字符替换"""
    res = urllib.parse.quote(str.encode("utf-8").decode(sys.stdin.encoding).encode("utf8"), "")
    res = res.replace("+", "%20")
    res = res.replace("*", "%2A")
    res = res.replace("%7E", "~")
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
        "Action": action,
        "AccessKeyId": ak,
        "SignatureMethod": "HMAC-SHA1",
        "SignatureNonce": str(uuid.uuid1()),
        "SignatureVersion": "1.0",
        "Timestamp": timestamp,
        "Version": "2019-08-08",
    }
    if param:
        D.update(param)
    sortedD = sorted(D.items(), key=lambda x: x[0])
    canstring = ""
    for k, v in sortedD:
        canstring += "&" + percentEncode(k) + "=" + percentEncode(v)
    stringToSign = method + "&%2F&" + percentEncode(canstring[1:])
    key_bytes = bytes(access_key_secret, "utf-8")  # Commonly "latin-1" or "utf-8"
    data_bytes = bytes(stringToSign, "utf-8")  # Assumes `data` is also a string.
    h = hmac.new(key_bytes, data_bytes, sha1)
    Signature = base64.encodebytes(h.digest()).strip()
    D["Signature"] = Signature
    url = url + "/?" + urllib.parse.urlencode(D)
    print(url)
    return url


def describe_vdc():
    action = "DescribeVdc"
    method = "GET"
    param = {}
    path = '{}/network'.format(NETWORK_URL_BASE)
    url = get_signature(action, AK, AccessKeySecret, method, path, param)
    res = requests.get(url)
    result = json.loads(res.text)
    if result.get('Code', '') != 'Success':
        logger.info(result)
        print(result)
        raise 'OpenAPI action DescribeVdc call failure'


def get_ip_info_by_segment():
    action = "GetIpInfoBySegment"
    method = "POST"
    param = {}
    path = '{}/ccs'.format(NETWORK_URL_BASE)
    url = get_signature(action, AK, AccessKeySecret, method, path, param=param)
    body = {
        "Segment": "10.240.1.0/24",
        "PrivateId": "350d1114-7236-11ee-86a0-2afcdb52245c"
    }
    res = requests.post(url, json=body)
    result = json.loads(res.content)
    if result.get('Code', '') != 'Success':
        logger.info(result)
        print(result)
        raise 'OpenAPI action GetIpInfoBySegment call failure'


if __name__ == "__main__":
    try:
        describe_vdc()
        get_ip_info_by_segment()
        print("{} 测试执行成功！".format(datetime.now().replace(microsecond=0)))
    except Exception as e:
        logger.exception(e)
        send_msg()

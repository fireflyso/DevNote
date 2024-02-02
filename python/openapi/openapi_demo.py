import base64
import hmac
import json
import sys
import urllib
import uuid
import time
from hashlib import sha1

import requests

AK = "abc07d56422e11eea9798e96c407823e"
AccessKeySecret = "b9042f4c207d6b59fdcb9bc99f655928"
NETWORK_URL = "http://cdsapi.capitalonline.net/vpc"
NETWORK_URL_BASE = "http://cdsapi.capitalonline.net/"


# AK = "3254353a425511eea9798e96c407823e"
# AccessKeySecret = "9102ca1c149ff4a923f2ab12a34e38fe"

# 线上测试账号
AK = "38bc80ae369611eaabc00242ac110002"
AccessKeySecret = "808db82b32e28be06d1879ef0c635f9c"


AK = "38bc80ae369611eaabc00242ac110002"
AccessKeySecret = "808db82b32e28be06d1879ef0c635f9c"


# NETWORK_URL = "http://cdsapi-gateway.gic.pre/openapi/vpc"
# NETWORK_URL = "http://openapi.gic.test/vpc"
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



def slb_detail():
    action = "DescribeVpcSlb"
    method = "GET"
    param = {
        "SlbId": "c7dd1256-5066-11ee-b005-4acd0fbc45a5",
        "SlbName": ""
    }
    url = get_signature(action, AK, AccessKeySecret, method, NETWORK_URL, param)
    res = requests.get(url)
    result = json.loads(res.text)
    return result



def query_vpc_slb_rs_port():
    action = "QueryVpcSLBRsPort"
    method = "POST"
    param = {}
    url = get_signature(action, AK, AccessKeySecret, method, NETWORK_URL, param=param)
    body = {
        "ListenId": "e9e2f5da-5202-11ee-ada8-7ef2e53a0a4c",
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
                "RsPortId": "f7ee3806-5202-11ee-ada8-7ef2e53a0a4c",
                "Ip": "10.20.0.7",
                "Port": "10000",
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
        "RsPortIds": ["0a9b247e-56bc-11ee-99b3-7aae9f9135ae"]
    }
    res = requests.post(url, json=body)
    result = json.loads(res.content)
    return result


def create_vpc_slb_rs_port():
    action = "CreateVpcSLBRsPort"
    method = "POST"
    param = {}
    url = get_signature(action, AK, AccessKeySecret, method, NETWORK_URL, param=param)
    body = {
        "ListenId": "cd39c2d8-56e9-11ee-a730-123a7cd7feb8",
        "RsList": [
            {
                "VmId": "ins-m85i3o2sfx25ou08",
                "VmName": "slb-vm",
                "VmPublicIp": "",
                "VmType": "kvm",
                "VmPrivateIp": "10.21.5.1",
                "Port": "8000",
                "Weight": "100"
            },
            {
                "VmId": "ins-b8dgxo4scxx57up8",
                "VmName": "slb-vm",
                "VmPublicIp": "",
                "VmType": "kvm",
                "VmPrivateIp": "10.21.5.0",
                "Port": "8000",
                "Weight": "100"
            }
        ]
    }

    res = requests.post(url, json=body)
    result = json.loads(res.content)
    return result


def create_vpc_slb_listen():
    action = "CreateVpcSLBListen"
    method = "POST"
    param = {}
    url = get_signature(action, AK, AccessKeySecret, method, NETWORK_URL, param=param)
    body = {
        "SlbId": "40fb6312-511c-11ee-99be-8e09f8677b8d",
        "ListenName": "新建监听",
        "Vip": "114.112.38.27",
        "VipId": "91fb5c0a-53b4-11ee-9d9f-feb5ec439909",
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
    method = "POST"
    param = {}
    url = get_signature(action, AK, AccessKeySecret, method, NETWORK_URL, param=param)
    body = {
        "ListenId": "e9e2f5da-5202-11ee-ada8-7ef2e53a0a4c"
    }
    res = requests.post(url, json=body)
    result = json.loads(res.content)
    return result


def update_vpc_slb_listen():
    action = "UpdateVpcSLBListen"
    method = "POST"
    param = {}
    url = get_signature(action, AK, AccessKeySecret, method, NETWORK_URL, param=param)
    body = {
        "SlbId": "1963F28E-3Fc8-11Ee-Baf3-162664D58161",
        "ListenId": "ab24bf50-53b4-11ee-9d9f-feb5ec439909",
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
    action = "DeleteVpcSLBListen"
    method = "POST"
    param = {}
    url = get_signature(action, AK, AccessKeySecret, method, NETWORK_URL, param=param)
    body = {
        "ListenIds": [
            "7fdee0c2-56df-11ee-99c8-d6ae37b9a49b",
            "8b9c0d04-56da-11ee-99c8-d6ae37b9a49b",
            "91d944f0-56d7-11ee-a730-123a7cd7feb8",
            "85bf0cae-56e1-11ee-92b7-caf1c886f483",
            "bc9c88f8-56cf-11ee-99b3-7aae9f9135ae",
        ]
    }
    res = requests.post(url, json=body)
    result = json.loads(res.content)
    return result


def vpc_slb_listen_monitor():
    action = "QueryVpcSlbListenMonitor"
    method = "POST"
    param = {}
    url = get_signature(action, AK, AccessKeySecret, method, NETWORK_URL, param=param)
    body = {
        "ListenId": "e9e2f5da-5202-11ee-ada8-7ef2e53a0a4c"
    }
    res = requests.post(url, json=body)
    result = json.loads(res.content)
    return result


def bandwidth_flow():
    action = "QueryWanFlow"
    method = "POST"
    param = {}
    url = get_signature(action, AK, AccessKeySecret, method, NETWORK_URL, param=param)
    body = {
        "ResourceId": "4eb6e0e6-5089-11ee-ada8-7ef2e53a0a4c"
    }
    res = requests.post(url, json=body)
    result = json.loads(res.content)
    return result


def vpc_slb_monitor():
    action = "DescribeVpcSlbMonitor"
    method = "POST"
    param = {}
    url = get_signature(action, AK, AccessKeySecret, method, NETWORK_URL, param=param)
    body = {
        "SlbId": "f43d3228-55fb-11ee-8573-ca21895e3d63"
    }
    res = requests.post(url, json=body)
    result = json.loads(res.content)
    return result


def describe_vdc():
    action = "DescribeVdc"
    method = "GET"
    param = {}
    path = '{}/network'.format(NETWORK_URL_BASE)
    url = get_signature(action, AK, AccessKeySecret, method, path, param)
    res = requests.get(url)
    result = json.loads(res.text)
    return result


def get_ip_info_by_segment():
    action = "GetIpInfoBySegment"
    method = "POST"
    param = {}
    path = '{}/ccs'.format(NETWORK_URL_BASE)
    url = get_signature(action, AK, AccessKeySecret, method, path, param=param)
    body = {
        "Segment": "10.1.1.0/24",
        "PrivateId": "2fc6cd96-5083-11ee-9fdc-a2c4633796fc"
    }
    res = requests.post(url, json=body)
    result = json.loads(res.content)
    return result


def vdc_list():
    NETWORK_URL = 'http://cdsapi.capitalonline.net/network'
    # NETWORK_URL = 'http://cdsapi-gateway.gic.pre/openapi/network'
    action = 'DescribeVdc'
    method = "GET"
    params = {}
    body = {}
    AK = '38bc80ae369611eaabc00242ac110002'
    AccessKeySecret = '808db82b32e28be06d1879ef0c635f9c'
    url = get_signature(action, AK, AccessKeySecret, method, NETWORK_URL, param=params)
    res = requests.get(url, json=body)
    result = json.loads(res.content)
    return result


def describe_nat_conn():
    action = "DescribeNatConn"
    method = "GET"
    param = {
        "NatId": "290a3276-7fa5-11ee-9732-e2630655970f",
        "StartTime": "2023-11-15 16:31:00",
        "EndTime": "2023-11-15 17:01:01"
    }
    url = get_signature(action, AK, AccessKeySecret, method, NETWORK_URL, param)
    res = requests.get(url)
    result = json.loads(res.text)
    return result


def describe_nat_rule_conn():
    action = "DescribeNatRuleConn"
    method = "GET"
    param = {
        "RuleId": "42adfb9c-7fad-11ee-a711-56418d35492d",
        "StartTime": "2023-11-12 10:00:00",
        "EndTime": "2023-11-16 15:20:00"
    }
    url = get_signature(action, AK, AccessKeySecret, method, NETWORK_URL, param)
    res = requests.get(url)
    result = json.loads(res.text)
    return result


if __name__ == "__main__":
    # res = slb_detail()
    # vpc负载均衡监听服务器端口信息查询    done
    # res = query_vpc_slb_rs_port()
    # vpc负载均衡监听批量修改服务器端口    done
    # res = update_vpc_slb_rs_port()
    # vpc负载均衡监听批量解绑服务器端口    done
    # res = delete_vpc_slb_rs_port()
    # vpc负载均衡监听批量绑定服务器端口    done
    # res = create_vpc_slb_rs_port()

    # 查询vpc负载均衡监听               done
    # res = query_vpc_slb_listen()
    # 更新vpc负载均衡监听               done
    # res = update_vpc_slb_listen()
    # 删除vpc负载均衡监听               done
    # res = delete_vpc_slb_listen()
    # 创建vpc负载均衡监听               done
    # res = create_vpc_slb_listen()

    # vpc slb实时监听告警查询接口
    # res = vpc_slb_listen_monitor()
    # 实时带宽查询接口
    # res = bandwidth_flow()
    # vpc slb实时告警查询接口
    # res = vpc_slb_monitor()

    # vdc详情查看
    # res = describe_vdc()
    # res = get_ip_info_by_segment()

    # nat连接数查询
    # res = describe_nat_conn()
    # nat rule连接数查询
    res = describe_nat_rule_conn()

    print(res)
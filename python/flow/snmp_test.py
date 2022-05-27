#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import copy
import datetime
import json
import logging
import sys

import MySQLdb
import platform
import time
import traceback
from logging.handlers import TimedRotatingFileHandler

import requests
from func_timeout import func_set_timeout as time_out, FunctionTimedOut
from pysnmp.hlapi import *


def bulk_cmd(ip, data_format_func=None, max=25, max_retry=6):
    """
    bulk 批量命令获取信息
    :param oid: oidget dc info except
    :param data_format_func:
    :param max_retry: 当获取异常时，重复次数，默认位3次
    :return: []
    """
    for i in range(max_retry):
        data = []
        for errorIndication, errorStatus, \
            errorIndex, varBinds in bulkCmd(SnmpEngine(),
                                            CommunityData('QAZXSWedc'),
                                            UdpTransportTarget((ip, 161)),
                                            ContextData(), 0, max,
                                            ObjectType(ObjectIdentity('.1.3.6.1.2.1.2.2.1.2')),
                                            lexicographicMode=False):
            # 格式化数据
            print(errorIndication, errorStatus, errorIndex, varBinds)
            value = data_format_func(errorIndication, errorStatus, errorIndex, varBinds)
            if not value:
                # 当有异常时，重新获取
                data = []
                break
            else:
                data.append(value)
        # 当获取数据正常时，返回data
        if data:
            return data
        time.sleep(i + 1)
    # 重试后依然获取失败，返回[]
    return []

def descr_format(errorIndication, errorStatus, errorIndex, varBinds):
    """
    接口描述 数据格式化
    :param errorIndication:
    :param errorStatus:
    :param errorIndex:
    :param varBinds:
    :return:
    """
    descr_dict = {}
    if errorIndication:
        return False
    if errorStatus:
        return False
    for varBind in varBinds:
        line = (' = '.join([x.prettyPrint() for x in varBind]))
        print(line)
        if_descr = line.split('= ')[-1]
        flag = line.split('=')[0].split('.')[-1]
        descr_dict[flag] = if_descr
    return descr_dict

bulk_cmd('114.112.76.117', descr_format)
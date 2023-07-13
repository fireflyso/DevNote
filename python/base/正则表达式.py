# -- coding: utf-8 --
# @Time : 2023/4/10 18:23
# @Author : xulu.liu
import re
import socket


def is_valid_ip_address(ip_address):
    """判断给定的字符串是否是合法的IP地址"""
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    match = re.match(pattern, ip_address)
    if match:
        return True
    else:
        return False


def is_valid_ip(address):
    try:
        print(socket.inet_aton(address))
        return True
    except:
        return False


ip = '192.168.0.01'
print(is_valid_ip_address(ip))
print(is_valid_ip(ip))

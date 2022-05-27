# -*- coding: utf-8 -*-
from socket import *
import logical_port_pb2, port_pb2
import subprocess


def for_logical_usage(message):
    ts = logical_port_pb2.telemetry_top_pb2.TelemetryStream()
    ts.ParseFromString(message)
    device = ts.system_id
    time = ts.timestamp
    for interface_info in ts.enterprise.ListFields()[0][1].ListFields()[0][1].interface_info:
        data = {
            "if_name": interface_info.if_name,
            "init_time": interface_info.init_time,
            "snmp_if_index": interface_info.snmp_if_index,
            "parent_ae_name": interface_info.parent_ae_name,
            "egress_stats.if_packets": interface_info.egress_stats.if_packets,
            "egress_stats.if_octets": interface_info.egress_stats.if_octets,
            "ingress_stats.if_packets": interface_info.egress_stats.if_octets,
            "ingress_stats.if_octets": interface_info.egress_stats.if_octets,
            "device": device,
            "host": "snmp-agent",
            "sensor_name": "jnprLogicalInterfaceExt",
            "time": time
        }
        print(data)


def for_interface(message):
    pass


def for_cpu_memory(message):
    pass


def for_npu_utilization(message):
    ts = port_pb2.telemetry__top__pb2.TelemetryStream()
    ts.ParseFromString(message)
    import pdb
    pdb.set_trace()
    device = ts.system_id
    time = ts.timestamp
    for interface_info in ts.enterprise.ListFields()[0][1].ListFields()[0][1].interface_info:
        data = {
            "if_name": interface_info.if_name,
            "init_time": interface_info.init_time,
            "snmp_if_index": interface_info.snmp_if_index,
            "parent_ae_name": interface_info.parent_ae_name,
            "egress_stats.if_packets": interface_info.egress_stats.if_packets,
            "egress_stats.if_octets": interface_info.egress_stats.if_octets,
            "ingress_stats.if_packets": interface_info.egress_stats.if_octets,
            "ingress_stats.if_octets": interface_info.egress_stats.if_octets,
            "device": device,
            "host": "snmp-agent",
            "sensor_name": "jnprLogicalInterfaceExt",
            "time": time
        }
        print(data)


serverPort = 8888
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
while True:
    message, clientAddress = serverSocket.recvfrom(4096)
    # print('message : {}'.format(message))
    # print('{} -- 接收到一条信息, client address : {}\n'.format(datetime.now(), clientAddress))
    msg = message.decode('utf-8', 'replace')
    try:
        if '/junos/system/linecard/interface/logical/usage/' in msg:
            for_logical_usage(message)
        elif '/junos/system/linecard/interface/' in msg:
            for_interface(message)
        elif '/junos/system/linecard/cpu/memory/' in msg:
            for_cpu_memory(message)
        elif '/junos/system/linecard/npu/utilization/' in msg:
            for_npu_utilization(message)
    except Exception as e:
        print('except : {}'.format(e))

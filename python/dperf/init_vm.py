# -*- coding: utf-8 -*-
# @Time:    2023/4/20 11:23

from threading import Thread
from netmiko import ConnectHandler

server_cmd_list = """
modprobe uio
modprobe uio_pci_generic
ip link set eth1 down
ip link
dpdk-devbind -b uio_pci_generic 0000:00:03.0
ip route add default via 10.20.1.4
""".strip().split('\n')

client_cmd_list = """
modprobe uio
modprobe uio_pci_generic
ip link set eth1 down
ip link
dpdk-devbind -b uio_pci_generic 0000:00:03.0
ip route add default via 10.20.1.4
""".strip().split('\n')

# server_cmd_list = """
# """.split()
#
# client_cmd_list = """
# """.split()


client_list = [
    {'ip': '10.17.1.5', 'port': '22', 'name': ''},
    {'ip': '10.17.1.6', 'port': '22', 'name': ''},
    {'ip': '10.17.1.7', 'port': '22', 'name': ''},
    {'ip': '10.17.1.8', 'port': '22', 'name': ''},
]


server_list = [
    {'ip': '10.20.1.5', 'port': '22', 'name': ''},
    {'ip': '10.20.1.6', 'port': '22', 'name': ''},
    {'ip': '10.20.1.7', 'port': '22', 'name': ''},
    {'ip': '10.20.1.8', 'port': '22', 'name': ''},
]


def send_config_task(vm_info, cmd):
    try:
        connection = ConnectHandler(
            device_type='linux',
            ip=vm_info["ip"],
            port=vm_info["port"],
            username='root',
            password='DB-china123',
            fast_cli=True,
            timeout=60,
            global_cmd_verify=False,
            conn_timeout=60
        )
        output = connection.send_config_set(cmd)
        print(f'{vm_info["ip"]} {output}')
        print('-' * 100)

        connection.disconnect()
    except Exception as e:
        print(f'{vm_info["ip"]} {e}')
        print('-' * 200)


def main():

    thread_list = []
    if server_cmd_list:
        for server in server_list:
            thread = Thread(target=send_config_task,
                            args=(server, server_cmd_list))
            thread.daemon = True
            thread.start()
            thread_list.append(thread)
    if client_cmd_list:
        for client in client_list:
            thread = Thread(target=send_config_task,
                            args=(client, client_cmd_list))
            thread.daemon = True
            thread.start()
            thread_list.append(thread)
    for thread in thread_list:
        thread.join()


if __name__ == '__main__':
    main()
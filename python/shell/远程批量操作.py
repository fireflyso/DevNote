# -- coding: utf-8 --
# @Time : 2023/10/11 16:34
# @Author : xulu.liu
import paramiko
from datetime import datetime


def ssh2(ip, username, passwd, cmd):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, 22, username, passwd, timeout=5)
        for m in cmd:
            print(m)
            stdin, stdout, stderr = ssh.exec_command(m)
            print(stdin, stdout, stderr)
            out = stdout.readlines()
            # 屏幕输出
            for o in out:
                print(o)
        print('%s\tOK\n' % (ip))
        # ssh.close()
    except:
        print('%s\tError\n' % (ip))


if __name__ == '__main__':
    vm_list = [("10.11.8.5", "root", "P@$$w0rd"), ("10.11.8.7", "root", "P@$$w0rd"), ("10.11.8.11", "root", "P@$$w0rd"), ("10.11.8.12", "root", "P@$$w0rd"), ("10.11.132.6", "root", "Z39dmvKA0uR9YLP2"), ("10.11.132.7", "root", "c29fCeCbFqgH0im6"), ("10.11.92.3", "root", "ZStBWSufzaLX64sd"), ("10.11.92.4", "root", "23SiLKT56LIKw822"), ("10.11.8.1", "root", "P@$$w0rd"), ("10.11.8.2", "root", "P@$$w0rd"), ("10.11.8.6", "root", "P@$$w0rd"), ("10.11.112.4", "root", "2njN9DhrY00rfYuf"), ("10.11.8.3", "root", "P@$$w0rd"), ("10.11.8.4", "root", "P@$$w0rd"), ("10.11.112.1", "root", "qUhv9LC25w9wG0Bh"), ("10.11.20.4", "root", "P@$$w0rd"), ("10.11.92.1", "root", "P@$$w0rd"), ("10.11.92.2", "root", "P@$$w0rd"), ("10.11.132.1", "root", "P@$$w0rd"), ("10.11.132.2", "root", "P@$$w0rd"), ("10.11.132.3", "root", "P@$$w0rd"), ("10.11.132.5", "root", "P@$$w0rd"), ("10.11.132.4", "root", "P@$$w0rd"), ("10.11.20.1", "root", "P@$$w0rd"), ("10.11.20.2", "root", "P@$$w0rd"), ("10.11.20.3", "root", "P@$$w0rd"), ("10.11.8.8", "root", "P@$$w0rd"), ("10.11.8.9", "root", "P@$$w0rd"), ("10.11.8.10", "root", "P@$$w0rd"), ("10.11.112.2", "root", "a1eJnSUSYgmtP9Og"), ("10.11.112.3", "root", "hA5I091leRQ8iVhZ")]
    # vm_list = [("10.11.112.1", "root", "qUhv9LC25w9wG0Bh")]
    cmd = ["date -s '20231011 17:34:00'","rm -rf moniter.sh", """
cat>moniter.sh<<EOF
#!/bin/bash
. /etc/profile
url='http://wan-flow-bps.capitalcloud.net/slb_monitor_save'
active_conn=\$(/usr/local/bin/ipvsadm -ln --exact | tr '\\n' '|')
all_conn=\$(/usr/local/bin/ipvsadm -ln --stats --exact | tr '\\n' '|')
frr_status=\$(/usr/bin/vtysh -c "show bgp summary" | grep 100. | tr '\\n' '|')
slb_vm_id=\$SLB_VM_ID
monitor_date=\$(date "+%Y-%m-%d %H:%M:%S")
data='active_conn='\$active_conn'&all_conn='\$all_conn'&slb_vm_id='\$slb_vm_id'&monitor_date='\$monitor_date'&frr_status='\$frr_status
response=\$(echo \$data | curl -X POST \$url -d @-)
EOF
    """, "chmod +x moniter.sh"]
    for vm_info in vm_list:
        now = datetime.now()
        cmd[0] = "date -s '{}{}{} {}:{}:{}'".format(now.year, now.month, now.day, now.hour, now.minute, now.second)
        ip, username, passwd = vm_info
        ssh2(ip, username, passwd, cmd)

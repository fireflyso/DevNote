# -- coding: utf-8 --
# @Time : 2023/10/11 16:34
# @Author : xulu.liu
import paramiko


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
    vm_list = [("148.153.165.14", "root", "2nt58XJWTB4b"), ("148.153.38.78", "root", "2nt58XJWTB4b")]
    # vm_list = [("148.153.165.14", "root", "2nt58XJWTB4b")]
    cmd = [
        "rm -rf /root/lilith_wan_openapi_test/smoke_test.py",
        "mv /root/lilith_wan_openapi_test/smoke_test.py.bak /root/lilith_wan_openapi_test/smoke_test.py"
    ]
    for vm_info in vm_list:
        ip, username, passwd = vm_info
        ssh2(ip, username, passwd, cmd)

    print('开启任务完成!')

import subprocess
import re


def subprocess_popen(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    while p.poll() is None:
        if p.wait() != 0:
            print("命令执行失败，请检查设备连接状态")
            return False
        else:
            re_data = p.stdout.readlines()
            result = []
            re_str = "^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
            for i in range(2, len(re_data)):
                res = re_data[i].decode('utf-8').strip('\r\n')
                if "???" not in res:
                    ip = res.strip().split(' ')[1]
                    delay = res.strip().split(' ')[-4]
                    if re.match(re_str, ip) and delay:
                        result.append((ip, delay))
            return result


cmd = "mtr -c 1 -rn {}".format('122.9.178.4')
result = subprocess_popen(cmd)
print(result)

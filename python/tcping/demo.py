# -- coding: utf-8 --
# @Time : 2023/10/9 18:16
# @Author : xulu.liu
from tcping import Ping
import time
import socket
from functools import partial
from six import print_

iprint = partial(print_, flush=True)


class MyPing(Ping):
    def __init__(self, host, port=80, timeout=1):
        super().__init__(host, port, timeout)

    def ping(self, count=10):
        for n in range(1, count + 1):
            s = self._create_socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                time.sleep(0.1)
                cost_time = self.timer.cost(
                    (s.connect, s.shutdown),
                    ((self._host, self._port), None))
                s_runtime = 1000 * (cost_time)

                iprint("Connected to %s[:%s]: seq=%d time=%.2f ms" % (
                    self._host, self._port, n, s_runtime))

                self._conn_times.append(s_runtime)
            except socket.timeout:
                iprint("Connected to %s[:%s]: seq=%d time out!" % (
                    self._host, self._port, n))
                self._failed += 1

            except KeyboardInterrupt:
                self.statistics(n - 1)
                raise KeyboardInterrupt()

            else:
                self._successed += 1

            finally:
                s.close()

        self.statistics(n)


st_time = time.time()
ping = MyPing('164.52.54.46', 10401, 1)  # 地址、端口、超时时间
ping.ping(10)  # ping命令执行次数
ret = ping.result.table  # 以表格形式展现（ping.result.raw  # 原始形态，ping.result.rows  # 行显示）
print(ping.result.rows[0].host)
print('丢包率: {}%'.format(100 - float(ping.result.rows[0].success_rate.replace('%', ''))))
print('平均延时: {}'.format(ping.result.rows[0].average))
print('执行耗时: {}s'.format(time.time() - st_time))

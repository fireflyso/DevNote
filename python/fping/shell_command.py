# -- coding: utf-8 --
# @Time : 2023/2/13 10:38
# @Author : xulu.liu
# @File : shell_command.py
# @Software: PyCharm
from subprocess import Popen, PIPE, STDOUT
import os
import signal
from func_timeout import func_set_timeout, exceptions
from utils_logger import get_logger

logger = get_logger('shell_cmd', "INFO")


def get_timeout(*args, **kwargs):
    timeout = kwargs.pop('timeout', None)
    return timeout


@func_set_timeout(get_timeout)
def _run(command, res_list, pid_list, timeout=None):
    process = Popen(command, stdout=PIPE, stderr=STDOUT, shell=True, preexec_fn=os.setsid)
    pid_list.append(process.pid)
    with process.stdout:
        for line in iter(process.stdout.readline, b''):
            res_list.append(line.decode().strip())


def exe_command(command, timeout=30):
    """
    封装shell命令的执行，执行超时时强行杀掉shell启的进程，避免资源泄漏，同时会返回已经输出的数据结果
    （具体看命令，部分命令是及时输出结果，有的命令在执行完成后一次性输出结果）
    :param command:需要执行的shell命令
    :param timeout:超时时间
    :return:将命令的返回结果按行写入列表
    """
    res_list = []
    pid_list = []
    try:
        _run(command, res_list, pid_list, timeout=timeout)
    except exceptions.FunctionTimedOut:
        logger.warning('执行超时 : {}'.format(command))
        if pid_list:
            logger.warning('准备kill {}'.format(pid_list[0]))
            os.killpg(pid_list[0], signal.SIGTERM)

    return res_list

from datetime import datetime
import time
import random
# from dask.multiprocessing import get
from dask.threaded import get
from dask.distributed import Client
import logging
from logging import StreamHandler
logger = logging.getLogger(__name__)
handler = StreamHandler()
logger.addHandler(handler)


def log(func):
    def wrapper(*args, **kw):
        print('{} 开始执行...'.format(args[0]))
        st = datetime.now()
        try:
            result = func(*args, **kw)
            print('{} 执行完成...'.format(args[0]))
            print("{} 执行用时 : {}".format(args[0], (datetime.now() - st).seconds))
        except Exception as e:
            print('{} 执行错误 {}'.format(args[0], e))
            result = None

        return result

    return wrapper


@log
def run(info='info', parent='info'):
    print('task : {}, parent : {}'.format(info, parent))
    time.sleep(random.randint(1, 3))
    from clickhouse_driver import Client
    CK_HOST = "10.2.10.27"
    CK_USER = "default"
    CK_PASSWORD = "cds-china"
    CK_PORT = 9000
    client = Client(host=CK_HOST, port=CK_PORT, user=CK_USER, password=CK_PASSWORD)
    client.execute("show databases")

    return '{} - {}'.format(info, parent) if parent else info


dsk = {
    'step01': (run, 'info 01', ''),
    'step02': (run, 'info 02', 'step01'),
    'step03': (run, 'info 03', 'step02'),
    'step04': (run, 'info 04', 'step02'),
    'step05': (run, 'info 05', 'step02'),
    'step06': (run, 'info 06', 'step03'),
    'step07': (run, 'info 07', 'step04'),
    'step08': (run, 'info 08', ['step05', 'step06', 'step07']),
    'step09': (run, 'info 09', 'step08')
}

clent = Client(address="tcp://103.229.214.35:8786")
clent.get(dsk, 'step09')
# res = get(dsk, 'step02')

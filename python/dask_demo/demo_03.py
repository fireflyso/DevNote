from datetime import datetime
import time
import random
# from dask.multiprocessing import get
from dask.threaded import get
from dask.distributed import Client
from dask.graph_manipulation import bind
from dask import delayed
from baijing import utils_logger

logger = utils_logger.get_logger(__name__, "INFO")


def log(func):
    def wrapper(*args, **kw):
        logger.info('{} 开始执行...'.format(args[0]))
        st = datetime.now()
        try:
            result = func(*args, **kw)
            logger.info('{} 执行完成...'.format(args[0]))
            logger.info("{} 执行用时 : {}".format(args[0], (datetime.now() - st).seconds))
        except:
            logger.info('{} 执行错误'.format(args[0]))
            result = None

        return result

    return wrapper

@delayed
@log
def run(info='info', parent='info'):
    logger.info('task : {}, parent : {}'.format(info, parent))
    time.sleep(random.randint(1, 3))
    return '{} - {}'.format(info, parent) if parent else info


# clent = Client(address="tcp://103.229.214.35:8786")
step01 = run('info 01', '')
step02 = bind(run, step01)('info 02')
step03 = bind(run, step02)('info 03', '')
step04 = bind(run, step02)('info 04', '')
step05 = bind(run, step02)('info 05', '')
step06 = bind(run, step03)('info 06', '')
step07 = bind(run, step04)('info 07', '')
step08 = bind(run, [step05, step06, step07])('info 08')
step09 = bind(run, step08)('info 09', '')
# step09.visualize()
step09.compute()
# clent.compute(step09)

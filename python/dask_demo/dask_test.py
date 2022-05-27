from dask.distributed import Client
from time import sleep
from dask import delayed
from datetime import datetime


def inc(x):
    sleep(1)
    return x + 1


def add(x, y):
    sleep(1)
    return x + y


def time_log(func):
    def wrapper(*args, **kw):
        st = datetime.now()
        res = func(*args, **kw)
        print("执行用时 : {}".format((datetime.now() - st).seconds))
        return res

    return wrapper


@time_log
def go():
    data_list = []
    for index in range(10):
        x = delayed(inc)(index)
        data_list.append(x)
    z = delayed(sum)(data_list)
    z.visualize()
    print(z.compute())


if __name__ == "__main__":
    # client = Client()
    go()

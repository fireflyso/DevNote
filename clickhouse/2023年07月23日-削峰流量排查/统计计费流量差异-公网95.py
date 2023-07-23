# -- coding: utf-8 --
# @Time : 2023/7/23 12:18
# @Author : xulu.liu
import os
from clickhouse_driver import Client
import utils_logger
import xlwt
import pymysql


def get_pipe_list():
    pipe_list = []
    with open("public_pipe.out") as file:
        for line in file:
            pipe_list.append(line.replace('\n', ''))
    return pipe_list


def get_old_flow(pipe_id):
    start_time = datetime.strptime(request_params.start_time, '%Y-%m-%d %H:%M:%S')
    end_time = datetime.strptime(request_params.end_time, '%Y-%m-%d %H:%M:%S')

    if start_time > end_time:
        raise ServerException('请选择正确的时间区间')

    result = {"cloud_id": pipe_id, "data_type": '95'}
    out_bps = 0
    in_bps = 0
    value = 0
    client = get_ck_client()
    is_slb_master, pipe_ids = is_slb_pipe(pipe_id)
    if is_slb_master:
        query = "select toStartOfFiveMinute(time) as time, sum(in_bps), sum(out_bps) from {}.{} where pipe_id in " \
                "(%(pipe_list)s) and time >= %(start_time)s and time < %(end_time)s group by time " \
                "order by time;".format(settings.CK_DB_NAME, settings.FLOW_TABLE_NAME)
        params = {
            'pipe_list': pipe_ids,
            'start_time': start_time,
            'end_time': end_time,
        }
        res = client.execute(query, params)
    else:
        query = "SELECT time, in_bps, out_bps FROM {}.{} where pipe_id  = '{}' and time >= '{}' and time < '{}' " \
                "order by time".format(settings.CK_DB_NAME, settings.FLOW_TABLE_NAME, pipe_id, start_time, end_time)
        res = client.execute(query)

    res = [{"time": r[0], 'in_bps': r[1], 'out_bps': r[2]} for r in res]

    if request_params.from_vpc:
        query = "SELECT time, in_bps, out_bps FROM {}.{} where pipe_id  = '{}' and time >= '{}' and time <= '{}' " \
                "order by time".format(settings.CK_DB_NAME, settings.FLOW_TABLE_SECOND_NAME, pipe_id, start_time,
                                       end_time)
        res_second = client.execute(query)
        res_second = [{"time": r[0], 'in_bps': r[1], 'out_bps': r[2]} for r in res_second]
        res_dic = {r['time']: r for r in res}
        for res_data in res_second:
            flow_data = res_dic.get(res_data['time'], {})
            in_bps = res_data.get('in_bps', 0.0) + flow_data.get('in_bps', 0.0)
            out_bps = res_data.get('out_bps', 0.0) + flow_data.get('out_bps', 0.0)
            res_dic[res_data['time']] = {'time': res_data['time'], 'in_bps': in_bps, 'out_bps': out_bps}

        res = [v for k, v in res_dic.items()]
        res = sorted(res, key=lambda e: e.__getitem__('time'), reverse=False)

    num = len(res)
    if num == 0 and end_time - start_time < timedelta(minutes=10):
        result['data'] = [{
            "start_time": str(start_time),
            "out_bps": 0,
            "end_time": str(end_time),
            "value": 0,
            "in_bps": 0
        }]
        return result

    if num == 0 and not pipe_check.is_disable_juniper_pipe(pipe_id=pipe_id):
        logger.error('Request: pipe_id:{} time_start:{} end_time:{},Return Error: found no data in mongodb'.format(
            pipe_id, start_time, end_time))
        raise ServerException('No data found')

    index = int(num * 5 / 100)
    i = 0

    if num != 0:
        res_sort = sorted(res, key=lambda e: e.__getitem__('out_bps'), reverse=True)
        out_bps = res_sort[index]['out_bps']

        res_sort = sorted(res, key=lambda e: e.__getitem__('in_bps'), reverse=True)
        in_bps = res_sort[index]['in_bps']

        if out_bps >= in_bps:
            value = out_bps
        else:
            value = in_bps

    tmp = {
        "in_bps": in_bps,
        "out_bps": out_bps,
        "value": value,
        "start_time": str(start_time),
        "end_time": str(end_time)
    }
    data = [tmp]
    result["data"] = data
    return result


def get_real_flow(pipe_id):
    pass


def set_style(name, height, bold=False):
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = name
    font.bold = bold
    font.color_index = 4
    font.height = height
    style.font = font
    return style


def init_sheet():
    work_book = xlwt.Workbook()
    sheet = work_book.add_sheet('flow data', cell_overwrite_ok=True)
    row0 = ["pipe", "削峰数量", "削峰总带宽(M)", "最大削峰带宽(M)", "限速带宽(M)", "客户id", "客户名称", "节点", "平均超限(M)", "最大超限比例"]
    default_style = set_style('Times New Roman', 220, True)
    for i in range(0, len(row0)):
        sheet.write(0, i, row0[i], default_style)

    return work_book, sheet


def get_db_conn():
    db = pymysql.connect(
        host="write-mysql.gic.local",
        user="resop_20210108",
        password="1snzvbhdEOhfW4LArq$5",
        database="cdscp",
        port=6033,
        charset='utf8'
    )

    return db.cursor()


def get_ck_cilent():
    CK_HOST = "10.13.133.134"
    CK_USER = "flowdata"
    CK_PASSWORD = "wVen6RK3KpkpGdsA"
    CK_PORT = 9000
    client = Client(host=CK_HOST, port=CK_PORT, user=CK_USER, password=CK_PASSWORD)
    return client


if __name__ == '__main__':
    pipe_list = get_pipe_list()
    work_book, sheet = init_sheet()
    ck_client = get_ck_cilent()
    try:
        for pipe_id in pipe_list:
            old_flow_info = get_old_flow(pipe_id)
            real_flow_info = get_real_flow(pipe_id)

    except Exception as e:
        pass
    finally:
        ck_client.disconnect()
    work_book.save('real_flow.xls')

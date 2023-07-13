# -- coding: utf-8 --
# @Time : 2023/2/22 16:34
# @Author : xulu.liu
# @File : IP脏数据清理.py
# @Software: PyCharm
import pymysql
import utils_logger

logger = utils_logger.get_logger('clear_ip', 'INFO')


db = pymysql.connect(
    host="write-mysql.gic.local",
    user="resop_20210108",
    password="1snzvbhdEOhfW4LArq$5",
    database="cdscp",
    port=6033,
    charset='utf8'
)

cursor = db.cursor()

productno_list = ['RBB001565', 'RII001223', 'RII000440', 'RII001048', 'RII001284']
# productno_list = ['RBB001565']
all_id_list = []
except_dict = {}
for productno in productno_list:
    query_sql01 = "select id, name, productNo, status from ucenter.resource where productno='{}';".format(productno)
    _ = cursor.execute(query_sql01)
    res01 = cursor.fetchall()
    temp_suffix = -100
    temp_prefix = '0.0.0'
    except_id_list = []
    history = ()
    for r in res01:
        pid = r[0]
        name = r[1]
        suffix = int(name.split('.')[-1])
        suffix_len = len(str(suffix)) + 1
        prefix = name[:0-suffix_len]
        # 103.244.233
        # 225
        # logger.info('name : {}  前缀 : {}  后缀 : {}'.format(name, prefix, suffix))
        if prefix == temp_prefix and suffix == temp_suffix + 1:
            temp_suffix = suffix
            history = (pid, name)
            if except_id_list:
                except_id_list.append(pid)
            continue

        if except_id_list:
            logger.info('id list : {}'.format(except_id_list))
            all_id_list += except_id_list
            if len(except_id_list) == 1:
                except_id_list.append(except_id_list[0])
            update_sql = "UPDATE ucenter.resource SET customerNo = null, src = null, status = 'unused' WHERE id in {};".format(tuple(except_id_list))
            cursor.execute(update_sql)
            db.commit()
            logger.info(update_sql)
            except_id_list = []

        temp_suffix = suffix
        temp_prefix = prefix
        status = r[3]
        # logger.info('开始校验 : {} {}'.format(pid, name))
        if status == 'assigned':
            # 该IP段已被分配，需要去核对segment表和pipe表数据状态是否合法
            query_sql02 = "select count(b.id) from cloud_pipe_public_segment a, cloud_pipe b where a.address = '{}' and a.is_valid = 1 and a.pipe_id = b.id and b.is_valid = 1;".format(name)
            _ = cursor.execute(query_sql02)
            res02 = cursor.fetchall()
            if res02[0][0] != 1:
                except_dict.setdefault(productno, []).append((pid, name))
                logger.info('异常1 : {} {}  上一组数据  : {}'.format(pid, name, history))
                except_id_list.append(pid)
        else:
            query_sql03 = "select count(*) from cloud_pipe_public_segment where address = '{}' and is_valid = 1;".format(name)
            _ = cursor.execute(query_sql03)
            res03 = cursor.fetchall()
            if res03[0][0] != 0:
                except_dict.setdefault(productno, []).append((pid, name))
                logger.info('异常2 : {} {}  上一组数据  : {}'.format(pid, name, history))

        history = (pid, name)

logger.info(except_dict)
logger.info(all_id_list)





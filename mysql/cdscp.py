# coding=utf-8
# 操作线上库，慎用
import pymysql
import traceback

db = pymysql.connect(
    host="write-mysql.gic.local",
    user="resop_20210108",
    password="1snzvbhdEOhfW4LArq$5",
    database="cdscp",
    port=6033,
    charset='utf8'
)

cursor = db.cursor()
# sql = "DELETE from snmp_customer_flow_analysis where record_date = '2021-07-03 00:00:00'"
# sql = "update subinterface set interface_id = '3c12abf5-11ca-48d4-848a-5665d767d1c6' where subinterface_id = '0237d2b6-d3e5-4184-a7f4-7fd8ea986fe4'"
# sql = "UPDATE `cdscp`.`cloud_pipe` SET `is_valid` = 0 WHERE `id` in ('040294ac-b179-11eb-8931-0242ac110a7c', '5e384938-b225-11eb-88d8-0242ac110a62', '67bbe020-6ce2-11ea-96db-0242ac110002');"
# sql = "UPDATE `cdscp`.`cloud_pipe` SET `status` = 'error' WHERE `id` in ('5ee77714-1517-11e7-87e3-0242ac110002', 'e3a8f0d2-96b7-11e7-9211-0242ac110002')"
# sql = "UPDATE `cdscp`.`cloud_pipe` SET `status` = 'error' WHERE `id` in ('8e360d40-90f7-11e6-8992-0242ac102196', 'c526ccf0-7f6b-11e7-b6b0-0242ac110002')"
# sql = "INSERT INTO `cdscp`.`mn_alarm_event`(`id`, `customer_id`, `flag`, `obj_group_id`, `subject`, `content`, `detail`, `create_time`, `update_time`, `alarm_type`) VALUES ('87b54c48-96db-43af-be5a-0fceeb30e7d4', 'E036042', 1, '07cb50ba-7f46-11ec-8c13-0242ac110002', '高防ip回源带宽监控对象组“lxl-高防IP”流量告警', 'mail_content:高防ip|你好-43.227.197.71|流量异常:回源带宽超过了10Mbps的限制; message_content:高防ip|你好-43.227.197.71|流量异常:回源带宽超过了10Mbps的限制', '{\"alarm_info\": [{\"obj_alarm_detail\": [{\"max_value\": 10, \"verbose_data\": [{\"value_Mbps\": \"11Mbps\", \"value\": \"11836448bps\", \"time\": \"2021-10-08 11:50:09\"}, {\"value_Mbps\": \"11Mbps\", \"value\": \"11824144bps\", \"time\": \"2021-10-08 11:49:08\"}]}], \"obj_name\": \"\\u9ad8\\u9632\", \"obj_id\": \"2081\"}]}', '2022-01-27 18:00:19', '2022-01-27 18:00:19', 1);"

sql = "update cloud_pipe_idc set config = '100m' where id = 128;"
cursor.execute(sql)
db.commit()
cursor.close()
try:
    pass
except:
    db.rollback()
    traceback.print_exc()
finally:
    cursor.close()

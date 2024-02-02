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


sql = "select c.id, c.vlan_name, a.vlan_id, b.interface_name from automatic_product.subinterface a, automatic_product.interface b, cloud_pipe c, cloud_gic_app_network d where a.interface_id = b.interface_id and c.is_valid = 1 and c.cds_resource_id = a.subinterface_id and c.status = 'ok' and c.id = d.pipe_id and d.is_valid = 1;"
_ = cursor.execute(sql)
res = cursor.fetchall()
for r in res:
    if r[1] != "{}.{}".format(r[3], r[2]):
        print("pipe : {}, vlan name: {}, if name : {}, vlan id : {}".format(r[0], r[1], r[3], r[2]))

sql = "select a.id, e.name, a.qos, d.name from cloud_gic a, cloud_gic_app_network b, cloud_app c, cloud_datacenter d, account_customer e where a.is_valid = 1 and a.id = b.gic_id and b.is_valid = 1 and b.app_id = c.id and c.site_id = d.id and a.customer_id = e.id;"
_ = cursor.execute(sql)
res = cursor.fetchall()
gic_id = ''
node_list = []
temp_info = (0,0,0,[])
for r in res:
    if gic_id == r[0]:
        node_list.append(r[3])
        temp_info = r
    else:
        gic_id = r[0]
        print("{}, {}, {}, {}".format(temp_info[0], temp_info[1], temp_info[2], '-'.join(node_list)))
        node_list = [r[3]]
        temp_info = r




sql = ''''''
cursor.execute(sql)
db.commit()

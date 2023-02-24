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


sql = "select * from snmp_register where route_ip = '10.215.122.9';"
_ = cursor.execute(sql)
res = cursor.fetchall()
for r in res:
    print("UPDATE automatic_product.subinterface SET interface_id = 'd5fe5c81-e661-483b-9e65-d76aeb6adc3a' WHERE subinterface_id = '{}';".format(r[0]))


sql = "select id, vlan_id from cdscp.cloud_pipe where cds_resource_id in (select subinterface_id from automatic_product.subinterface where interface_id = '9daa14fe-6b5a-43d0-9add-1d653afae30d' and vlan_id in ('1810','2014','2025','2042','2057','2058','2062','2100','2103','2118','2126','2173','2182','2193','2194','2202','2206','2221','2282','2288','2299','2300','2305','2314','2318','2327','2336','2384','2397','2412','2429','2447','2461','2522','2527','2542','2548','2557','2565','2573','2586','2631','2640','2651','2681','2688','2697','2754','2759','2761','2825','2835','2851','2858','2862','2864','2914','2929','2939','2940','2944','2981','3006','3011','3037','3041','3061','3086','3087','3107','3115','3132','3134','3156','3163','3167','3225','3241','3255','3333','3367','3381','3406','3430','3516','3527','3528','3559','3562','3585','3601','3622','3623','3657','3659','3661','3669','3687','3709','3737','3744','3765','3770','3785','3795','3807','3810','3831','3857','3875','3878','3879','3886','3888','3890','3895','3915','3977','3980')) and is_valid = 1;"
_ = cursor.execute(sql)
res = cursor.fetchall()
for r in res:
    print("UPDATE cdscp.cloud_pipe SET vlan_name = 'Bundle-Ether170.{}' WHERE id = '{}';".format(r[1], r[0]))


sql = "select count(*) from cloud_task where status = 'NEW';"
cursor.execute(sql)
cursor.fetchall()
sql = "delete from fping_prefixes where is_valid = 0;"
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


sql_list = ["UPDATE automatic_product.subinterface SET subinterface_name = 'Bundle-Ether22.2002', interface_id = '96a90d7f-1529-4ed1-aef8-310a407bd589' WHERE subinterface_id = '26d4c8f9-2db5-4454-a2a5-03646e86cb9b';","UPDATE automatic_product.subinterface SET subinterface_name = 'Bundle-Ether22.2420', interface_id = '96a90d7f-1529-4ed1-aef8-310a407bd589' WHERE subinterface_id = '02b8fe2f-dc35-41cc-9364-6158d2f6b885';","UPDATE cdscp.cloud_pipe SET vlan_name = 'Bundle-Ether22.2002' WHERE id = '8b1f7296-eadc-11e7-a364-0242ac110002';","UPDATE cdscp.cloud_pipe SET vlan_name = 'Bundle-Ether22.2420' WHERE id = '08cfefd0-6aa0-11e7-bab8-0242ac110002';"]
for sql in sql_list:
    cursor.execute(sql)




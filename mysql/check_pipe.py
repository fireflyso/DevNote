# coding=utf-8
import pymysql

db = pymysql.connect(
    host="write-mysql.gic.local",
    user="resop_20210108",
    password="1snzvbhdEOhfW4LArq$5",
    database="cdscp",
    port=6033,
    charset='utf8'
)

cursor = db.cursor()

pipe_str = "pipe 5b9b93ee-5e3f-11ec-84f9-325a1a2d6631 flow num 0 2021-12-17 13:30:00 - 2021-12-17 14:00:00 pipe 6b1fd77c-5e39-11ec-9bb1-4af8b597dd82 flow num 0 2021-12-17 13:30:00 - 2021-12-17 14:00:00 pipe 79d133c8-5e3f-11ec-bfc1-da10f2e8ec33 flow num 0 2021-12-17 13:30:00 - 2021-12-17 14:00:00 pipe d3cbf684-e642-11e7-ae72-0242ac11015a flow num 0 2021-12-17 13:30:00 - 2021-12-17 14:00:00"
pipe_list = []
for pipe_info in pipe_str.split('pipe'):
    info_list = pipe_info.split(' ')
    if len(info_list) > 2:
        pipe_list.append("'{}'".format(info_list[1]))

print('告警的pipe ： {}\n'.format(pipe_list))

query = "select id, vlan_name from cdscp.cloud_pipe where id in ({})".format(','.join(pipe_list))
query = "SELECT detail from mn_alarm_event where id = 'ba152bce-7dac-11ec-be26-0242ac110002'"
res = cursor.execute(query)
res_list = cursor.fetchall()

for r in res_list:
    # print("route ip : {}, handle ip: {}, pipe: {}, vlan name: {}\n".format(r[0], r[1], r[0], r[1]))
    print("\n=== 开始分析pipe : {} 的异常情况===".format(r[0]))
    print("   异常情况一：vlan_name冲突（status=33、裸金属影子pipe）")
    # 处理异常情况一
    sql = "SELECT p.id, p.vlan_name, s.interface_id, p.is_valid, p.status from cdscp.cloud_pipe p, automatic_product.subinterface s where p.vlan_name = '{}' and (p.is_valid = 1 or p.status = '33') and s.subinterface_id = p.cds_resource_id".format(r[1])
    one_res = cursor.execute(sql)
    one_list = cursor.fetchall()
    for one_info in one_list:
        sql = "SELECT count(*) from cdscp.bc_bill_resources_price WHERE cloud_id='{}' and end_time>NOW()".format(one_info[0])
        count_res = cursor.execute(sql)
        record_count = cursor.fetchall()[0][0]
        print("      pipe : {}, vlan name : {}, 所属interface : {}, 在计费表中对应的记录数为 : {}, is valid : {}, status : {}".format(one_info[0], one_info[1], one_info[2], record_count, one_info[3], one_info[4]))
        if not record_count:
            print('      pipe : {} 没有对应的计费信息，应该被修改为影子pipe，DML为 :')
            update_sql = "UPDATE `cdscp`.`cloud_pipe` SET `vlan_name` = '{}.shadow' WHERE `id` = '{}';".format(one_info[1], one_info[0])
            print("         {}".format(update_sql))

    print("\n   异常情况二：设备是否添加监控")
    sql = "SELECT e.id as pipe_id, b.route_id, e.vlan_name, e.is_valid as pipe_is_valid, e.`status` as pipe_status, a.* from cdscp.snmp_register a, automatic_product.route b, automatic_product.interface c , automatic_product.subinterface d, cdscp.cloud_pipe e where e.id = '{}' and e.cds_resource_id = d.subinterface_id and d.interface_id = c.interface_id and c.route_id = b.route_id and b.ip = a.route_ip".format(r[0])
    two_res = cursor.execute(sql)
    two_list = cursor.fetchall()
    if two_list:
        print("      pipe : {}, route ip : {}, handle : {}, agent : {}".format(r[0], two_list[0][6], two_list[0][15], two_list[0][14]))
    else:
        sql = "SELECT e.id as pipe_id, b.ip, e.vlan_name, e.is_valid as pipe_is_valid, e.`status` as pipe_status from automatic_product.route b, automatic_product.interface c , automatic_product.subinterface d, cdscp.cloud_pipe e where e.id = '{}' and e.cds_resource_id = d.subinterface_id and d.interface_id = c.interface_id and c.route_id = b.route_id".format(r[0])
        snmp_res = cursor.execute(sql)
        snmp_list = cursor.fetchall()
        print("      pipe : {} 没有对应的监控信息，所属route ip为: {}".format(r[0], snmp_list[0][1]))

    print("\n   异常情况三：是否为测试资源")
    sql = "SELECT b.id, b.name, b.level, b.address from cloud_pipe a, account_customer b where a.customer_id = b.id and a.id = '{}'".format(r[0])
    customer_res = cursor.execute(sql)
    customer_info = cursor.fetchall()[0]
    print("      pipe : {}, 客户ID : {}, 客户名称 : {}, 客户等级 : {}, 地址 : {}".format(
        r[0],
        customer_info[0],
        customer_info[1],
        customer_info[2],
        customer_info[3]
    ))


"""
几种异常情况
1 没有添加监控
2 存在相同的vlan id的pipe状态为33
3 裸金属异常占用（两个pipe使用同一个vlan）
4 资源在设备上不存在，需要问二线
"""
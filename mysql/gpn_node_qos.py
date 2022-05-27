# coding=utf-8
# 统计所有GPN，节点之间的带宽总和
import pymysql
import traceback
import xlwt

def set_style(name, height, bold=False):
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = name
    font.bold = bold
    font.color_index = 4
    font.height = height
    style.font = font
    return style

db = pymysql.connect(
    host="write-mysql.gic.local",
    user="resop_20210108",
    password="1snzvbhdEOhfW4LArq$5",
    database="cdscp",
    port=6033,
    charset='utf8'
)

cursor = db.cursor()
try:
    sql = "SELECT customerno from ucenter.customer WHERE is_valid=1 and custType=1"
    customer = cursor.execute(sql)
    customer_list = cursor.fetchall()
    test_customer_list = []
    for r in customer_list:
        test_customer_list.append(r[0])

    query = "SELECT a.gic_id, b.id, d.city_id, b.qos, e.customer_id FROM cloud_gic_app_network a, cloud_pipe b, cloud_app c, cloud_datacenter d, cloud_gic e, ucenter.customer f WHERE a.is_valid = 1 and a.pipe_id = b.id and a.app_id = c.id and c.site_id = d.id and b.is_valid =1 and c.is_valid = 1 and a.gic_id = e.id and e.is_valid = 1 and f.is_valid = 1 and e.customer_id = f.customerno"
    res = cursor.execute(query)
    res_list = cursor.fetchall()
    print("获取到所有的gpn节点数 : {}".format(len(res_list)))
    gic_dir = {}
    for r in res_list:
        gic_id = r[0]
        node_info = (r[0], r[1], r[2], r[3])
        if r[4] not in test_customer_list:
            gic_dir.setdefault(gic_id, []).append(node_info)

    node_qos_list = []
    for gic_id, node_list in gic_dir.items():
        node_len = len(node_list)
        for index in range(node_len-1):
            core_node = node_list[index]
            for sub in node_list[index+1:]:
                if core_node[2] != sub[2]:
                    node_qos_list.append(
                        [core_node[2], sub[2], min(core_node[3], sub[3]), 1]
                    )

    print("统计到所有的节点连线数量为: {}".format(len(node_qos_list)))
    qos_info_dir = {}
    for node_qos_info in node_qos_list:
        if node_qos_info[3] == 1:
            node_qos_info[3] = 0
            site_one = node_qos_info[0]
            site_two = node_qos_info[1]
            qos_info_dir[(site_one, site_two)] = node_qos_info[2]
            for sub_info in node_qos_list:
                if sub_info[3] == 1 and site_one in sub_info and site_two in sub_info:
                    sub_info[3] = 0
                    qos_value = qos_info_dir.get((site_one, site_two), 0) + sub_info[2]
                    qos_info_dir[(site_one, site_two)] = qos_value

    # print(qos_info_dir)
    print("节点之间的连线去重后数量: {}".format(len(qos_info_dir)))

    sql = "SELECT id, name from cloud_city"
    res = cursor.execute(sql)
    res_list = cursor.fetchall()
    site_dir = {}
    for r in res_list:
        site_dir[r[0]] = r[1]

    default_style = set_style('Times New Roman', 220, True)
    f = xlwt.Workbook()
    sheet = f.add_sheet('GPN节点线路带宽', cell_overwrite_ok=True)
    sheet.write(0, 0, "节点一", default_style)
    sheet.write(0, 1, "节点二", default_style)
    sheet.write(0, 2, "总带宽", default_style)

    row = 1
    total = 0
    for key, value in qos_info_dir.items():
        site_one, site_two = key
        print("{} <-> {} value : {}".format(site_dir.get(site_one, site_one), site_dir.get(site_two, site_two), value))
        sheet.write(row, 0, site_dir.get(site_one, site_one), default_style)
        sheet.write(row, 1, site_dir.get(site_two, site_two), default_style)
        sheet.write(row, 2, value, default_style)
        row += 1
        total += value

    print("total : {}".format(total/1000))

    f.save('GPN带宽信息.xls')

except:
    db.rollback()
    traceback.print_exc()
finally:
    cursor.close()

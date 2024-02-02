import pymysql
db = pymysql.connect(
    host="10.13.103.180",
    user="jichu_wangluo",
    password="VTuzl1iwTTkGNAzc",
    port=7036,
    charset='utf8'
)


cursor = db.cursor()

sql = "select * from cdscp.cloud_slb_vm where id = '00590594-e349-11ed-86a4-72832771a656';"
_ = cursor.execute(sql)
res = cursor.fetchall()
breakpoint()

# nat_list = ['0882df22-5092-11ee-ab57-2a67ec848099', 'd6209520-6675-11ee-ad98-26c88fb1f070', 'aa9754a6-7c7e-11ee-9e30-c6e21f01387d', 'e3447362-5b8e-11ee-a983-3a6a4fd51549', 'c0b45092-4d47-11ee-b005-4acd0fbc45a5', '97580522-8212-11ee-9732-e2630655970f', '873c0738-7d5d-11ee-9e30-c6e21f01387d', '35cc69f0-3826-11ee-abeb-fe156b49c309', '40ff2380-7723-11ee-9d84-f649d446a000', '03550148-442a-11ee-a0d1-c2d95376be84', '40db6fd0-5d0b-11ee-94e1-660920dc2c55', 'b9350510-0a75-11ee-a462-1e4274f3791e', '03bcd96c-7ad5-11ee-9e30-c6e21f01387d', '0aaf8e0e-2b7a-11ee-a212-8edc80ca2126', '4f642298-ed9b-11ed-84eb-228bd07ca645', '98290c28-72e8-11ee-8c96-0a5bd53cc3f9', 'f3375f3e-64b5-11ee-ad98-26c88fb1f070', '1753dae4-432a-11ee-a0d1-c2d95376be84', 'f03a61a2-562b-11ee-ada8-7ef2e53a0a4c', 'bb0f69c6-56f5-11ee-a730-123a7cd7feb8', '82dd77ae-5bb0-11ee-bb54-4e35d34f6fb5', 'c2ba16b2-69ab-11ee-ad98-26c88fb1f070', '9a0d221c-83ab-11ee-9732-e2630655970f', '8f10c1b0-770e-11ee-8686-36239b64feb2', '0e9cf4b8-7fb5-11ee-9732-e2630655970f', 'ce8e784c-7fb4-11ee-a711-56418d35492d', '42bd0962-8448-11ee-a711-56418d35492d', '52420f76-8363-11ee-9d21-7eb59d5caf15', '96c6ea52-785c-11ee-b96a-6e3e4960a152', 'b0cf6350-cc7e-11ed-978a-c673cdcc5c4a', '7cc6a430-7e1a-11ee-b973-9e774d9dc971', '6d5195e2-6186-11ee-ad98-26c88fb1f070', '4cda2f5a-5c3f-11ee-bb54-4e35d34f6fb5', '7f0f05ae-fe07-11ed-b0eb-121ce766340c', 'c488401e-3c1e-11ee-9056-f6ef532488df', '165d57b2-df27-11ed-b120-7eb3022aafd7', '45ee4c08-0a91-11ee-8e26-eebeb738cf86', 'e71bcae6-f3c7-11ed-b7da-e62f4848ef55', 'a97840d0-6e3c-11ee-94e1-660920dc2c55']
#
# for nat_id in nat_list:
#     sql = "select id, updated_at, gic_resource_id from coreTasker.workflows where workflows.params like '%{}%' and workflow_type like 'bandwidth_bind_nat%' order by created_at desc limit 1;".format(nat_id)
#     _ = cursor.execute(sql)
#     res = cursor.fetchall()
#     if res:
#         update_time = res[0][1]
#         bandwidth_id = res[0][2]
#         # print('nat : {} 绑定记录: {}  {}'.format(nat_id, bandwidth_id, update_time))
#         sql_str = "INSERT INTO cdscp.cloud_os_eip_bandwidth_log (eip_id, bandwidth_id, start_time, end_time) VALUES ('{}', '{}', '{}', '2099-01-01 00:00:00');".format(nat_id, bandwidth_id, update_time)
#         print(sql_str)

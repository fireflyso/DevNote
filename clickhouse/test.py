import xlwt
import requests
import json

def set_style(name, height, bold=False):
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = name
    font.bold = bold
    font.color_index = 4
    font.height = height
    style.font = font
    return style

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


pipe_list = ["f7ffde5a-1fe1-11ea-bd0d-0242ac110002","79670672-f08e-11e9-8bb8-0242ac110002","33fd7038-2b96-11ea-b3db-0242ac110002","a0af4240-af26-11ec-953f-b6ffb62b2d07","a0af4240-af26-11ec-953f-b6ffb62b2d07","19e82786-1219-11ec-ae5a-0e21d3d5e04b","8047d220-43a0-11ec-92f1-9ee878f57083","30f8579c-20d6-11ea-9eba-0242ac110002","30f8579c-20d6-11ea-9eba-0242ac110002","d5093bb8-d350-11e9-b100-0242ac110002","d5093bb8-d350-11e9-b100-0242ac110002","24f1eb20-6ce4-11ea-bf7f-0242ac110002","649b13ac-5bc4-11ec-a2f3-5a154554716b","59f736f4-9c00-11ea-a783-f206082eadb4","58c6f0b0-5349-11ec-8a87-76560cfccef3","2fa48642-a32c-11ec-a97b-2681d6fc0182","7a9c9682-5516-11ea-a81a-0242ac110002","82e29bf0-e041-11ea-ae2d-365a63752e95","2f1e8606-8438-11ea-bfa7-0242ac110002","a99bf9ac-4e3d-11eb-858f-feae5cb8da3e","b04d5870-3e7c-11eb-9ba4-0242ac110002","f929eafa-82e7-11ea-8c7d-0242ac110002","3883e952-6d9f-11ea-9304-0242ac110002","b078cc54-8f9e-11ea-b319-e617272e3fc8","b078cc54-8f9e-11ea-b319-e617272e3fc8","da3b41d8-2a1d-11eb-97e8-0242ac110002","75bc759c-6203-11eb-8ed5-66fe387cdac7","3934fe82-83e1-11eb-97cf-eaa94a9340c5","1e59dd4a-fe3d-11eb-bf0a-6a40c175bc98","4de911d2-5ccc-11ec-90e9-3260887fa0d0","322f3798-ede9-11eb-a1b7-de0e3bfd2161","24f052b2-21c2-11ec-b8c8-8a28aec97c17","1efb94c8-f0ec-11ea-8628-0242ac110002","6a16c824-ed90-11ea-a343-c6b77dd10367","cebdf8cc-cf7f-11e9-82a3-0242ac110002","4fb49b62-dd39-11ea-b9c0-0242ac110002","9a0334b4-1446-11eb-a387-ca0633cb5575","f2074ffa-dc61-11ea-a6ce-0242ac110002","fa7feb10-7965-11ea-a080-0242ac110002","bc5aa1e8-e398-11ea-a3f9-0242ac110002","e12f9ffe-968b-11eb-a3a5-5650210ee312","e6349482-0c2f-11eb-830c-0242ac110002","e6349482-0c2f-11eb-830c-0242ac110002","2e4cf3ca-0c5a-11eb-a656-0242ac110002","436569cc-0f75-11eb-8910-0242ac110002","436569cc-0f75-11eb-8910-0242ac110002"]
f = xlwt.Workbook()
row0 = ["pipe id", "ip清单", "入流量(M)", "出流量(M)"]
default_style = set_style('Times New Roman', 220, True)
sheet = f.add_sheet("sheet1", cell_overwrite_ok=True)
for i in range(0, len(row0)):
    sheet.write(0, i, row0[i], default_style)

index = 1
for pipe_id in pipe_list:
    print("查询pipe : {}".format(pipe_id))
    mysql_query = "select address, mask from cloud_pipe_public_segment where pipe_id = '{}' and is_valid = 1;".format(pipe_id)
    cursor.execute(mysql_query)
    res = cursor.fetchall()
    segment_list = ['{}/{}'.format(r[0], r[1]) for r in res]

    post_data = {
        "start_time": "2022-04-01 00:00:00",
        "end_time": "2022-05-01 00:00:00",
        "cloud_id": pipe_id
    }
    res = requests.post('http://wan-flow-bps.gic.pre/bps_95', post_data)
    res = json.loads(res.content)

    sheet.write(index, 0, pipe_id, default_style)
    sheet.write(index, 1, ', '.join(segment_list), default_style)
    sheet.write(index, 2, round(res.get('data')[0].get('in_bps')/1000/1000, 3), default_style)
    sheet.write(index, 3, round(res.get('data')[0].get('out_bps')/1000/1000, 3), default_style)
    index += 1

f.save('test.xls')

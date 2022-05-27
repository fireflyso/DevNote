from clickhouse_driver import Client
import xlwt

CK_HOST = "10.13.133.134"
CK_USER = "flowdata"
CK_PASSWORD = "wVen6RK3KpkpGdsA"
CK_DB_ANME = "flow_snmp"
CK_PORT = 9000
client = Client(host=CK_HOST, port=CK_PORT, user=CK_USER, password=CK_PASSWORD)

def set_style(name, height, bold=False):
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = name
    font.bold = bold
    font.color_index = 4
    font.height = height
    style.font = font
    return style

# pipe_list = ['7186ef0a-4573-11ea-85aa-0242ac110002', 'f19e8cd4-3abe-11eb-9ba4-0242ac110002', '0c4f3a92-3eb6-11eb-9ba4-0242ac110002']
pipe_list = ["1c79a138-7a33-11eb-97cf-eaa94a9340c5","18d12120-7df2-11ea-840b-f60cf64db9de","acb7e10e-5ebf-11eb-9d1a-82a8900ceb71","c834fe38-d338-11eb-a7e1-2263a554bfe3","20d00f72-1f36-11eb-851e-0242ac110002","f77423ba-9e61-11eb-8ea9-1a0f201a18dc","a1f8bef2-fe5e-11eb-a555-464d033b5fd1","29a0c35c-63e1-11e8-a6d1-0242ac110002","6e4e093e-2a34-11ec-92c6-4aa9b5806a6a","748bf3dc-3e39-11e8-8607-0242ac110002","a513987a-3c6e-11ec-ad5f-aa9751aacb94","1c1ba34c-b472-11e7-9c3c-0242ac110002","995654d6-8621-11eb-991c-3a855a2ea340","b59036f0-3fdb-11e9-ab53-0242ac110002","0ce33d50-900b-11ea-8948-0242ac110002","1b0a0e4a-febc-11e8-9d33-0242ac110002","26b5a4d0-4fea-11eb-a34c-0242ac110002","7bb53eba-894a-11ec-89d8-9279f52b6172","6c4835b6-3aa2-11ea-8f7f-0242ac110002","f35bf148-0ec6-11eb-955d-0242ac110002","5d2545ee-4dbd-11ec-9fa7-b6e127184f5c","f2b64b68-6c39-11e7-bab8-0242ac110002","7c5f7a64-f0d1-11ea-8348-0242ac110002","28ea1f3c-4975-11ea-bfc9-0242ac110002","5bdef7f4-b220-11eb-89b9-beb21d25212f","58319a12-2977-11eb-ab9d-0242ac110002"]
f = xlwt.Workbook()
row0 = ["pipe id", "时间", "入流量(M)", "出流量(M)"]
default_style = set_style('Times New Roman', 220, True)

index = 1
for pipe_id in pipe_list:
    print("查询pipe : {}".format(pipe_id))
    sheet = f.add_sheet("sheet{}".format(index), cell_overwrite_ok=True)
    index += 1
    for i in range(0, len(row0)):
        sheet.write(0, i, row0[i], default_style)

    sql = "select time, in_bps, out_bps from flow_snmp.flow_data where pipe_id = '{}' and time >= '2022-02-01 00:00:00' and time < '2022-03-01 00:00:00' order by time".format(pipe_id)
    data_list = client.execute(sql)
    row = 1
    for data in data_list:
        sheet.write(row, 0, pipe_id, default_style)
        sheet.write(row, 1, str(data[0]), default_style)
        sheet.write(row, 2, round(float(str(data[1]))/1000/1000, 2), default_style)
        sheet.write(row, 3, round(float(str(data[2]))/1000/1000, 2), default_style)
        row += 1

f.save('test.xls')

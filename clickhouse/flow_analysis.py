from clickhouse_driver import Client

CK_HOST = "10.13.133.135"
CK_USER = "flowdata"
CK_PASSWORD = "wVen6RK3KpkpGdsA"
CK_DB_ANME = "flow_snmp"
CK_PORT = 9000
client = Client(host=CK_HOST, port=CK_PORT, user=CK_USER, password=CK_PASSWORD)


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

info_list = client.execute("select pipe_id, out_bps from flow_snmp.flow_data where pipe_id in ('af0f71b8-ba37-11ec-a414-c66285652eaa','35631dca-300f-11e9-8d22-0242ac110002','b9c15012-c087-11ec-87fd-6e0d4b982ad5','3c6d58aa-fe76-11eb-aba8-0e16eef25193','14793edc-ee5e-11ea-9587-4226b22ceef4','bdad5608-331a-11ec-b427-4a2c9149e281','16466b60-bcd4-11ea-b26a-fa7ae99f6685','0f88af96-c604-11ec-bd1b-5e0e8ae9f52e','f1a4cc10-4481-11e8-b6c5-0242ac110002','3b59c7e2-a2f0-11ea-b713-0242ac110002','961aef60-6d4e-11ec-b2af-0e89447b8ee2','7c3a60da-eef7-11e9-9e64-0242ac110002','415c7a9a-1c95-11ea-a9ba-0242ac110002','f5118f6c-b9cf-11ea-9e09-0242ac110002','84c9d4ea-25c4-11e8-9afd-0242ac110002','743c3094-d0b7-11e7-94b2-0242ac110002','2a8374b2-528e-11e9-8e14-0242ac110002','29e7558a-a176-11e6-9857-0242ac102197','3fb4b690-c39f-11e7-b642-0242ac110002','c420571e-38f4-11ea-8f7f-0242ac110002','a86111b8-7076-11e9-ac6c-0242ac110002','470babaa-9e4f-11ea-b9e5-0242ac110002','455963fc-a79d-11ec-bab2-92baa902f4a8','21a04382-91ef-11eb-9309-fef0d1d18793','38eb5eb8-bddf-11e9-a5c5-0242ac110002','2153a04a-dcb7-11ec-8818-4e297d7cbb7c','f4dc24b0-ee61-11e9-842c-0242ac110002','d4f9f46e-4357-11eb-bd48-b6a066c5fc94','89b223ac-aed1-11ea-ba46-0242ac110002','caf7a132-6807-11e9-98a2-0242ac110002','641dc508-bf7c-11eb-87c0-6a633d0575d8','6cca842e-90a9-11e9-8baf-0242ac110002','18d3ce2a-629a-11ea-87f6-0242ac110002','c9537582-c087-11ec-a176-12ba9996a4f9','21c0ce8e-d532-11e9-97aa-0242ac110002','1180a216-32fe-11ec-a626-02e12117a9dc','2b6f9a6a-4033-11eb-91ab-0242ac110002','e39ce8f0-3217-11ec-be89-32f298f4feb1','1b2e1a04-3b71-11ea-8a95-0242ac110002','f5251e88-b9cf-11ea-bdee-0242ac110002','1a26484e-fe65-11eb-a02b-1e38f27fdb02','648bb36e-1b28-11ea-bd0d-0242ac110002','f451075e-851a-11ea-b7e7-0242ac110002','e9396cf2-4d2e-11ec-af2d-62e96eb38216','e4a116f6-6923-11e8-bcfc-0242ac110002','3b41135e-94cc-11e6-a16d-0242ac100602','8f5d5aca-43f9-11eb-865b-0242ac110002','87908d4e-5516-11ea-85aa-0242ac110002','a6538cb8-e026-11ea-b7ba-0242ac110002','7937420e-4f2b-11e7-afad-0242ac110002','c75d9e74-de68-11e8-aa43-0242ac110002','2afc35d8-d6a0-11e8-8c1b-0242ac110002','6c174044-d6a0-11e8-a2b0-0242ac110002','b04ac69e-96ff-11e9-8baf-0242ac110002','72db559e-fbe0-11e9-9a34-0242ac110002','bb954226-4c25-11ec-ba13-e24155c2136f','42adf544-6639-11e9-8806-0242ac110002','913667b8-e954-11e7-a664-0242ac110002','317d5ad6-c899-11e9-8f2e-0242ac110002','ec0886ca-b406-11e9-8e60-0242ac110002','3974706c-6ed7-11ec-962c-52f1064b3d9b','202905b6-bcb2-11e9-b67a-0242ac110002','20914228-cc07-11e6-9980-0242ac110002','27f8921a-1ad4-11e8-b6dd-0242ac110002','f3f30c94-6cba-11ea-ad23-0242ac110002','0167e2ae-e942-11e7-89e5-0242ac110002','1508ea5c-3735-11e7-8860-0242ac110002','cd0e6f62-ba7e-11ea-93c0-2e8aec4f3b6c','3aebcbb2-26b7-11ea-9782-0242ac110002','117f0e62-593c-11ea-9d4e-0242ac110002','08c47a06-6924-11ec-a6a9-b240c10b0009','4c8ffe10-8098-11eb-ba2a-a211abb5865e','1bf402e4-7255-11ea-ac48-7a1ae9c5896b','7093d29e-e054-11ea-ac27-0242ac110002','512260a0-1bad-11e9-9f85-0242ac110002','02026ecc-9f92-11ec-903c-e22a7879871b','560de562-a372-11ec-b22f-2e41545e0d04','93989340-d6ff-11e6-b3d4-0242ac110002','258e4f36-8a1c-11ec-b1ed-4e829e0439ab','7484117c-bca1-11ec-a860-72f82dc1dc46','4f76ac9c-2b9c-11e6-871e-0050569b1b91','cb483cd4-817b-11eb-b015-1e5aa05ba8f7','a3b292ec-6485-11e9-8806-0242ac110002','c26d525c-93b3-11ec-bf7e-e2c0ad57d64b','44c25cb6-80f7-11e9-932a-0242ac110002','0fcad918-8961-11e8-b50e-0242ac110002','7d0c80d0-6dd8-11ec-84e7-2a91651dd208','62e1c300-54f0-11e8-9955-0242ac110002','e313d0c8-1e13-11e7-87e3-0242ac110002','79a431d8-79f0-11e9-8e8a-0242ac110002','ca8690d0-9ea3-11eb-ae3d-768e7352a735','18a5bf78-1aac-11e7-ac87-0242ac110002','c404177a-38f4-11ea-b4bf-0242ac110002','25f6cfe0-8108-11e9-86af-0242ac110002','3550a17e-b0b6-11ec-9b45-56b99978e07b','2e3f66d2-a5dd-11e8-b54b-0242ac110002','dbff190e-93c1-11ec-9d9e-52194df22c9a','6c1b8e60-9e2d-11e9-be55-0242ac110002','61dd3544-4353-11eb-9ba4-0242ac110002','23130c80-b7fb-11ec-a790-769e29ec26b5','05bbabb2-de9b-11e7-8fb1-0242ac110002','f235dc3e-1861-11ec-a5f1-42330aefd4e3','503a8f3a-3dea-11eb-9ba4-0242ac110002','17805552-d58a-11eb-9be5-6a32d350c612','9a100f18-af31-11ec-b8a6-d657ade4c296','d4ead5de-771d-11eb-9236-aa0939aaab3a','dfc53cc0-884e-11e9-907a-0242ac110002','69f04f9a-80f0-11e9-a0f4-0242ac110002','37c23d46-2314-11ea-ae07-0242ac110002','76c51d3c-82b0-11ea-9fe7-8e27766fe61a','c22016d8-74d1-11e6-b7a7-0242ac103690','4a236d2a-1766-11ea-bbad-0242ac110002','4587d48c-69cb-11eb-8198-dacdf26e1c91','fb9a529c-6e2c-11e8-8125-0242ac110002','0a061284-87b8-11ea-b58c-f653e1b3e322','a79e7af4-16a0-11ec-8e12-16cc13125ce8','d86064f0-9ef0-11ea-8bc7-0242ac110002','fc07094e-3e1a-11e6-9184-0050569b1b91','e15768ea-9f54-11ec-a908-aa07576076e6','97874ef2-d9f3-11e9-b701-0242ac110002','446daa58-0580-11ec-b933-068953fe9429','4d9404f2-ec2f-11eb-a613-525153309411','58d9dfba-5952-11ea-b87c-0242ac110002','a67e09a2-a6c7-11ec-b69c-029fc8c1ad04','9f0bded8-7141-11e9-a5ea-0242ac110002','891b6508-c6a3-11e6-8ad6-0242ac110002','8f96c01c-d095-11ea-91c8-0242ac110002','29cc35f2-77c0-11e9-8e8a-0242ac110002','874cd6d6-c0c7-11ea-a149-0242ac110002','62f265e8-2928-11e6-8b5d-0050569b1b91','91bb0e06-7e7d-11ec-93c7-4a04fecb13de','c110239a-c987-11e6-8ad6-0242ac110002','9a8b8ab8-44f1-11eb-83c1-5e62c83e5908','9e3ddefc-cf4e-11ec-93f5-561b183afaf1','97de01ea-c3ad-11e9-b373-0242ac110002','6b9b12a4-85cb-11ea-bd98-7207da4452b9','0ff53a00-e258-11e8-9eee-0242ac110002','63e9dd00-286f-11e6-8a38-0050569b1b91','9e57d440-a8c8-11eb-bf03-f63f7e4eb1c1','21e40b56-4403-11eb-9c9b-0242ac110002','e73f22d4-7874-11e9-9774-0242ac110002','15934020-6384-11ea-ba02-0242ac110002','c7ad821e-4133-11ec-aa56-4eb24abdae64','436dacb2-fa2d-11e9-9a34-0242ac110002','795aed56-fb31-11eb-844a-120c1bbf1f19','e13c228e-1afd-11ea-884e-0242ac110002','4fe32f8e-6543-11e7-bab8-0242ac110002','c6067eea-b18e-11ec-aaac-5e0b60d0c8ba','be35222a-c444-11ec-a49e-fe3d5eb3c7c2','bc137752-dcbe-11ec-940a-f265a347c968','cb6d0b58-c3a7-11ec-b908-0242ac1100bd','d7771f88-c3a7-11ec-a7b8-0242ac1100b8','71e372b2-4b65-11ec-964b-dab0cc25944f','62dadf5a-769c-11e7-b6b0-0242ac110002','51f55622-0f31-11ea-8878-0242ac110002','631c8a60-05e0-11ea-95ca-0242ac110002','a1ca69f4-2b9a-11e6-af6b-0050569b1b91','5739fa70-2e39-11eb-a8c2-0242ac110002','d01d6874-5a38-11ec-84f9-325a1a2d6631') and time = '2022-05-28 16:10:00' order by out_bps desc limit 20")
for info in info_list:
    pipe_id = info[0]
    sql = "select a.id, a.name, c.id, c.gpn_name, d.name from cloud_pipe a, cloud_gic_app_network b, cloud_gic c, account_customer d where a.id = '{}' and a.id = b.pipe_id and b.gic_id = c.id and a.customer_id = d.id;".format(pipe_id)
    _ = cursor.execute(sql)
    res = cursor.fetchall()[0]
    text = '{}, {}, {}, {}, {}, {}'.format(info[0], round(info[1]/1000/1000, 2), res[1], res[2], res[3], res[4])
    print(text)
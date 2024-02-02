import requests
headers = {'Cookie': 'csrftoken=MJy5nloIiolVAYgC9OVoI7rDLPRr8uNSzC890pEPNko0fdpM8XqlhzO4oi9hakPt; sessionid=9um5mlpikcv4clgbwcfgxy9relka7epa'}
for n in range(100):
    res = requests.post('http://10.13.2.133:7722/api/flow/device_detail_flow/?route_id=c789563e-8f85-4016-883f-cfc5b24d14e0&date=2022-07-12+05:46:03', headers=headers)
    url = 'http://10.13.2.133:7722/api/flow/device_detail_flow'
    content = {
        "data1": 11
    }
    requests.post(url, json=content)
    print('第 {} 次请求，status : {}, 结果长度为 : {}'.format(n, res.status_code, len(res.content)))
import requests

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    'Cookie': 'cds-token=8c7dc79242a658c2dbdac5d9531f26fc55234ca45902fe066a155dbe1abcbb71;SESSION_TOKEN=xhhhnegvijlgq30d3yhaqm47lk4qos53'
}
data = {"product_id": 11, "compare_id": 16, "keyword": 1539, "start_time": "2023-03-05 15:01:46",
        "end_time": "2023-03-06 15:01:46", "compare_type": "operator"}
url = 'http://localhost:8020/api/visualization/ip_compare/search_data'
res = requests.post(url=url, data=data, headers=HEADERS)

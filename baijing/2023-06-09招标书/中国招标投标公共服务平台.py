# -- coding: utf-8 --
# @Time : 2023/6/8 18:13
# @Author : xulu.liu
import requests
import json
from baijing import utils_logger
import time
import random

logger = utils_logger.get_logger('baijing', 'INFO')
keyword_list = ['IDC', '数据中心', '智算中心', '超算中心']
url = 'http://www.cebpubservice.com/ctpsp_iiss/searchbusinesstypebeforedooraction/getStringMethod.do'
business_type_list = ['招标公告', '开标记录', '评标公示', '中标公告', '签约履行']

for keyword in keyword_list:
    for business_type in business_type_list:
        logger.info('开始抓取关键字 : {}, 分类 : {}'.format(keyword, business_type))
        data = {
            "searchName": keyword,
            "searchArea": "",
            "searchIndustry": "",
            "centerPlat": "",
            "businessType": business_type,
            "searchTimeStart": "",
            "searchTimeStop": "",
            "timeTypeParam": "",
            "bulletinIssnTime": "",
            "bulletinIssnTimeStart": "",
            "bulletinIssnTimeStop": "",
            "pageNo": "1",
            "row": "15"
        }
        proxies = {
            'http': 'socks5://admin:admin@164.52.47.110:8081',
            'https': 'socks5://admin:admin@164.52.47.110:8081',
        }
        HEADERS = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Connection": "keep-alive",
            "Content-Length": "264",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": "_uab_collina=168621853190673111376633; Hm_lvt_ef2114bed21175425a21bb8a1e40ebdf=1686218531; Hm_lpvt_ef2114bed21175425a21bb8a1e40ebdf=1686223307; JSESSIONID=B47C0D077D000688B904FCE9B6EA545F; route=8636ec056e4da7b4e2eea437c76697c0; BSFIT_EXPIRATION=1686297602555; BSFIT_DEVICEID=GkygBQWchSVwU7Ch6QYuqC-OeCTGiTu19DvwIFsuvF9nQ1bwncdZ8UGWyFYzeIXugFtmFqZOE11UrJFYaVfDJjFRBiHwXj9ThNlrasK_KF0ecOBa__E-Uuexn1qXjd6nSPrWLJ971WMc4Da5Lqzk--07E3-IIdTZ; __ts=1686220698004; BSFIT_+5kC1=pJ84EXhTpCtT6CtTEw,pC1Q6J1wpCpwpe; acw_tc=2760777416862233058414096e0ac6cff3d56ff0b3ba40ad3f2e3ade682c7d; cmsurl=/../../index.shtml; __ts=1686223307427; ssxmod_itna=YqAhD5Y57IO9q0d4YIYP7uxMFdDQDcmGpC67Cx05a7eGzDAxn40iDtP=wlP=l=YnvqDUrp0PHblwc0NjF/mDrQf4ff5hYD84i7DKqibDCqD1D3qDk/SxYAkDt4DTD34DYDihQSn9oVPDHDGPVQT=lDi3Db2tDf4DmDGYMGqDgS4DB+xGn/4GgjqqiYeGv0lj2Iut4Dm4PaxtDzdFDtd6u3Q0l9T6CxW2YDrPi+AvQ+YeFFG4PYBwP0iLxbDApY++xjG4ITBD5KAAd3FlNDD33/0464rD; ssxmod_itna2=YqAhD5Y57IO9q0d4YIYP7uxMFdDQDcmGpC67DnFSiRxDsWqDyixjbc+ZDKxK9LN9DnR6xX38TBrh4HeWgtAoOK6Sbmy09WfifiPbxjnmoq=/f6vCTT7f2jFrNv=1gcdqX//MRTUpYZSqLVS8iRnRiDV+N4TQ=Y6TYG0d2OKw+3Ku=UCL0YgMLNpnK2BSErgRnAFuXek=j=vL0axnFeNQRWu=UkcZ2OxUbzyprFM6WbVpyK6gjh13PDKkGiIEI7e3h80gqwjKk3UOMkY0kk0Bb34LDQSF5O0Bw7UrKszyIqtDGcDijgVicYHievSjFQjIDD==; BSFIT_+5kC1=pJ84EXhTpbpbpJeWp+,pC+dEb1wpCNwpN,pC1TEC8wpCNwpw",
            "Host": "www.cebpubservice.com",
            "Origin": "http://www.cebpubservice.com",
            "Referer": "http://www.cebpubservice.com/ctpsp_iiss/searchbusinesstypebeforedooraction/getSearch.do",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.58",
            "X-Requested-With": "XMLHttpRequest"
        }
        total_page = 1
        page_num = 1
        while page_num <= total_page:
            try:
                data['pageNo'] = str(page_num)
                res = requests.post(url, data=data,  timeout=10, headers=HEADERS)
                page_num += 1
                time.sleep(random.randint(1, 3))
                res_data = json.loads(res.content)
                info_list = res_data['object']['returnlist']
                total_page = res_data['object']['page']['totalPage']
                logger.info('共计 {} 页，当前第 {} 页'.format(total_page, page_num))
                for info in info_list:
                    logger.error('{}, {}, {}, {}, {}, {}'.format(
                        info['businessObjectName'], info['receiveTime'], info['regionName'], business_type,
                        info['businessObjectName'], info['transactionPlatfName']
                    ))
            except Exception as e:
                logger.warn(e)

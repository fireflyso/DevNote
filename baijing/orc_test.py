#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import urllib2
import base64


def get_img_base64(img_file):
    with open(img_file, 'rb') as infile:
        s = infile.read()
        return base64.b64encode(s)


def predict(url, appcode, img_base64, kv_config, old_format):
    if not old_format:
        param = {}
        param['image'] = img_base64
        if kv_config is not None:
            param['configure'] = json.dumps(kv_config)
        body = json.dumps(param)
    else:
        param = {}
        pic = {}
        pic['dataType'] = 50
        pic['dataValue'] = img_base64
        param['image'] = pic

        if kv_config is not None:
            conf = {}
            conf['dataType'] = 50
            conf['dataValue'] = json.dumps(kv_config)
            param['configure'] = conf

        inputs = {"inputs": [param]}
        body = json.dumps(inputs)

    headers = {'Authorization': 'APPCODE %s' % appcode}
    request = urllib2.Request(url=url, headers=headers, data=body)
    try:
        response = urllib2.urlopen(request, timeout=10)
        return response.code, response.headers, response.read()
    except urllib2.HTTPError as e:
        return e.code, e.headers, e.read()


def demo():
    appcode = '7c500d6445de4645aea579321355a6e3'
    url = 'https://form.market.alicloudapi.com/api/predict/ocr_table_parse'
    img_file = '/Users/liuxulu/Downloads/test.jpg'
    # 如果输入带有inputs, 设置为True，否则设为False
    is_old_format = False
    config = {'format': 'xlsx', 'finance': False, 'dir_assure': False}
    # 如果没有configure字段，config设为None
    # config = None

    img_base64data = get_img_base64(img_file)
    stat, header, content = predict(url, appcode, img_base64data, config, is_old_format)
    if stat != 200:
        print('Http status code: ', stat)
        print('Error msg in header: ', header['x-ca-error-message'] if 'x-ca-error-message' in header else '')
        print('Error msg in body: ', content)
        exit()
    if is_old_format:
        result_str = json.loads(content)['outputs'][0]['outputValue']['dataValue']
    else:
        result_str = json.loads(content)

    with open('output.xlsx', 'wb') as fout:
        fout.write(base64.b64decode(result_str['tables']))

    print(result_str)


if __name__ == '__main__':
    demo()

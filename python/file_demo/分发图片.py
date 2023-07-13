# -- coding: utf-8 --
# @Time : 2023/4/13 17:40
# @Author : xulu.liu
import os
import re

folder_path = "/Users/liuxulu/workspace/blog/source/_posts/"


def findAllFile(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            if f.endswith('.md'):
                fullname = os.path.join(root, f)
                yield fullname


def mkdir(path):
    folder = os.path.exists(path)

    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径


for file_path in findAllFile(folder_path):
    f = open(file_path, 'r')
    # print(file_path)
    alllines = f.readlines()
    f.close()
    for eachline in alllines:
        if '](https://raw.githubusercontent.com' in eachline:
            file_name = file_path.split('/')[-1]
            img_path = "{}{}".format(file_path.replace(file_name, ''), 'img')
            mkdir(img_path)
            print(file_name)
            eachline = eachline.removesuffix('\n')
            img_name = eachline.removesuffix(')').split('/')[-1]
            print(img_name)
            cmd = "cp /Users/liuxulu/workspace/DevNote/sh/{} {}/{}".format(img_name, img_path, img_name)
            # cmd = "rm -rf {}".format(img_path)
            os.system(cmd)
            print(cmd)


# -- coding: utf-8 --
# @Time : 2023/4/13 12:14
# @Author : xulu.liu
import os

folder_path = "/Users/liuxulu/workspace/blog/source/_posts/"


def findAllFile(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            if f.endswith('.md'):
                fullname = os.path.join(root, f)
                yield fullname


for all_path in findAllFile(folder_path):
    filename = all_path.replace(folder_path, '')
    file_path = all_path
    print(file_path)
    title = "{} -- {}".format(filename.split('/')[-2], filename.split('/')[-1].replace('.md', ''))
    tag = filename.split('/')[0]
    categories = filename.split('/')[:-1]
    categorie_str = ''
    for c in categories:
        categorie_str += '- {}\n'.format(c)
    header = "---\ntitle: {}\ncategories:\n{}tags:\n{}---\n\n".format(title, categorie_str, categorie_str)
    with open(file_path, 'r+') as f:
        old = f.read()
        f.seek(0)
        f.write(header)
        f.write(old)



import os
import re

# 指定要修改文件名称的目录
dir_path = "/data/alist/video/花戎"

# 遍历目录下的所有文件
for filename in os.listdir(dir_path):
    # 使用正则表达式匹配符合条件的文件名称
    match = re.match(r"(\d+)\.1080p.HD国语中字无水印\[最新电影www.dygangs.me].mp4", filename)
    if match:
        # 构造新的文件名称
        new_filename = "花戎" + match.group(1) + "集.mp4"
        # 对文件进行重命名
        os.rename(os.path.join(dir_path, filename), os.path.join(dir_path, new_filename))
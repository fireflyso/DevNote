# -- coding: utf-8 --
# @Time : 2023/4/13 20:35
# @Author : xulu.liu

import urllib.request

urls = ['https://raw.githubusercontent.com/fireflyso/Img/master/markdown/cifang.png', 'https://raw.githubusercontent.com/fireflyso/Img/master/markdown/java_string.png', 'https://raw.githubusercontent.com/fireflyso/Img/master/2021-07/运输层.png', 'https://raw.githubusercontent.com/fireflyso/Img/master/2021-08/端口号.png', 'https://raw.githubusercontent.com/fireflyso/Img/master/2021-08/流行应用的运输协议.png', 'https://raw.githubusercontent.com/fireflyso/Img/master/2021-08/UDP.png', 'https://raw.githubusercontent.com/fireflyso/Img/master/2021-08/可靠传输1.png', 'https://raw.githubusercontent.com/fireflyso/Img/master/2021-08/比特交替协议.png', 'https://raw.githubusercontent.com/fireflyso/Img/master/2021-08/分组流水线.png', 'https://raw.githubusercontent.com/fireflyso/Img/master/2021-08/回退N步.png', 'https://raw.githubusercontent.com/fireflyso/Img/master/2021-08/TCP缓存.png', 'https://raw.githubusercontent.com/fireflyso/Img/master/2021-08/TCP报文段.png', 'https://raw.githubusercontent.com/fireflyso/Img/master/2021-08/telnet.png', 'https://raw.githubusercontent.com/fireflyso/Img/master/2021-05/应用层.png', 'https://raw.githubusercontent.com/fireflyso/Img/master/2021-05/套接字.png', 'https://raw.githubusercontent.com/fireflyso/Img/master/2021-06/缓存服务器.png', 'https://raw.githubusercontent.com/fireflyso/Img/master/2021-06/邮件服务.png', 'https://raw.githubusercontent.com/fireflyso/Img/master/2021-07/p2p.png', 'https://raw.githubusercontent.com/fireflyso/Img/master/2021-05/%E7%BD%91%E7%BB%9C%E5%B0%81%E8%A3%85.png', 'https://raw.githubusercontent.com/fireflyso/Img/master/2021-07/ch存储.png', 'https://raw.githubusercontent.com/fireflyso/Img/master/2021-11/jiqun.png', 'https://raw.githubusercontent.com/fireflyso/Img/master/2021-11/hundun.png', 'https://raw.githubusercontent.com/fireflyso/Img/master/2021-11/sampleserver.png', 'https://raw.githubusercontent.com/fireflyso/Img/master/2021-11/fuzhaserver.png', 'https://raw.githubusercontent.com/fireflyso/Img/master/markdown/WX20180913-120012.png']
base_path = './img'
filenames = ['{}'.format(u.split('/')[-1]) for u in urls]

for url, filename in zip(urls, filenames):
    print('start : {}'.format(filename))
    urllib.request.urlretrieve(url, '{}/{}'.format(base_path, filename))

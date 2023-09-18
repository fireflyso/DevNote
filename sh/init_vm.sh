#!/bin/bash
#适配Ubuntu系统
echo "对服务器进行初始化"
echo "========================="
echo " 1：检查docker服务安装情况"
echo " 2：安装alist"
echo " 3：安装qBittorrent"
echo " 4：安装Nginx"
echo "========================="

echo "--- 0. 准备安装zsh ---"
apt update
apt install zsh
sh -c "$(wget https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh -O -)"
apt install htop

echo "--- 1. 检查docker服务安装情况 ---"
res=$(ps aux | grep  docker | wc -l)
if [[ $res == 1 ]]
then
  echo "  docker尚未安装，即将开始安装"
  curl -sSL https://get.daocloud.io/docker | sh
else
  echo "  docker服务运行正常"
fi
apt  install docker-compose

echo "--- 2. 安装alist ---"
docker pull xhofe/alist:latest
mkdir -vp /data/alist
docker run -d --restart=always -v /etc/alist:/opt/alist/data -v /data:/data -p 5244:5244 -e PUID=0 -e PGID=0 -e UMASK=022 --name="alist" xhofe/alist:latest
echo "通过端口5244访问alist服务"
echo "alist账户信息 : " $(docker exec -it alist ./alist admin)

echo "--- 3. 安装qBittorrent ---"
docker pull linuxserver/qbittorrent
mkdir -vp /data/qbittorrent/config /data/qbittorrent/downloads
cat > /data/qbittorrent/docker-compose.yml <<EOF
version: "2"
services:
  qbittorrent:
    image: linuxserver/qbittorrent
    container_name: qbittorrent
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Asia/Shanghai # 你的时区
      - UMASK_SET=022
      - WEBUI_PORT=8888 # 将此处修改成你欲使用的 WEB 管理平台端口
    volumes:
      - /data/qBittorrent/config:/config # 绝对路径请修改为自己的config文件夹
      - /data/qBittorrent/downloads:/downloads # 绝对路径请修改为自己的downloads文件夹
    ports:
      # 要使用的映射下载端口与内部下载端口，可保持默认，安装完成后在管理页面仍然可以改成其他端口。
      - 6881:6881
      - 6881:6881/udp
      # 此处WEB UI 目标端口与内部端口务必保证相同，见问题1
      - 8888:8888
    restart: unless-stopped
EOF
docker-compose -f /data/qbittorrent/docker-compose.yml up -d
echo "通过端口8888访问qbittorrent服务,默认用户密码: admin/adminadmin 请在web ui中设置-web ui下修改密码"

echo "--- 3. 安装Nginx ---"
docker pull nginx:latest
mkdir -vp /data/nginx
cat > /data/nginx/host.conf <<EOF

server {
        listen       80;
        server_name  *.liuxulu.top;

        if ($http_host ~* "^(.*?)\.liuxulu\.top$") {    #正则表达式
                set $domain $1;                     #设置变量
        }

        location / {
            if ($domain ~* "alist") {
            proxy_pass http://alist.liuxulu.top:5244;      #域名中有alist，转发到5244端口
            }
            if ($domain ~* "bit") {
            proxy_pass http://bit.liuxulu.top:8888;      #域名中有bit，转发到8888端口
            }
            if ($domain ~* "blog") {
            proxy_pass http://blog.liuxulu.top:8088;      #域名中有bit，转发到8888端口
            }

            tcp_nodelay     on;
            proxy_set_header Host            $host;
            proxy_set_header X-Real-IP       $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            #以上三行，目的是将代理服务器收到的用户的信息传到真实服务器上

            root   html;
            index  index.html index.htm;            #默认情况
        }
        error_log /var/log/error.log debug;
        # log_format myFormat '$remote_addr–$remote_user [$time_local] $request $status $body_bytes_sent $http_referer $http_user_agent $http_x_forwarded_for'; #自定义格式
        # access_log /var/log/access.log myFormat;
}

server{
        listen    8088;     # 端口
        root /data/blog_page;   # 静态页面路径，要和上面git仓库配置路径对应上
        server_name blog.liuxulu.top;   # 这个好像没啥用
        location /{
        }
        error_log /var/log/blog-error.log debug;
        # log_format myFormat '$remote_addr–$remote_user [$time_local] $request $status $body_bytes_sent $http_referer $http_user_agent $http_x_forwarded_for'; #自定义格式
        # access_log /var/log/blog-access.log myFormat;
}
EOF
docker run -d --net=host -v /data/nginx/:/etc/nginx/conf.d/ -v /data/blog_page:/data/blog_page --name nginx nginx
#!/bin/bash
#适配Ubuntu系统
echo "对服务器进行初始化"
echo "========================="
echo " 1：检查docker服务安装情况"
echo " 2：安装alist"
echo " 3：安装qBittorrent"
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




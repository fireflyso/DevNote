apt-get update
sudo apt-get install      apt-transport-https      ca-certificates      curl      gnupg      lsb-release
curl -fsSL https://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo   "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://mirrors.aliyun.com/docker-ce/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
sudo systemctl enable docker
sudo systemctl start docker

docker pull nginx:latest
docker run --name nginx-test -p 8080:80 -d nginx

sudo apt install build-essential libssl-dev git unzip
wget http://106.3.133.42:5244/d/local/wrk-master.zip
unzip wrk-master.zip
rm -rf wrk-master.zip
cd wrk-master
make -j8
sudo cp wrk /usr/local/bin




# VDC

snmpwalk -v 2c -c QAZXSWedc 10.215.84.10 .1.3.6.1.2.1.2.2.1.2

# 出向
snmpwalk -v 2c -c QAZXSWedc 10.215.84.10 .1.3.6.1.2.1.31.1.1.1.10.2941

# 入向
snmpwalk -v 2c -c QAZXSWedc 10.215.84.2 .1.3.6.1.2.1.31.1.1.1.6.1844


## 诺基亚
snmpwalk -v 2c -c private 118.186.56.46 .1.3.6.1.2.1.2.2.1.2




client.execute("ALTER TABLE flow_snmp.flow_data_local_new UPDATE in_bps=2110148916.0,out_bps=85141233354.0 WHERE pipe_id = '4eaf5570-f45d-11ed-bb3b-fac1491bd8ed' and time = '2023-07-01 03:10:00';")
client.execute("SELECT pipe_id, time, in_bps, out_bps FROM flow_snmp.flow_data_local_new where pipe_id = '4eaf5570-f45d-11ed-bb3b-fac1491bd8ed' and time = '2023-07-01 03:10:00'")
client.execute("SELECT * FROM flow_snmp.flow_data_local_new where pipe_id = '4eaf5570-f45d-11ed-bb3b-fac1491bd8ed' and time = '2023-07-01 03:10:00'")



# EIP count
# 拿设备上所有的接口
snmpwalk -v 2c -c QAZXSWedc 10.13.103.191  1.3.6.1.4.1.2636.3.5.2.1.7 | grep 5803da3a-cc47-11ed-8ce9-ba7dff90fbd8


# 拿接口的数据
# in

snmpwalk -v 2c -c QAZXSWedc 10.212.143.251  1.3.6.1.4.1.2636.3.5.2.1.5
snmpwalk -v 2c -c QAZXSWedc 10.215.84.2  1.3.6.1.4.1.2636.3.5.2.1.5.15.108.51.45.105.110.110.101.114.45.116.101.115.116.45.49.24.108.51.45.105.110.110.101.114.45.116.101.115.116.45.49.45.97.122.49.45.118.112.99.49.2

snmpwalk -v 2c -c QAZXSWedc 10.212.143.250  1.3.6.1.4.1.2636.3.5.2.1.5.20.118.114.102.45.69.49.48.52.54.49.54.45.49.48.48.56.54.45.105.110.39.99.98.56.50.50.49.49.50.45.50.53.48.49.45.49.49.101.100.45.57.50.99.99.45.98.101.101.100.98.50.101.100.54.55.98.100.95.105.110.2



run show snmp mib walk 1.3.6.1.4.1.2636.3.5.2.1.5.15.108.51.45.105.110.110.101.114.45.116.101.115.116.45.49.24.108.51.45.105.110.110.101.114.45.116.101.115.116.45.49.45.97.122.49.45.118.112.99.49.2  l3-inner-test-1-az1-vpc1



# out
snmpwalk -v 2c -c QAZXSWedc 10.212.143.250  1.3.6.1.4.1.2636.3.5.2.1.5.20.118.114.102.45.69.49.48.52.54.49.54.45.49.48.48.56.54.45.105.110.39.99.98.56.50.50.49.49.50.45.50.53.48.49.45.49.49.101.100.45.57.50.99.99.45.98.101.101.100.98.50.101.100.54.55.98.100.95.105.110.2



docker run -d --name stack_elk_logstash -v /data/telemetry/logstash_data:/data --net=host -t wenxingu/stack_elk_logstash


docker run -p 8888:8888 --rm -v $(pwd)/etc:/fluentd/etc -v $(pwd)/log:/fluentd/log fluent/fluentd:v1.7-1 -c /fluentd/etc/fluentd_basic_setup.conf -v

docker run -p 8888:8888 --rm -v $(pwd)/etc:/fluentd/etc -v $(pwd)/log:/fluentd/log fluent/fluentd:v1.7-1 -c /fluentd/etc/fluentd_udp.conf -v


curl -i -X POST -d "json={"action":"login","user":2}" http://10.2.10.126:8888/test.cycle



Done installing documentation for string-scrub, tzinfo-data, sigdump, http_parser.rb, cool.io, yajl-ruby, msgpack, fluentd, fluent-plugin-rewrite-tag-filter, fluent-plugin-udp-native-sensors after 3 seconds

nc -u 10.2.10.126 8887  通过这个命令可以发送upd消息

nc -ul 0.0.0.0 8887 > data.gpb

protoc --decode_raw  < ../data.gpb

protoc --decode TelemetryStream logical_port.proto -I /usr/include -I .  < ../data.gpb > ../data.out
/root/telemetry/protoc-3.17.3/bin/protoc --decode TelemetryStream port.proto < ../data.gpb | less -N

# mac本地
protoc --decode TelemetryStream logical_port.proto < ../../data.gpb | less -N
protoc --python_out=./

protoc --decode TelemetryStream logical_port.proto  -I .  < ../../data.gpb > ../../data.out

gem search -rd

gem list --local

tzinfo (2.0.4, 1.2.9)

gem install fluent-plugin-udp-native-sensors-0.0.1.gem

set services analytics export-profile export-params format json

protoc -I /usr/include -I . --python_out=./


protoc -I /usr/include -I . --ruby_out=./ logical_port.proto

protoc --decode TelemetryStream port.proto < ../../data.gpb | less -N


python -m grpc_tools.protoc -I. --python_out=./ --grpc_python_out=./ ./data.proto

-v /etc/timezone:/etc/timezone:ro -v /etc/localtime:/etc/localtime:ro

docker run -it -p 8885:8885 -v /root/work/wan_telemetry-20220527_nokia:/code -d --net=host wan_telemetry > /dev/null 2>&1 &

docker run -it -p 8877:8877 -v /data/telemetry_data:/data/telemetry_data -e TZ=Asia/Shanghai registry.cn-beijing.aliyuncs.com/fireflyos/huawei_telemery_server:v1 > /dev/null 2>&1 &
docker run -it -v /data/telemetry_data:/data/telemetry_data -e TZ=Asia/Shanghai registry.cn-beijing.aliyuncs.com/fireflyos/huawei_telemetry_worker:v1 > /dev/null 2>&1 &

docker run -it -v /data/telemetry_data:/data/telemetry_data -e TZ=Asia/Shanghai huawei_telemetry_worker > /dev/null 2>&1 &

docker run -itd -p 8877:8877 -v /Users/liuxulu/workspace/cds:/workspace --privileged my_centos /usr/sbin/init

docker run -it -v /data/telemetry_data:/data/telemetry_data -e TZ=Asia/Shanghai -e server_path="src/juniper/udp/juniper_worker.py" wan_telemetry > /dev/null 2>&1 &

docker run -p 8888:8888/udp -v /data/telemetry_data:/data/telemetry_data -e TZ=Asia/Shanghai -e server_path="src/cisco/udp/cisco_server.py" wan_telemetry > /dev/null 2>&1 &

docker run --name mongodb -p 10086:27017 -v $PWD/db:/data/db -d mongo:latest

docker run -it -p 8000:8000 -v /Users/liuxulu/workspace/cds/cdsop:/app -v /etc/hosts:/etc/hosts cdsop > /dev/null 2>&1 &
docker run -it -p 8000:8000 -v /Users/liuxulu/workspace/cds/cdsop:/app cdsop > /dev/null 2>&1 &


db.createUser({ user: "firefly", pwd: "#Y1U,5V<yg{U", roles: [ { role: "userAdminAnyDatabase", db: "admin" } ] });
db.auth("firefly","#Y1U,5V<yg{U");

sudo firewall-cmd --zone=public --add-port=10086/tcp --permanent

半小时检查GPN流量超限
http://10.13.227.41:6017/api/api_task/check_gpn_qos?mail=xulu.liu@capitalonline.net,qiang.zhang@capitalonline.net,mu.huang@capitalonline.net,zheng.liu@capitalonline.net,lin.li@capitalonline.net,su.kong@capitalonline.net,luojinshuchanpinbu@capitalonline.net&interval=30
* * * * * curl http://10.13.2.133:6017/api/api_task/check_idc_flow?mail=xulu.liu@capitalonline.net

http://10.13.227.41:6017/api/api_task/check_idc_flow?mail=xulu.liu@capitalonline.net
http://10.13.227.165:6017/api/api_task/check_idc_flow?mail=xulu.liu@capitalonline.net

*/30 * * * * source /root/work/pro_env/venv/bin/activate && python /root/work/pro_env/gpn_flow_check.py > /root/work/pro_env/gpn_flow_check.log




  

api-flow-bps 1.1.1.1:6007 pre 这是最老的项目，python2没有部署到k8s
api-flow-bps-k8s api-flow-bps.pre api-flow-bps-service 这个项目本来是老项目的python3和k8s部署重构版本，这里面有vm接口，但是由于和第三个项目冗余了，已被我们废弃，这个项目已经完成了k8s 测试、预生产和生产的部署，你们可以直接维护，让他们直接掉这个项目就可以，只是目前他们的测试环境的地址没写对
wan-flow-bps wan-flow-bps.pre wan-flow-bps-service  这是我们现在在用的计量项目，这里面没有vm那个接口

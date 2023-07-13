#!/bin/bash

# 线上版本
#!/bin/bash

url='wan-flow-bps.gic.pre/slb_monitor_save'
active_conn=$(ipvsadm -ln --exact | tr '\n' '|')
all_conn=$(ipvsadm -ln --stats --exact | tr '\n' '|')
slb_vm_id=$SLB_VM_ID
monitor_date=$(date "+%Y-%m-%d %H:%M:%S")

data='active_conn='$active_conn'&all_conn='$all_conn'&slb_vm_id='$slb_vm_id'&monitor_date='$monitor_date
echo $data
response=$(curl -X POST -d "$data" $url)
echo $response



# 第二版内容（舍弃网卡信息采集）
# 采集DPVS主机中SLB的监控数据
# 1. ipvsadm -ln 采集到实时连接数
# 2. ipvsadm -ln --stats 采集到累计连接数、IO包数、IO字节数
# 通过环境变量$SLB_VM_ID获取到DPVS机器在数据库表中的编号
# 将vm id和两个监控命令返回结果推送到api
url='localhost:8000'
active_conn=$(ipvsadm -ln --exact | tr '\n' '|')
all_conn=$(ipvsadm -ln --stats --exact | tr '\n' '|')
slb_vm_id=$SLB_VM_ID
monitor_date=$(date "+%Y-%m-%d %H:%M:%S")

#active_conn='IP Virtual Server version 0.0.0 (size=0)|Prot LocalAddress:Port Scheduler Flags| -> RemoteAddress:Port Forward Weight ActiveConn InActConn|TCP 10.1.255.1:80 rr| -> 172.16.0.1:80 FullNat 100 0 0 | -> 172.16.0.2:80 FullNat 100 0 0 |TCP 10.1.255.1:81 rr| -> 172.17.2.1:80 FullNat 100 0 0 | -> 172.17.2.2:80 FullNat 100 0 0 |'
#all_conn='IP Virtual Server version 0.0.0 (size=0)|Prot LocalAddress:Port Conns InPkts OutPkts InBytes OutBytes| -> RemoteAddress:Port|TCP 10.1.255.1:80 59288 9055695905 9055392057 8919691329622 8928503398908| -> 172.16.0.1:80 29642 4530920823 4530768890 4462872441777 4467281552714| -> 172.16.0.2:80 29646 4524775082 4524623167 4456818887845 4461221846194|TCP 10.1.255.1:81 0 0 0 0 0| -> 172.17.2.1:80 0 0 0 0 0| -> 172.17.2.2:80 0 0 0 0 0|'
#slb_vm_id='4459c4bb-967c-48a4-a6a8-f1d374abcfb3'
#response=$(curl -X POST -d 'active_conn='$active_conn'&all_conn='$all_conn'&slb_vm_id='$slb_vm_id'&monitor_date='$monitor_date $url'/api/slb_monitor/save/')
data='active_conn='$active_conn'&all_conn='$all_conn'&slb_vm_id='$slb_vm_id'&monitor_date='$monitor_date
data='active_conn=IP Virtual Server version 0.0.0 (size=0)|Prot LocalAddress:Port Scheduler Flags| -> RemoteAddress:Port Forward Weight ActiveConn InActConn|TCP 10.1.255.1:80 rr| -> 172.16.0.1:80 FullNat 100 0 5621 | -> 172.16.0.2:80 FullNat 100 0 5625 |TCP 10.1.255.1:81 rr| -> 172.17.2.1:80 FullNat 100 0 0 | -> 172.17.2.2:80 FullNat 100 0 0 |&all_conn=IP Virtual Server version 0.0.0 (size=0)|Prot LocalAddress:Port Conns InPkts OutPkts InBytes OutBytes| -> RemoteAddress:Port|TCP 10.1.255.1:80 1147427 4586846 0 220168608 0| -> 172.16.0.1:80 573713 2293422 0 110084256 0| -> 172.16.0.2:80 573714 2293424 0 110084352 0|TCP 10.1.255.1:81 0 0 0 0 0| -> 172.17.2.1:80 0 0 0 0 0| -> 172.17.2.2:80 0 0 0 0 0|&slb_vm_id=4459c4bb-967c-48a4-a6a8-f1d374abcfb3&monitor_date=2023-03-23 16:12:14'
response=$(curl -X POST -d $data $url'/api/slb_monitor/save/')


# 第一版内容
# 采集DPVS主机中SLB的监控数据
# 1. ipvsadm -ln 采集到实时连接数
# 2. ipvsadm -ln --stats 采集到累计连接数、IO包数、IO字节数
# 3. dpip -s link show dpdk0 采集到IO包数、IO字节数、IO异常包数

#url='localhost:8000'
#active_conn=$(ipvsadm -ln | tr '\n' '&')
#all_conn=$(ipvsadm -ln --stats | tr '\n' '&')
#io_error=$(dpip -s link show | tr '\n' '&')
#monitor_data='active_conn='$active_conn'&all_conn='$all_conn'&io_error='$io_error
#response=$(curl -X POST -d 'monitor_data='$monitor_data $url'/api/slb_monitor/save/')




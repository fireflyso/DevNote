#!/bin/bash

url='http://106.3.133.42:7636/monitor/'
active_conn=$(ipvsadm -ln --exact | tr '\n' '|')
all_conn=$(ipvsadm -ln --stats --exact | tr '\n' '|')
slb_vm_id=$SLB_VM_ID
monitor_date=$(date "+%Y-%m-%d %H:%M:%S")

data='active_conn='$active_conn'&all_conn='$all_conn'&slb_vm_id='$slb_vm_id'&monitor_date='$monitor_date
echo $data
response=$(curl -X POST -d "$data" $url)
echo $response
# -- coding: utf-8 --
# @Time : 2023/9/13 10:55
# @Author : xulu.liu
import requests

OPERATE_VM_CMD = 'http://corevm-api/v1/core_vm/cck/exec_command/'
params = {
    "customer_id": "E2130386",
    "user_id": "775101",
    "master_vm_id": "6f1a05ac-ee54-4ec1-b71b-47488c4243d4",
    "task": False,
    "params": "ipvsadm -ln",
    "master_vm_username": "root",
    "master_vm_password": "qUhv9LC25w9wG0Bh"
}
response = requests.post(OPERATE_VM_CMD, data=params, timeout=5, verify=False)


OPERATE_VM_PID = 'http://corevm-api/v1/core_vm/cck/exec_command/'
params = {
    "vm_id": "E2130386",
    "vm_name": "775101",
    "site_id": "6f1a05ac-ee54-4ec1-b71b-47488c4243d4",
    "pid": False,
    "vm_username": "ipvsadm -ln",
    "vm_password": "root"
}
response = requests.post(OPERATE_VM_CMD, data=params, timeout=5, verify=False)
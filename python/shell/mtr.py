import subprocess
from datetime import datetime

out_file = './out.info'
commands = [
    "mtr -c 1 -rnz 36.65.144.59",
    "mtr -c 1 -rnz 216.177.141.60",
    "mtr -c 1 -rnz 36.68.136.67",
    "mtr -c 1 -rnz 36.68.137.73",
    "mtr -c 1 -rnz 36.68.139.174",
    "mtr -c 1 -rnz 36.67.247.82"
]
command = 'mtr -c 1 -rnz 36.65.144.59'
start_time = datetime.now()
res = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE)
print('耗时 : {} s'.format((datetime.now() - start_time).seconds))

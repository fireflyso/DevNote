import requests
from stem import Signal
from stem.control import Controller


def switch_proxy():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password='admin')
        controller.signal(Signal.NEWNYM)


for i in range(10):
    # switch_proxy()
    response = requests.get('http://icanhazip.com/', proxies={'http': 'socks5://admin:admin@164.52.47.110:8081'})
    print(response.text.strip())



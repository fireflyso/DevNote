import requests
from stem import Signal
from stem.control import Controller


def switch_proxy():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password='my password')
        controller.signal(Signal.NEWNYM)


for i in range(10):
    switch_proxy()
    response = requests.get('http://icanhazip.com/', proxies={'http': '127.0.0.1:8118'})
    print(response.text.strip())
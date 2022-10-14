import requests
import config

# 校园网地址
network_addr = "http://10.10.43.3/drcom/login"

# Head
network_header = {
    'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Host': '10.10.43.3',
    'Referer': 'http://10.10.43.3/',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}

# Param
network_param = {
    'callback': 'dr1665733424916',
    'DDDDD': config.network_user,
    'upass': config.network_pswd,
    '0MKKey': '123456',
    'R1': '0',
    'R3': '0',
    'R6': '0',
    'para': '00',
    'v6ip': '',
    '_': '1665733415071'
}


def networkConnect():
    r = requests.get(network_addr, params=network_param, headers=network_header)
    print(r)

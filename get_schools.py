import os
import time
import json
import requests
import subprocess

from constant import *

HEADERS = {
    "Origin": "http://account.weibo.com",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "*/*",
    "DNT": 1,
    "Referer": "http://account.weibo.com/set/index?topnav=1&wvr=6",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4",
    "Cookie": "wvr=6; SINAGLOBAL=881647481583.0588.1451824626364; _s_tentry=www.dewen.net.cn; Apache=249416289844.1643.1468652580457; ULV=1468652580503:52:2:1:249416289844.1643.1468652580457:1467740628140; login_sid_t=6f9b270fe9593ce47753f4af7f282256; un=lyc9308@sina.com; SSOLoginState=1472363909; SCF=Av0VI7pqQYAa7Z1fNicVBeCzfq6U2zH7gHBjSthnuiOwvKfxfcIOPua0aia77wqiGub03QHoIHUJjNQyBiKnoDE.; SUB=_2A256wQV-DeTxGedN6VMT-CfNwzmIHXVZt3G2rDV8PUNbmtBeLW7skW9lvjQszGjNraJdn80Q2OkQ0pUtrg..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhQ9vNSxFk7qMJZYnV_8GPg5JpX5KMhUgL.Fo20eo2E1h.p1h-2dJLoI7yz9g8XI8veIBtt; SUHB=04Wf9se103tTlO; ALF=1504094382; WBStore=0e9767219e7dbe35|undefined; UV3=usrmdinst_4; UOR=www.importnew.com,widget.weibo.com,www.google.com; AccV5=usrmdinst_0; SINAGLOBAL=881647481583.0588.1451824626364; _s_tentry=www.dewen.net.cn; Apache=249416289844.1643.1468652580457; ULV=1468652580503:52:2:1:249416289844.1643.1468652580457:1467740628140; login_sid_t=6f9b270fe9593ce47753f4af7f282256; un=lyc9308@sina.com; SSOLoginState=1472363909; SCF=Av0VI7pqQYAa7Z1fNicVBeCzfq6U2zH7gHBjSthnuiOwvKfxfcIOPua0aia77wqiGub03QHoIHUJjNQyBiKnoDE.; SUB=_2A256wQV-DeTxGedN6VMT-CfNwzmIHXVZt3G2rDV8PUNbmtBeLW7skW9lvjQszGjNraJdn80Q2OkQ0pUtrg..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhQ9vNSxFk7qMJZYnV_8GPg5JpX5KMhUgL.Fo20eo2E1h.p1h-2dJLoI7yz9g8XI8veIBtt; SUHB=04Wf9se103tTlO; ALF=1504094382; WBStore=0e9767219e7dbe35|undefined; UV3=usrmdinst_4; UOR=www.importnew.com,widget.weibo.com,www.google.com; AccV5=usrmdinst_0"
}
# PROVINCES_WITH_CITIES = {}
ACCESS_TOKEN = "2.00tfz68BZhHwxD50cb79f632Ux_vxD"
URL = "https://api.weibo.com/2/common/get_city.json?province={}&access_token={}"


def get_cities_in_province():
    for province in PROVINCES:
        r = requests.get(URL.format(province[0], ACCESS_TOKEN), headers=HEADERS)
        if r.status_code == 200:
            PROVINCES_WITH_CITIES[province[1]] = {
                'cities': r.text,
                'num': province[0],
                'name': province[1],
            }
        time.sleep(5)
    print(PROVINCES_WITH_CITIES)


def deal_result():
    for province in PROVINCES_WITH_CITIES.keys():
        cities = PROVINCES_WITH_CITIES[province]['cities']
        PROVINCES_WITH_CITIES[province]['cities'] = eval(cities)
    print(PROVINCES_WITH_CITIES)


def get_university():
    for province in PROVINCES_WITH_CITIES.keys():
        p_path = '/home/heath/PycharmProjects/Schools/datas/大学'
        if not os.path.exists(p_path):
            subprocess.call(['mkdir', '-p', p_path])
        url = 'http://account.weibo.com/set/aj5/userinfo/schoollist?__rnd=%d' % int(time.time() * 1000)
        payload = {
            'province': int(PROVINCES_WITH_CITIES[province]['num']) % 100,
            'city': '',
            'type': 1,
            '_t': 0
        }
        print(url)
        print(payload)
        r = requests.post(url, data=payload, headers=HEADERS)
        if r.status_code == 200:
            with open(os.path.join(p_path, province + '.txt'), 'w') as f:
                json.dump(r.text, f)
            print('finish %s' % province)
            time.sleep(10)


if __name__ == '__main__':
    get_university()

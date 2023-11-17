import requests
from lxml import etree
import os
import json
from urllib import parse
import execjs
import hashlib
import time

import Utils

class SpiderRequest():
    def __init__(self, parse_url, url, cookie):
        self.parse_url = parse_url
        self.url = url
        self.cookie = cookie
        self.headers = {}

    def get_headers(self):
        star = 'd_c0='
        end = ';'
        cookie_mes = self.cookie[self.cookie.index(star):].replace(star, '')
        cookie_mes = cookie_mes[:cookie_mes.index(end)]
        f = "+".join(["101_3_2.0", self.parse_url, cookie_mes])
        fmd5 = hashlib.new('md5', f.encode()).hexdigest()
        jsdom_path = Utils.read_my_file('my_file/jsdom_path.txt')
        with open("./g_encrypt.js", 'r', encoding='utf-8') as f:
            ctx1 = execjs.compile(f.read(), cwd=jsdom_path)
        encrypt_str = "2.0_%s" % ctx1.call('b', fmd5)
        print(encrypt_str)
        headers = {
            'Host': 'api.zhihu.com', # self.cookie
            'Cookie': 'KLBRSID=d017ffedd50a8c265f0e648afe355952|1699962004|1699961431; zst_82=2.0ANBULRJ8sxcLAAAASwUAADIuMJJcU2UAAAAANox6NQl4hfXoSeRK3MSddSrW-Tw=; d_c0=AECXyptR5BVLBdkILlvvl7AqiEu8n3-h2YM=|1699961431; q_c0=2|1:0|10:1698430641|4:q_c0|80:MS4xXzV1RkdRQUFBQUFMQUFBQVlBSlZUYkdMWTJVSDZXaDVvR1ktaVkwNjZuMFVNbmNJYjF4ejJnPT0=|c423fdd9a27d752e32dee0a59cbd333deb406188147db8f4427b60e3a7f06d5e; z_c0=2|1:0|10:1698430641|4:z_c0|80:MS4xXzV1RkdRQUFBQUFMQUFBQVlBSlZUYkdMWTJVSDZXaDVvR1ktaVkwNjZuMFVNbmNJYjF4ejJnPT0=|c57fed1025a869b2702c739558726806ff7b446f7eb885364a89aa785732fbb0; _xsrf=MCyApmOQ17yyIJf47xh2XkhRtHSsNySx; __utma=51854390.659237652.1669057290.1695809172.1698515976.7; __utmv=51854390.110-1|2=registration_date=20200229=1^3=entry_date=20200229=1; __utmz=51854390.1669057290.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); q_c1=2986d93d01aa46a489e9a7b13b188e23|1698515975000|1669057288000; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1697783872,1698215553; edu_user_uuid=edu-v1|81dec717-9464-4d31-9060-232ea447fef7; _zap=b3d55bf0-ae9f-4a11-9be2-85212afa70bf',
            'Accept': '*/*',
            'x-requested-with': 'Fetch',
            'Sec-Fetch-Site': 'same-site',
            'x-zse-93': '101_5_3.1',
            'x-hd': '4a49b0522f7f0de89332958a6ca143fd',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Sec-Fetch-Mode': 'cors',
            'Accept-Encoding': 'gzip, deflate, br',
            'Origin': 'https://www.zhihu.com',
            'User-Agent': 'ZhihuHybrid osee2unifiedRelease/16416 osee2unifiedReleaseVersion/9.26.0 Mozilla/5.0 (iPhone; CPU iPhone OS 16_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
            'Referer': 'https://www.zhihu.com/',
            'x-app-version': '9.26.0',
            'Connection': 'keep-alive',
            'x-ac-udid': 'AECXyptR5BVLBdkILlvvl7AqiEu8n3-h2YM=',
            'Sec-Fetch-Dest': 'empty',
            'x-zse-96': encrypt_str
        }
        # headers = {
        #     "x-app-version": "9.26.0",
        #     'x-app-za': 'OS=Web',
        #     "x-zse-93": "101_5_3.1",
        #     "x-zse-96": encrypt_str,
        #     "User-agent": "ZhihuHybrid osee2unifiedRelease/16416 osee2unifiedReleaseVersion/9.26.0 Mozilla/5.0 (iPhone; CPU iPhone OS 16_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
        #     "Cookie": self.cookie,
        # }
        self.headers = headers

    def getRequest(self):
        self.get_headers()
        response = requests.get(self.url, headers=self.headers)
        response.encoding = 'utf-8'
        print('1')
        print(response.status_code)
        # print(response.text)
        shelf_data = response.json()
        with open('./my_file/api_data.json', 'w', encoding='utf-8') as file:
            json.dump(shelf_data, file, ensure_ascii=False, indent=4)
        print('2')
        # print(json_mes)
        return shelf_data

    def postRequest(self, data):
        self.get_headers()
        headers = self.headers
        # headers['Content-Type'] = 'application/json'
        print(headers)
        print(int(round(time.time() * 1000)))  # 毫秒级时间戳

        print(data)
        response = requests.post(self.url, json=data, headers=headers)
        response.encoding = 'utf-8'
        print(response)
        print(response.text)
        json_mes = json.loads(response.text)
        print(json_mes)
        return json_mes



if __name__ == '__main__':
    url = 'https://api.zhihu.com/pluton/shelves?limit=500&offset=0&property_type=column'
    url_path = '/pluton/shelves?limit=200&offset=0&property_type=column'
    cookie = Utils.read_my_file('my_file/cookie.txt')
    op = SpiderRequest(url_path, url, cookie)
    data = op.getRequest()
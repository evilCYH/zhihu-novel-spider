# -*- coding: utf-8 -*-
import pandas as pd
import requests
import os
import re
from random_useragent import UserAgent
from bs4 import BeautifulSoup

u = UserAgent()

# dir = '.\\download\\B 面人生 那些神展开的烧脑悬疑故事'
# result = dir.split('\\')[-1]
# print(result)
# paragraphs = [1, 2, 3, 4, 5, 6]
#
# for paragraph in paragraphs:
#     print(paragraph)
#     if paragraph > 3:
#         break
# print('over')
# 遍历文件夹中的所有文件和文件夹
# def traversal_dirs(path):
#     dirs = []
#     files = []
#     for item in os.scandir(path):
#         if item.is_dir():
#             dirs.append(item.path)
#
#         elif item.is_file():
#             files.append(item.path)
#     return dirs
#
#
# dir_list = traversal_dirs(r'.\test')
# print(dir_list)

# df = pd.read_csv('./my_file/filter_data.csv', encoding='utf-8-sig')
# print(df[df['title'] == '半岛铁盒 消失的情书']['author'])
# print(df.columns)

# -*- coding: utf-8 -*-
import random
from time import sleep
#
# paragraphs = [3]
# if paragraphs:
#     print(1)

# url = 'https://www.ysg0.com/book/27/9d3c1cdceaabb.html'
# headers = {
#             'Host': 'www.ysg0.com',
#             'Cookie':'lf_reader_num_363=1; reader_config_web=0%7C18%7C1%7C0%7C1; Hm_lvt_56ba7884d3bf128f739cc872be9cf063=1700120220; PHPSESSID=lgsth57keofuifvo90gnek647d; lf_user_auth=think%3A%7B%22uid%22%3A%22101345%22%2C%22username%22%3A%22zrz%22%7D; lf_user_auth_sign=c821567a3e21d7ad2246bb86f26962dffa8e0ce1; lf_user_recommend=1700120306; lf_read_log=think%3A%7B%22393%22%3A%22363%257C05aa97ed06940%257C1700120339%22%7D; Hm_lpvt_56ba7884d3bf128f739cc872be9cf063=1700120342',
#             'Referer': 'https://www.ysg0.com/user/user/login.html',
#             'Connection': 'keep-alive',
#             'User-Agent': u.pc()
#         }
# chapter_response = requests.get(url, headers = headers)
#
# soup = BeautifulSoup(chapter_response.content, 'html.parser')
#
# paragraphs = soup.find_all('div', class_ = 'read-content j_readContent')[0].find_all('p')
#
# print(paragraphs)

import requests

url = 'https://www.ysg0.com/api/save_chapter/index'
params = {'id': '27', 'key': 'b58c71facc758'}

response = requests.get(url, params=params)
print(response.text)

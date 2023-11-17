import pandas as pd
import os
import requests
import random
import csv
import re
import datetime
from time import sleep
from bs4 import BeautifulSoup
from ua import ua_generate
from urllib.parse import urlencode
from random_useragent import UserAgent

u = UserAgent()

df = pd.read_csv('./my_file/filter_data.csv')

log_filename = f'./my_file/error.log'
abandon_filename = f'./my_file/abandon.txt'

zhihu_header = {
    'User-Agent': ua_generate()
}
ysg_header = {
    'User-Agent': u.pc()
}

for index, row in df.iterrows():
    print("==================================================================")
    novel_name = row['title']
    print(f"开始处理 [{novel_name}]")
    # 创建info csv
    parameter = urlencode({'keyWords': f"{row['business_url']}"})
    ysg_api = f'https://api.ysg0.com/apis/survey/novelSearch/getNovelSearchList?{parameter}'

    ysg_response = requests.get(ysg_api, headers=ysg_header)
    ysg_data = ysg_response.json()
    rest_time2 = round(random.uniform(5, 6), 2)
    sleep(rest_time2)

    if ysg_data['code'] != 200:
        # 获取当前时间
        current_time = datetime.datetime.now()
        # 构建要写入日志的内容
        error_message = ysg_data['message']
        log_message = f"[{current_time}] [{novel_name}] {error_message}"
        abandon_message = f"{novel_name}"
        # 写入日志文件
        with open(log_filename, 'a') as file:
            file.write(log_message + '\n')
        # 写入废弃文件
        with open(abandon_filename, 'a') as file:
            file.write(abandon_message + '\n')

        print(f"[{novel_name}] {error_message}")
        # 进入dataframe下一行
        continue
    else:
        print(f"[{novel_name}] ok, code = {ysg_data['code']}")

    # 创建文件夹
    save_path = f'{os.getcwd()}\download\{novel_name}'
    show_path = f'./download/{novel_name}/'
    if os.path.exists(save_path):
        print(f'{show_path} 文件夹之前已创建, go on')
    else:
        print(f'{show_path} 文件夹未创建, 开始build')
        os.mkdir(save_path)
        print(f'{show_path} 文件夹已创建完毕')

    # 获取img封面的url
    img_url = row['tab_artwork']

    img_response = requests.get(img_url, headers=zhihu_header)

    rest_time1 = round(random.uniform(0.3, 0.5), 2)
    sleep(rest_time1)

    img = img_response.content

    # 保存图像到本地文件
    if os.path.exists(f'{save_path}\cover.jpg'):
        print(f'封面已存在, go on')
    else:
        with open(f"{save_path}\cover.jpg", "wb") as f:
            f.write(img)
            print('封面已保存完毕')

    for i in range(0,2):
        try:
            novel_url = ysg_data['data'][0]['url']
            break
        except KeyError:
            print(f"第{i+1}次 Error: 'data' key not found. Sleeping for 2 seconds...")
            sleep(2)

    result = re.search(r'https://ysg0.com/novel/(.*)', novel_url)
    # print(result)
    if result:
        pass
    else:
        # 获取当前时间
        current_time = datetime.datetime.now()
        # 构建要写入日志的内容
        log_message = f"[{current_time}] [{novel_name}] url may have some error"
        # 写入日志文件
        with open(log_filename, 'a') as file:
            file.write(log_message + '\n')

    catalog_response = requests.get(novel_url, headers=ysg_header)
    # print(f'catalog data: {catalog_response.status_code}')

    soup = BeautifulSoup(catalog_response.content, 'html.parser')

    # 假设已经有了 soup 对象
    div_elements = soup.find_all('div', class_="cate-list")

    chapter_list = []
    for div_element in div_elements:
        a_elements = div_element.find_all('a')
        # 对每个包含<a>标签的<div>元素进行操作
        for a_element in a_elements:
            # 这里可以处理每个<a>元素，比如获取链接或者文本等
            chapter_href = 'https://www.ysg0.com' + a_element.get('href')  # 获取链接
            chapter_name = a_element.find('span', class_="chapter_name").text  # 获取文本内容
            chapter_list.append([chapter_name, chapter_href])
    # 写入CSV文件
    csv_filename = f'{save_path}\chapter_data.csv'

    with open(csv_filename, 'w', newline='', encoding="utf_8_sig") as csv_file:
        csv_writer = csv.writer(csv_file)
        # 写入表头
        csv_writer.writerow(['Title', 'URL'])
        # 写入数据
        csv_writer.writerows(chapter_list)

    print(f'Chapter info has been written to {show_path}chapter_data.csv')

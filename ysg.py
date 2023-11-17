# -*- coding: utf-8 -*-
import datetime
import random
from time import sleep

import pandas as pd
import requests
import os
import re

from ebooklib import epub
from random_useragent import UserAgent
from tqdm import tqdm

u = UserAgent()
from bs4 import BeautifulSoup

cookies = [
    'lf_reader_num_363=1; reader_config_web=0%7C18%7C1%7C0%7C1; Hm_lvt_56ba7884d3bf128f739cc872be9cf063=1700120220; PHPSESSID=lgsth57keofuifvo90gnek647d; lf_user_auth=think%3A%7B%22uid%22%3A%22101345%22%2C%22username%22%3A%22zrz%22%7D; lf_user_auth_sign=c821567a3e21d7ad2246bb86f26962dffa8e0ce1; lf_user_recommend=1700120306; lf_read_log=think%3A%7B%22393%22%3A%22363%257C05aa97ed06940%257C1700120339%22%7D; Hm_lpvt_56ba7884d3bf128f739cc872be9cf063=1700120342',
    '__51uvsct__K2jtTf36F5UaO7Vp=5; __51vcke__K2jtTf36F5UaO7Vp=1ded822f-24d4-5818-8435-3d473d17b856; __51vuft__K2jtTf36F5UaO7Vp=1700030715797; Hm_lvt_56ba7884d3bf128f739cc872be9cf063=1700030716,1700110221; lf_reader_num_27=1; lf_read_log=think%3A%7B%2228%22%3A%2227%257C6505b0aac7964%257C1700035212%22%2C%22184526%22%3A%22185963%257C178e40073b1cc%257C1700055432%22%2C%22393%22%3A%22363%257C05aa97ed06940%257C1700120523%22%7D; reader_config_web=0%7C18%7C1%7C0%7C1; lf_reader_num_185963=1; lf_reader_num_363=7; Hm_lpvt_56ba7884d3bf128f739cc872be9cf063=1700120526; PHPSESSID=ldsip41voo53qfrsbjm3nnbj98; lf_user_auth=think%3A%7B%22uid%22%3A%22101350%22%2C%22username%22%3A%22cxk%22%7D; lf_user_auth_sign=bab8f2a9fc16750f8f4137f6260fe67a17593eb8; lf_user_recommend=1700120522',
    '__51vcke__K2jtTf36F5UaO7Vp=fe97124e-9481-5cee-9d3e-db9a04bbc9fa; __51vuft__K2jtTf36F5UaO7Vp=1699947989479; lf_reader_num_184263=1; reader_config_web=0%7C18%7C1%7C0%7C1; lf_reader_num_40608=1; lf_reader_num_186155=1; fontsize=100px; __51uvsct__K2jtTf36F5UaO7Vp=8; lf_reader_num_363=5; PHPSESSID=bqjd7kkhc5lvs9vlrlsse9gtn1; lf_user_auth=think%3A%7B%22uid%22%3A%22100596%22%2C%22username%22%3A%22litohong%22%7D; lf_user_auth_sign=75057c50df6248b342c926e9085591c150168915; lf_user_recommend=1700067105; lf_read_log=think%3A%7B%22182822%22%3A%22184263%257C0bb3993a22eab%257C1699949720%22%2C%2239154%22%3A%2240608%257Cd27fd6d76bdaf%257C1699950362%22%2C%22184718%22%3A%22186155%257C6b1c6c4c5bba7%257C1700023377%22%2C%22393%22%3A%22363%257C05aa97ed06940%257C1700067105%22%7D; __vtins__K2jtTf36F5UaO7Vp=%7B%22sid%22%3A%20%2210b7f733-610a-5643-970c-dca25b683bf2%22%2C%20%22vd%22%3A%206%2C%20%22stt%22%3A%20175017%2C%20%22dr%22%3A%2051586%2C%20%22expires%22%3A%201700068906576%2C%20%22ct%22%3A%201700067106576%7D',
    'lf_reader_num_363=1; reader_config_web=0%7C18%7C1%7C0%7C1; Hm_lvt_56ba7884d3bf128f739cc872be9cf063=1700120628; PHPSESSID=ivbsofs97g7jtafjl06cq4g3rl; lf_user_auth=think%3A%7B%22uid%22%3A%22101354%22%2C%22username%22%3A%22wynn%22%7D; lf_user_auth_sign=f84935fbe1a2417e1f517cfdf106b1cca204aaa0; lf_user_recommend=1700120731; lf_read_log=think%3A%7B%22393%22%3A%22363%257C05aa97ed06940%257C1700120731%22%7D; Hm_lpvt_56ba7884d3bf128f739cc872be9cf063=1700120734',
    'Hm_lvt_56ba7884d3bf128f739cc872be9cf063=1700125805; PHPSESSID=tkconbkv3v12p8neth9silvfce; lf_user_auth=think%3A%7B%22uid%22%3A%22101461%22%2C%22username%22%3A%22ybb%22%7D; lf_user_auth_sign=6642b425e57284439e5af740e572a0ae2b80e047; lf_user_recommend=1700125875; lf_read_log=think%3A%7B%222915%22%3A%224371%257C03705710f19e9%257C1700125936%22%7D; reader_config_web=0%7C18%7C1%7C0%7C1; Hm_lpvt_56ba7884d3bf128f739cc872be9cf063=1700125939'

]


# 遍历文件夹中的所有文件和文件夹
def traversal_dirs(path):
    dirs = []
    files = []
    for item in os.scandir(path):
        if item.is_dir():
            dirs.append(item.path)

        elif item.is_file():
            files.append(item.path)
    return dirs


dir_list = traversal_dirs(r'.\rest')
df = pd.read_csv('./my_file/filter_data.csv', encoding='utf-8-sig')

for dir in dir_list:
    novel_name = dir.split('\\')[-1]

    print("============================================================")
    print(f'开始处理 {novel_name}')

    pattern = r"\[\'(.*)\'\]"
    author = re.search(pattern, df[df['title'] == novel_name]['author'].values[0]).group(1)
    id = df[df['title'] == novel_name]['business_url'].values[0].split('/')[-1]

    csv_path = f'{dir}\\chapter_data.csv'
    chapter_data = pd.read_csv(csv_path, encoding='utf-8-sig')

    epub_name = f'.\\total\\{novel_name}.epub'

    toc_items = []

    book = epub.EpubBook()
    book.set_cover("image.jpg", open(f'{dir}\\cover.jpg', 'rb').read())

    book.set_title(novel_name)
    book.set_identifier(id)
    book.set_language('zh-CN')
    book.add_author(author)

    for index, row in tqdm(chapter_data.iterrows(), desc="Downloading chapters", total=len(chapter_data)-1):
        chapter_url = row['URL']
        chapter_name = row['Title']
        headers = {
            'Host': 'www.ysg0.com',
            'Cookie':random.choice(cookies),
            'Referer': 'https://www.ysg0.com/user/user/login.html',
            'Connection': 'keep-alive',
            'User-Agent': u.pc()
        }

        retry_count = 1
        while retry_count < 21:  # 设置最大重试次数
            try:
                chapter_response = requests.get(chapter_url, headers = headers)
                rest_time = round(random.uniform(0, retry_count + 1), 2)
                sleep(rest_time)
                soup = BeautifulSoup(chapter_response.content, 'html.parser')

                paragraphs = soup.find_all('div', class_ = 'read-content j_readContent')[0].find_all('p')

            except Exception as e:
                if retry_count == 1:
                    tqdm.write(f"错误：{e}")
                    tqdm.write(f"{row['Title']} 获取失败，正在尝试重试...")
                tqdm.write(f"第 ({retry_count}/20) 次重试获取章节内容")
                retry_count += 1  # 否则重试
                continue

            if paragraphs:
                break  # 如果成功获取章节内容，跳出重试循环
            else:
                if retry_count == 1:
                    tqdm.write(f"{row['Title']} 获取失败，正在尝试重试...")
                tqdm.write(f"第 ({retry_count}/20) 次重试获取章节内容")
                # 获取当前时间
                current_time = datetime.datetime.now()
                # 构建要写入日志的内容
                log_message = f"[{current_time}] [{novel_name}] [{chapter_name}] 未找到段落paragraphs {retry_count} 次"
                with open('./my_file/error.log', 'a') as file:
                    file.write(log_message + '\n')
                retry_count += 1  # 否则重试

        if retry_count == 21:
            tqdm.write(f"无法获取章节内容: {row['Title']}，跳过。")
            error_message = chapter_response.text
            with open('./my_file/error.txt', 'a', encoding='utf-8') as file:
                file.write(str(error_message))
                file.write('\n')
                file.write(str(headers))
                file.write('\n')
                file.write('\n')
                file.write('\n')
            continue  # 重试次数过多后，跳过当前章节

        if re.search(r'本文 来自(.*)', paragraphs[-1].text):
            paragraphs.pop()

        chapter_content = ''

        # 添加章节标题到正文中
        chapter_content += f'<p style="font-family: 思源宋体; font-size: 24px; font-weight: bold;">{chapter_name}</p>'
        chapter_content += f'<p style="font-family: 微软雅黑"></p>'

        # 将段落转为str
        str_paragraphs = ""
        for p in paragraphs:
            text = p.get_text().strip()
            str_paragraphs += text + "\n"

        # 定义要匹配的模式
        pattern = re.compile(r'\n>>>(.*?)最新章节', re.DOTALL)
        cleaned_text = re.sub(pattern, '', str_paragraphs)

        # 按照换行符分割文本成为一个段落列表
        str_paragraphs_list = cleaned_text.split('\n')

        # 添加 HTML 标签，生成包含段落的列表
        html_paragraphs = [f"<p style='font-family: 微软雅黑'>{para}</p>" for para in str_paragraphs_list if para.strip()]

        for paragraph in html_paragraphs:
            chapter_content += paragraph

        # 创建章节
        epub_chapter = epub.EpubHtml(title=chapter_name, file_name=f'chapter_{index+1}.xhtml')
        epub_chapter.content = chapter_content

        # 添加章节到书籍
        book.add_item(epub_chapter)
        toc_items.append(epub.Link(f'chapter_{index + 1}.xhtml', f"{row['Title']}", f'chapter{index + 1}'))

        print(f"{row['Title']} 已添加到epub")

        rest_time = round(random.uniform(1, 3), 2)
        sleep(rest_time)

    book.toc = tuple(toc_items)

    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # 生成epub文件
    epub.write_epub(epub_name, book)

    rest_time = round(random.uniform(2, 4), 2)
    sleep(rest_time)

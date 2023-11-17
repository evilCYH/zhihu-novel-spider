# -*- coding: utf-8 -*-
import pandas as pd

df = pd.read_csv('./my_file/data.csv', encoding='utf-8-sig')

# 对 title 列进行正则替换，只保留中文、英文和数字
df['title'] = df['title'].str.replace(r'[^\u4e00-\u9fff\w\s]', ' ', regex=True)
# 替换多个连续空格为一个空格
df['title'] = df['title'].str.replace(r'\s+', ' ', regex=True).str.strip()

df.to_csv('./my_file/filter_data.csv', encoding='utf-8-sig', index=False)
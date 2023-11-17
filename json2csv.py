import json
import csv

filename = './my_file/api_data.json'
with open(filename, encoding='utf-8') as f:
    api_data = json.load(f)

booklist = api_data['data']
key_list = booklist[0].keys()

with open('./my_file/origin_data.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    fieldnames = key_list
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # 写入表头
    writer.writeheader()

    # 写入数据行
    for row in booklist:
        writer.writerow(row)

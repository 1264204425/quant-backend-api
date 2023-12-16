import pandas as pd
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import requests
import time
import os


# Create your views here.
def update_ahr999():
    url = 'https://ahr999.178711.com/data.json'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    response = requests.get(url, headers=headers)

    data = response.json()
    count = 0
    dates = []
    for sublist in data:
        timestamp = sublist[0]
        day = time.strftime('%Y/%m/%d', time.localtime(timestamp / 1000))
        value = sublist[1]
        dates.append((day, value))
        # dates.append((day, value))
        # count += 1
        # print(f"day: {day}, Value: {value}")
        # print(f"Total: {count}")
    print(dates)
    # 导出数据到 Excel 文件
    current_dir = os.getcwd()
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
    output_dir = os.path.join(parent_dir + '\\quant\\static\\data\\ahr999.csv')
    # print(output_dir)
    print(output_dir)
    df = pd.DataFrame(dates, columns=['day', 'value'])
    df.to_csv(output_dir, index=False)


@login_required
def ahr999_view(request):
    update_ahr999()
    df1 = pd.read_csv('static/data/ahr999.csv')
    day = df1['day']
    # # 将时间字符串转换为时间戳
    # times = pd.to_datetime(day)
    # # 获取年月日信息
    # times_ymd = times.dt.strftime("%Y/%m/%d")
    times_ymd = day
    # 将时间放入列表
    date_list = times_ymd.tolist()

    ahr999 = df1['value'].tolist()
    ahr999 = str(ahr999).replace("'", "")
    print(date_list)
    print(ahr999)
    return render(request, 'user/ahr999.html', locals())

# -*- coding = utf-8 -*-
# @Time : 2021/6/3 15:54
# @Author : toast
# @File : spider_picture.py
# @Software : PyCharm


"""
https://mp.weixin.qq.com/s/ZcAJ_SMDNzBvKrAZLy2oOg
"""

from bs4 import BeautifulSoup  # 网页解析，获取数据
import re  # 正则表达式，进行文字匹配
import urllib.request, urllib.error  # 制定URL，获取网页数据
import os
import time
import requests

baseurl = "https://mp.weixin.qq.com/s/ZcAJ_SMDNzBvKrAZLy2oOg"


# 得到指定一个URL的网页内容
def askURL(url):
    head = {  # 模拟浏览器头部信息，向服务器发送消息
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 80.0.3987.122  Safari / 537.36"
    }
    # 用户代理，表示告诉服务器，我们是什么类型的机器、浏览器（本质上是告诉浏览器，我们可以接收什么水平的文件内容）

    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


# 保存图片到本地
def save_to_txt(results, name, i):
    # 在当目录下创建文件夹
    if not os.path.exists('./' + name):
        os.makedirs('./' + name)
    # 下载图片
    for result in results:
        print('正在保存第{}个'.format(i))
        try:
            pic = requests.get(result, timeout=10)
            time.sleep(1)
        except:
            print('当前图片无法下载')
            continue
        # 把图片保存到文件夹
        file_full_name = './' + name + '/' + str(i) + '.jpg'
        with open(file_full_name, 'wb') as f:
            f.write(pic.content)


# <p><img class="rich_pages" data-ratio="1.4143145161290323" data-s="300,640" data-src="(.*?)" data-type="png" data-w="992" style=""/></p>


find_url = re.compile(
    r'<p><img class="rich_pages" data-ratio="1.4143145161290323" data-s="300,640" data-src="(.*?)" data-type="png" data-w="992" style=""/></p>')

name = "picture"
if not os.path.exists('./' + name):
    os.makedirs('./' + name)

# 获取图片链接
url = baseurl
html = askURL(url)  # 保存获取到的网页源码
# 2.逐一解析数据
soup = BeautifulSoup(html, "html.parser")
i = 0
for item in soup.find_all("p"):  # 查找符合要求的字符串，形成列表
    # print(item)   #测试：查看item全部信息
    item = str(item)
    URL = re.findall(find_url, item)
    if URL:
        print(URL)
        save_to_txt(URL, name, i)
        i = i + 1
from bs4 import BeautifulSoup  # 网页解析，获取数据
import urllib.request  # 制定URL，获取网页数据
import json

# import re  # 正则表达式，进行文字匹配
'''
cn_en_dic = {'confirm': "确诊",
             'suspect': "疑似",
             'heal': "治愈",
             'dead': "死亡",
             'severe': "重症",
             'storeConfirm': "现存确诊",
             'input': "输入",
             'noSymptom': "无症状",
             'incrNoSymptom': "新增无症状"}
'''


def ask_url(url):
    head = {  # 模拟浏览器头部信息，向服务器发送消息
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) "
                      "AppleWebKit / 537.36(KHTML, like Gecko) Chrome "
                      "/ 80.0.3987.122  Safari / 537.36"
    }
    # 用户代理（本质上是告诉浏览器，我们可以接收什么水平的文件内容）
    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


def get_map_data():
    # 1.爬取网页
    url = "https://c.m.163.com/ug/api/wuhan/app/data/list-total?t=316578012887"  # 要爬取的网页链接
    data = {}
    html = ask_url(url)  # 保存获取到的网页源码
    # 2.逐一解析数据
    soup = BeautifulSoup(html, "html.parser")
    html = json.loads(html)
    temp = html['data']['chinaTotal']
    temp['lastUpdateTime'] = html['data']['areaTree'][2]['lastUpdateTime']
    data['chinaTotal'] = temp
    temp = html['data']['areaTree'][2]['children']
    x = []  # 存储数据
    for item in temp:
        y = {}  # 存储各省数据
        y['name'] = item['name']
        y['today'] = item['today']
        y['total'] = item['total']
        y['lastUpdateTime'] = item['lastUpdateTime']
        z = []
        for value in item['children']:
            o = {}
            o['name'] = value['name']
            o['today'] = value['today']
            o['total'] = value['total']
            o['lastUpdateTime'] = value['lastUpdateTime']
            z.append(o)
        y['children'] = z
        x.append(y)
    # print(x)
    data['data'] = x
    # print(data)
    return data


def get_time_data():
    url = "https://c.m.163.com/ug/api/wuhan/app/data/list-total?t=316578012887"  # 要爬取的网页链接
    data = {}
    html = ask_url(url)  # 保存获取到的网页源码
    soup = BeautifulSoup(html, "html.parser")
    html = json.loads(html)
    temp = html['data']['chinaTotal']
    temp['lastUpdateTime'] = html['data']['areaTree'][2]['lastUpdateTime']
    data['chinaTotal'] = temp
    temp = html['data']['chinaDayList']
    # print(temp)
    x = []  # 存储数据
    for item in temp:
        y = {}  # 存储各省数据
        y['data'] = item['date']
        y['today'] = item['today']
        y['total'] = item['total']
        x.append(y)
    # print(x)
    data['data'] = x
    return data


##测试
def get_city():
    # 1.爬取网页
    url = "https://c.m.163.com/ug/api/wuhan/app/data/list-total?t=316578012887"  # 要爬取的网页链接
    data = {}
    html = ask_url(url)  # 保存获取到的网页源码
    # 2.逐一解析数据
    soup = BeautifulSoup(html, "html.parser")
    html = json.loads(html)
    temp = html['data']['areaTree'][2]['children']
    x = []  # 存储数据
    for item in temp:
        y = {}
        y['value'] = item['name']
        y['label'] = item['name']
        z = []
        for value in item['children']:
            o = {}
            o['value'] = value['name']
            o['label'] = value['name']
            z.append(o)
        y['children'] = z
        x.append(y)
    # print(x)
    return x


# import urllib.request, urllib.error  # 制定URL，获取网页数据
if __name__ == '__main__':
    get_time_data()

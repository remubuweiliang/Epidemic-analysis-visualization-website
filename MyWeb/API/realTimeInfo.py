from bs4 import BeautifulSoup  # 网页解析，获取数据
import urllib.request  # 制定URL，获取网页数据
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys  # 键盘导入类
from time import sleep
import re  # 正则表达式，进行文字匹配

'''
# find_element_by_name 通过name查找单个元素
# find_element_by_xpath 通过xpath查找单个元素
# find_element_by_link_text 通过链接查找单个元素
# find_element_by_partial_link_text 通过部分链接查找单个元素
# find_element_by_tag_name 通过标签名称查找单个元素
# find_element_by_class_name 通过类名查找单个元素
# find_element_by_css_selector 通过css选择武器查找单个元素
# find_elements_by_name 通过name查找多个元素
# find_elements_by_xpath 通过xpath查找多个元素
# find_elements_by_link_text 通过链接查找多个元素
# find_elements_by_partial_link_text 通过部分链接查找多个元素
# find_elements_by_tag_name 通过标签名称查找多个元素
# find_elements_by_class_name 通过类名查找多个元素
# find_elements_by_css_selector 通过css选择武器查找多个元素

btn_more = browser.find_element_by_id('btn_more')
print(btn_more.get_attribute('class')) # 获取属性
print(btn_more.get_attribute('href')) # 获取属性
print(btn_more.text) # 获取文本值

btn_more.click() # 模拟点击,可以模拟点击加载更多
input_search = browser.find_element(By.ID,'q')
input_search.clear() # 清空输入

# 执行JavaScript脚本
browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
browser.execute_script('alert("To Bottom")')

driver.find_element_by_id('kw').send_keys(Keys.BACK_SPACE)  # 删除键    #删除多输入的一个字
driver.find_element_by_id('kw').send_keys(Keys.SPACE)  # 输入空格键
driver.find_element_by_id('kw').send_keys(Keys.CONTROL, 'a')  # 输入Control+a模拟全选
driver.find_element_by_id('kw').send_keys(Keys.CONTROL, 'c')  # 输入Control+c模拟复制
driver.find_element_by_id('kw').click()  # 单击之后鼠标焦点就在文字后面了，不然还在文字上，粘贴就会直接覆盖文字
driver.find_element_by_id('kw').send_keys(Keys.CONTROL, 'v')  # 输入Control+v模拟粘贴
driver.find_element_by_id('kw').click()
driver.find_element_by_id('kw').send_keys(Keys.ENTER)  # 回车键
'''

# findImgSrc = re.compile(r'<img.*src="(.*?)"', re.S)
# findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
# findJudge = re.compile(r'<span>(\d*)人评价</span>')
# findInq = re.compile(r'<span class="inq">(.*)</span>')
# findBd = re.compile(r'<p class="">(.*?)</p>', re.S)
findLink = re.compile(r'<a href="(.*?)" target="_blank">')  # 创建正则表达式对象，标售规则   影片详情链接的规则
# findTitle = re.compile(r'<h2><a href="(.*) " target="_blank">(.*?) 第二个匹配分组</a></h2>')
findTitle = re.compile(r'<h2>\n<a href="(.*?)" target="_blank">(.*?)\n</h2>')
findSubTitle = re.compile(r'<p>(.*)</p>')
findTime = re.compile(r'<p>\n(.*?)<span>(.*?)</span>\n</p>')
findDetailTitle = re.compile(r'<h1 class="news_title">(.*)</h1>')
findContent = re.compile(r'<div class="news_txt" data-size="standard">(.*?)</div>\n<div class="go_to_topic">')


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


# 资讯主页面爬取
def get_real_time_info(find):
    options = webdriver.ChromeOptions()
    # 静默模式
    options.add_argument("headless")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    browser = webdriver.Chrome(chrome_options=options)  # 指定和打开浏览器
    # browser = webdriver.Chrome()  # 指定和打开浏览器
    try:
        # get打开指定的url，传入要打开的url
        browser.get('https://www.thepaper.cn/searchResult.jsp')
        # 通过find_element_by_name获取到网页标签，send_keys()输入内容,在搜索栏输入python
        browser.find_element_by_class_name('sc_inp').send_keys(find)  # 在输入框输入内容
        sleep(1)
        browser.find_element_by_class_name('sc_inp').send_keys(Keys.ENTER)  # 回车键
        soup = BeautifulSoup(browser.page_source, "html.parser")
        # html = json.loads(browser.page_source)
        datalist = []
        for item in soup.find_all('div', class_="search_res"):  # 查找符合要求的字符串\
            data = {}
            item = str(item)
            data['link'] = '/real_time_info/' + re.findall(findLink, item)[0]  # 通过正则表达式查找
            # x = re.findall(findLink, item)[0]  # 通过正则表达式查找
            # data['link'] = "https://www.thepaper.cn/" + x
            data['titles'] = re.findall(findTitle, item)[0][1]
            data['subTitles'] = re.findall(findSubTitle, item)[0]
            datalist.append(data)
        browser.close()
        return datalist
    except Exception as e:
        print("模拟登录失败：{}".format(e))
        browser.close()
        pass


def get_detail(url):
    url = "https://www.thepaper.cn/" + url  # 要爬取的网页链接
    html = ask_url(url)  # 保存获取到的网页源码
    soup = BeautifulSoup(html, "html.parser")
    # html = json.loads(browser.page_source)
    data = {}
    try:
        for item in soup.find_all('div', class_="newscontent"):  # 查找符合要求的字符串\
            item = str(item)
            data['titles'] = re.findall(findDetailTitle, item)[0]
            data['time'] = []
            data['time'].append(re.findall(findTime, item)[0][0].replace("&", ""))
            data['time'].append(re.findall(findTime, item)[0][1])
            data['content'] = re.findall(findContent, item)[0]
        # print(data)
        # print(type(data))
        return data
    except:
        pass


if __name__ == '__main__':
    get_real_time_info("佛山")
    # get_detail('newsDetail_forward_13194712')

import requests
import json
import re
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

url = 'http://www.acfun.cn/v/list73/index.htm'
browser = webdriver.Chrome()
browser.get(url)
response = browser.page_source
browser.close()
pattern = re.compile('<a href="(/a/ac\d+)"')
ros = pattern.findall(response)
print(ros)
# a = response.find_all('', {'class': 'act-cont-top clearfix'})


# selenium实现
#browser = webdriver.Chrome()
#browser.get('http://www.acfun.cn/v/list73/index.htm')
#lis = browser.find_elements_by_css_selector('.act-cont-top.clearfix a')
#for i in lis:
    #print(i.get_attribute("href"))
#browser.close()

# json 实现
#import requests
#import json
# 请求heaaders
#response = requests.get('http://webapi.aixifan.com/query/article/list?pageNo=1&size=10&realmIds=6%2C7&originalOnly=false&orderType=1&periodType=-1&filterTitleImage=true')
#response = response.json()
#response = response['data']['articleList']
#for i in response:
    #print(i['id'])


# print(response)

# browser = webdriver.Chrome()
# browser.get('http://www.acfun.cn/v/list73/index.htm')
# print(browser)
# browser.close()
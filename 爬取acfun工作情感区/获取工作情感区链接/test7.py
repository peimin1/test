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

# print(response)

# browser = webdriver.Chrome()
# browser.get('http://www.acfun.cn/v/list73/index.htm')
# print(browser)
# browser.close()
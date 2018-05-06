from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import random
import string

url = "http://www.acfun.cn/a/ac4335460"

response = urlopen(url)
html = response.read().decode('utf-8')
soup = BeautifulSoup(html, features='lxml')
a = soup.find('', {'class': 'caption'}).get_text()
with open('./img/acfun.txt', 'w', encoding='utf-8') as f:
    f.write(a + '\n')
b = soup.find('', {'class':'article-content'}).find_all('p')
for i in b:
    with open('./img/acfun.txt', 'a', encoding='utf-8') as f:
        f.write(i.text + '\n')
    print(i.text)


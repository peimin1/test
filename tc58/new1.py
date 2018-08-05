import requests
import os

html = requests.get('https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1490350083846&di=01e5ca0ce5499719c43f5d1e9f75d8c9&imgtype=0&src=http%3A%2F%2Fwww.th7.cn%2Fd%2Ffile%2Fp%2F2016%2F05%2F03%2F9e9ce32b8128ad84229ccc69f8c2e6c9.jpg')
with open('picture.jpg', 'wb') as file:
    file.write(html.content)

current_path = os.path.abspath(__file__)
b = os.path.abspath(os.path.dirname(current_path)) + '\picture.jpg'
print(b)
print(os.path.abspath(os.path.dirname(current_path) + os.path.sep + "."))
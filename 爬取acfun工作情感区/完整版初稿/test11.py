import requests
import time
from bs4 import BeautifulSoup
from urllib.request import urlopen
from multiprocessing import Pool


def acfun(url, id):
    url = url
    response = urlopen(url)
    html = response.read().decode('utf-8')
    soup = BeautifulSoup(html, features='lxml')
    a = soup.find('', {'class': 'caption'}).get_text()
    with open('./img/' + id + '.txt', 'w', encoding='utf-8') as f:
        f.write('标题:' + a + '\n\n')
    b = soup.find('', {'class': 'article-content'}).find_all('p')
    for i in b:
        with open('./img/' + id + '.txt', 'a', encoding='utf-8') as f:
            f.write(i.text + '\n')
        # print(i.text)


def main(i):

    allurl = []
    response = requests.get('http://webapi.aixifan.com/query/article/list?pageNo=' + str(i) +
                            '&size=10&realmIds=6%2C7&originalOnly=false&orderType=1&periodType=-1&filterTitleImage=true')
    # response.json() 与 json.load(response.text)的写法是一样的，将json数据转化为字典
    r = response.json()
    s = r['data']['articleList']
    for i in s:
        acfun('http://www.acfun.cn/a/ac' + str(i['id']), str(i['id']))
        allurl.append(i['id'])
    print(allurl)


if __name__ == '__main__':
    print(time.time())
    # for i in range(1, 4):
    #     main(i)
    pool = Pool()
    pool.map(main, [i + 1 for i in range(3)])
    print(time.time())

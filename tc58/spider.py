import time
import random
import re
from bs4 import BeautifulSoup
import requests
import pymongo
import redis
from .ips import ips
from .user_agent_proxy import user_agents

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'}
url = 'http://sz.58.com/ershoufang/34980703772340x.shtml'


def city_url(url):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6'}
    proxies = {'https': '112.193.131.17:8118'}
    res = requests.get(url, headers=headers, proxies=proxies).content.decode('utf-8')
    all_city_url = re.findall(r'<a href="(//.*?/ershoufang/)" onclick=".*?">.*?</a>', res)
    set_all_City_url = set(all_city_url)
    all_city_url = list(set_all_City_url)
    full_url = []
    for i in all_city_url:
        full_url.append('http:' + i)
    return full_url


def house_url(url):
    res = requests.get(url).text
    soup = BeautifulSoup(res, 'lxml')
    try:
        last_page = soup.find('', {'class': 'next'}).previous_sibling.text
        all_house_url = []
        for i in range(1, int(last_page) + 1):
            full_url = url + 'pn' + str(i) + '/'
            all_house_url.append(full_url)
        return all_house_url
    except:
        pass


def detail_house(url):
    res = requests.get(url).text
    soup = BeautifulSoup(res, 'lxml')
    response = soup.find_all('', {'class': 'title'})
    all_detail_urls = []
    for i in response:
        all_detail_urls.append(i.find('a')['href'])
    return all_detail_urls


def detail_house(url):
    res = requests.get(url, headers=headers).text
    soup = BeautifulSoup(res, 'lxml')
    title = soup.find('h1', {'class': 'c_333'}).text
    total_price = soup.find('', {'class': 'price'}).text
    unit_price = soup.find('', {'class': 'unit'}).text
    house_type = soup.select('#generalSituation > div > ul.general-item-left > li > span')[3].text.strip()
    name = re.findall(r'"userName":(.*),"userid":', res)[0].encode('utf-8').decode("unicode-escape")
    phone_num = soup.find('', {'class': 'phone-num'}).text
    area = soup.select('#generalSituation > div > ul.general-item-left > li > span')[5].text.strip()
    house_orientation = soup.select('#generalSituation > div > ul.general-item-left > li > span')[7].text
    storey = soup.select('#generalSituation > div > ul.general-item-right > li > span')[1].text
    decorate = soup.select('#generalSituation > div > ul.general-item-right > li > span')[3].text
    property_right = soup.select('#generalSituation > div > ul.general-item-right > li > span')[6].text
    architectural_age = soup.select('#generalSituation > div > ul.general-item-right > li > span')[8].text
    premises = soup.find('', {'class': 'c_000 mr_10'}).find('a').text.strip()
    positions = soup.find_all('', {'class': 'c_000 mr_10'})[1].find_all('a')

    position = ''
    for i in positions:
        position += i.text.strip().replace(' ', '')
    img_urls_css = soup.select('#leftImg > li > img')
    img_urls = []
    for i in img_urls_css:
        img_urls.append(i.attrs['data-value'])
    describes_soup = soup.find('', {'class': 'general-item general-desc'}).select('p')
    describes = ''
    for i in describes_soup:
        describes += i.text.strip()

    item = {
        'title': title,
        'total_price':total_price,
        'unit_price': unit_price,
        'house_type': house_type,
        'name': name,
        'phone_num': phone_num,
        'area': area,
        'house_orientation': house_orientation,
        'storey': storey,
        'decorate': decorate,
        'property_right': property_right,
        'architectural_age': architectural_age,
        'premises': premises,
        'position': position,
        'img_urls': img_urls,
        'describes': describes,
    }
    return item


def pipline(data, db):
    # 保存图片需要在详细思考一下
    db.insert(data)

def get_url():
    pass

def mongo_connect():
    client_mongo = pymongo.MongoClient(host='47.106.96.225', port=27017)
    return client_mongo


def redis_client():
    client_redis = redis.Redis(host='47.106.96.225', port='6379', password='peimin123!')
    return client_redis

def queue():
    pass


def main():
    # start_url = 'http://www.58.com/ershoufang/changecity/'

    # house_urls = house_url('http://bj.58.com/ershoufang/')

    # detail_house('http://yancheng.58.com/ershoufang/pn2/')

    # print(house_url('http://qd.58.com/ershoufang/'))

   print()

if __name__ == '__main__':
    main()
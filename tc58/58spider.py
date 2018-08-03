# -*- coding:utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup
import pymongo
import redis

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'}
url = 'http://sz.58.com/ershoufang/34980703772340x.shtml'

def detail_house(url):

    res = requests.get(url, headers=headers).text
    print(res)
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
    client_mongo = mongo_connect()
    data = detail_house(url)
    pipline(data, client_mongo.tc58.cd)



if __name__ == '__main__':
    main()
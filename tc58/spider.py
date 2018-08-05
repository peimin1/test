import os
import random
import threading
from hashlib import sha1
import time
import queue
import logging
from gridfs import *
import re
from bs4 import BeautifulSoup
import requests
import pymongo
import redis
from tc58.ips import ips
from tc58.user_agent_proxy import user_agents, full_headers

q = queue.Queue()
full_headers = full_headers


def get_random_str():
    list1 = [chr(i) for i in range(65, 91)] + [chr(i) for i in range(97, 123)] + [str(i) for i in range(10)]
    num = random.sample(list1, 8)
    str1 = ''
    value = str1.join(num)
    return value


def decode_page(page_bytes, charsets=('utf-8',)):
    """

    :param page_bytes: 二进制内容
    :param charsets: 字符编码
    :return: 解码后的代码
    """
    page_html = None
    for charset in charsets:
        try:
            page_html = page_bytes.decode(charset)
            break
        except UnicodeDecodeError as error:
            logging.error('Decode:', error)
            pass
    return page_html


# 获取页面的HTML代码, 通过递归实现指定次数的重试操作, 实现3次重试操作
def get_page_html(seed_url, *, retry_times=3, charsets=('utf-8',), timeout=30):
    # timeout
    """

    :param seed_url: 初始url
    :param retry_times: 重复次数
    :param charsets: 字符编码
    :param timeout: 延迟
    :return: 解码后的code
    """
    page_html = None
    try:
        if seed_url.startswith('http://') or seed_url.startswith('https://'):
            proxies = {'https': random.choice(ips)}
            full_headers['User-Agent'] = random.choice(user_agents)
            # print('++++++++++++++当前使用的请求头是%s+++++++++++++++' % full_headers)
            # print('++++++++++++++当前使用的代理ip是%s++++++++++++++' % proxies)
            res = requests.get(seed_url, headers=full_headers, timeout=timeout)
            if res.status_code == 200:
                page_html = decode_page(res.content, charsets)
                soup = BeautifulSoup(page_html, 'lxml')
                # 测试是否能找到指定内容, 如果不能找到, 那么返回的就是错误的界面
                try:
                    test1 = soup.find('', {'class': 'pager'}).text
                except:
                    test2 = soup.find('h1', {'class': 'c_333'}).text
                return page_html
    except Exception as error:
        # logging.error('URL:', error)
        # 通过递归,实现URL的重复请求
        logging.error('ERROR: %s' % error)
        if retry_times > 0:
            return get_page_html(seed_url, retry_times=retry_times - 1,
                                 charsets=charsets)
        else:
            # 打印出不能抓取的URL
            print('-----------分割线---------------')
            print('当前URL:{}不能抓取'.format(seed_url))
            return None
    # 如果都没有成功,返回None,没有抓取到该URL
    return page_html


def city_url(url):
    """
    :param url: 58同城二手房的入口链接
    :return: 所有58二手房城市的链接
    """
    res = requests.get(url).content.decode('utf-8')
    all_city_url = re.findall(r'<a href="(//.*?/ershoufang/)" onclick="co.*?">.*?</a>', res)
    set_city_url = set(all_city_url)
    all_city_url = list(set_city_url)
    full_url = []
    for i in all_city_url:
        if i.startswith('//diaoyudao'):
            # 钓鱼岛的网址不能打开, 并且不符合正则表达式, 这里做单独处理
            full_url.append(''.join(['http:', '//cn.58.com/ershoufang/']))
        else:
            full_url.append('http:' + i)
    return full_url


def house_url(url):
    """

    :param url: 58同城城市的url
    :return: 该城市展示出来的所有二手房url
    """
    res = get_page_html(url)
    if res:
        all_house_url = []
        soup = BeautifulSoup(res, 'lxml')
        # 找到最后一页的页数,如果存在,就获取,否则就只有一页
        try:
            last_page = soup.find('', {'class': 'next'}).previous_sibling.text
            for i in range(1, int(last_page) + 1):
                full_url = url + 'pn' + str(i) + '/'
                all_house_url.append(full_url)
            return all_house_url
        except AttributeError:
            # 只有一页的时候的URL
            full_url = url + 'pn' + str(1) + '/'
            all_house_url.append(full_url)
            return all_house_url


def detail_house_url(url):
    """

    :param url: 一个城市的二手房url
    :return: 二手房详细内容的url
    """
    res = get_page_html(url)
    if res:
        soup = BeautifulSoup(res, 'lxml')
        response = soup.find_all('', {'class': 'title'})
        all_detail_urls = []
        for i in response:
            state_url = i.find('a')['href']
            # 存在//和http://开头的链接, 需要处理
            if state_url.startswith('http://'):
                all_detail_urls.append(state_url)
            else:
                right_url = ''.join(['http:', state_url])
                all_detail_urls.append(right_url)
        return all_detail_urls


def detail_house_content(url):
    """

    :param url: 二手房详细的url
    :return: 抓取的数据
    """

    res = get_page_html(url)
    if res:
        soup = BeautifulSoup(res, 'lxml')
        title = soup.find('h1', {'class': 'c_333'}).text  # 标题
        create_time = soup.find('', {'class': 'up', 'id': ''}).text  # 发表时间
        total_price = soup.find('', {'class': 'price'}).text  # 总价
        unit_price = soup.find('', {'class': 'unit'}).text.replace('\xa0', '')  # 单价
        house_type = soup.select('#generalSituation > div > ul.general-item-left > li > span')[3].text.strip()  # 户型
        try:
            name = re.findall(r'"userName":(.*),"userid":', res)[0].encode('utf-8').decode("unicode-escape")  # 经纪人名称
        except IndexError as e:
            logging.error('name IndexError: {}'.format(e))
            name = ''
        phone_num = soup.find('', {'class': 'phone-num'}).text  # 经纪人电话
        area = soup.select('#generalSituation > div > ul.general-item-left > li > span')[5].text.strip()  # 房屋面积
        try:
            house_orientation = soup.select('#generalSituation > div > ul.general-item-left > li > span')[7].text
        except IndexError as e:
            logging.error('house_orientation IndexError: {}'.format(e))
            house_orientation = ''  # 房屋朝向
        storey = soup.select('#generalSituation > div > ul.general-item-right > li > span')[1].text  # 房屋楼层
        decorate = soup.select('#generalSituation > div > ul.general-item-right > li > span')[3].text  # 装修情况
        try:
            property_right = soup.select('#generalSituation > div > ul.general-item-right > li > span')[6].text  # 房屋产权
        except IndexError as e:
            logging.error('property_right IndexError: {}'.format(e))
            property_right = ''
        try:
            architectural_age = soup.select('#generalSituation > div > ul.general-item-right > li > span')[8].text
        except IndexError as e:
            logging.error('architectural_age IndexError: {}'.format(e))
            architectural_age = ''  # 建筑年代
        premises = soup.find('', {'class': 'c_000 mr_10'}).text.strip().replace(' ', '').replace('\n', '')  # 楼盘
        positions = soup.find_all('', {'class': 'c_000 mr_10'})[1].find_all('a')  # 房屋位置
        position = ''
        for i in positions:
            position += i.text.strip().replace(' ', '')

        img_urls_css = soup.select('#leftImg > li > img')
        img_urls = []
        for i in img_urls_css:
            img_urls.append(i.attrs['data-value'])

        item = {}

        # 图片的存储选择存路径还是二进制，mongodb中采用gridfs存储大文件
        # 第一种方法, 图片存储在本地, 将路径存储在mongodb中
        img_paths = []
        for i in img_urls:
            res = get_img_content(i)
            filename = get_random_str() + str(time.time()) + '.jpg'  # 生成一个独一无二的文件名
            with open(filename, 'wb') as f:
                f.write(res)
            current_file = os.path.abspath(__file__)
            img_path = os.path.abspath(os.path.dirname(current_file)) + '\\' + filename
            img_paths.append(img_path)

        describes_soup = soup.find('', {'class': 'general-item general-desc'}).select('p')  # 房屋描述
        describes = ''
        for i in describes_soup:
            describes += i.text.strip()

        item.update({
            'title': title,
            'create_time': create_time,
            'total_price': total_price,
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
            # 'img_urls': img_urls,
            'describes': describes,
            'img_paths': img_paths
        })
        return item


def pipline(data, db):
    # 存储数据到mongodb中
    db.insert(data)

    # mongo_client = MongoClient('127.0.0.1', 27017)
    # mongo_db = mongo_client.test7
    # mongo_col = mongo_db.test
    # mongo_fs = GridFS(mongo_db, collection='coll_image')
    # img_id = mongo_fs.put(image, filename=filename )  # 图片插入mongo
    # mongo_dict['img_id'] = img_id


def get_img_content(url):
    res = requests.get(url, headers=full_headers).content
    return res
    # mongo_fs = GridFS(mongo_db, collection='coll_image')


def mongo_connect():
    client_mongo = pymongo.MongoClient(host='47.106.96.225', port=27017)

    return client_mongo


def redis_client():
    client_redis = redis.Redis(host='47.106.96.225', port='6379', password='peimin123!')
    return client_redis


class RedisFilter(object):
    """
    通过redis集合实现URL的去重
    """
    REDIS_SET_NAME = 'tc58'
    REDIS_SET_HOST = '47.106.96.225'
    REDIS_SET_PORT = 6379
    REDIS_sET_PASSWPRD = 'peimin123!'

    def __init__(self):
        self._redis = redis.StrictRedis(host=self.REDIS_SET_HOST, port=self.REDIS_SET_PORT,
                                        password=self.REDIS_sET_PASSWPRD)
        self._name = self.REDIS_SET_NAME

    # 增加指纹
    def add_fp(self, str1):
        fp = self.create_fp(str1)
        print(fp)
        self._redis.sadd(self._name, fp)

    # 判断指纹是否存在
    def exists(self, str1):
        fp = self.create_fp(str1)
        return self._redis.sismember(self._name, fp)

    # 生成指纹
    def create_fp(self, str1):
        s1 = sha1()
        s1.update(self._to_bytes(str1))
        fp = s1.hexdigest()
        return fp

    # 静态方法
    @staticmethod
    def _to_bytes(string):
        if isinstance(string, str):
            return string.encode("utf-8")
        else:
            return string


# 线程类
class MyThread(threading.Thread):
    """
    多线程类, 继承Thread, 重写run方法
    """
    def __init__(self, q):
        global Thread_id
        threading.Thread.__init__(self)
        self.q = q
        self.Thread_id = Thread_id
        Thread_id = Thread_id + 1

    def run(self):
        while True:
            try:
                task = self.q.get(block=True, timeout=1)  # 不设置阻塞的话会一直去尝试获取资源
            except queue.Empty:
                print('Thread',  self.Thread_id, 'end')
                break
            # 取到数据，开始处理（依据需求加处理代码）
            print("Starting ", self.Thread_id)
            print(task)
            self.q.task_done()
            print("Ending", self.Thread_id)


def main():

    count = 0  # 共爬取多少条数据
    not_city_crawing = []  # 未抓取到的城市URL列表, 用于存储抓取失败的URL
    not_house_crawing = []  # 未抓取到的二手房URL列表, 用于存储抓取失败的URL
    not_detail_crawing = []  # 未抓取到二手房具体数据的URL列表, 用于存储抓取失败的URL

    # 初始化redis 和 mongodb
    r = RedisFilter()
    mongo = mongo_connect()

    start_url = 'http://www.58.com/ershoufang/changecity/'
    city_urls = city_url(start_url)

    # 需要开启多线程的时候使用消息队列
    for i in city_urls:
        q.put(i)

    for i in range(len(city_urls)):
        one_city_url = q.get()
        city_name = one_city_url.split('//')[1].split('.')[0]
        print('正在抓取{}城市,URL为:{}'.format(city_name, one_city_url))

        # Thread_num 开启的线程数量 开启多线程的时候使用
        # for i in range(0, Thread_num):
        #     worker = myThread(q)
        #     worker.start()
        # q.join()

        # 按城市存储抓取的数据, 数据库的表名为city_name
        db = mongo.tc58.city_name

        all_house_urls = house_url(one_city_url)  # 该城市分页房源数据

        # 如果抓取成功就继续执行, 否则存入相应抓取失败的URL列表中
        for one_house_url in all_house_urls:
            print(one_house_url)
            detail_urls = detail_house_url(one_house_url)  # 该城市每页具体房源数据
            if detail_urls:
                print(detail_urls)
                for detail_url in detail_urls:
                    print('--------------------分割线---------------------')
                    print('当前url是:%s' % detail_url)
                    if r.exists(detail_url):  # 判断是不是抓取过的房源数据URL, 如果抓取,就不再抓取, 否则, 抓取该URL的数据
                        pass
                    else:
                        if detail_url:
                            full_headers['Referer'] = one_house_url  # 更换请求头的referer, 反反爬
                            item = detail_house_content(detail_url)  # 抓取数据
                            r.add_fp(detail_url)    # 抓取成功后增加摘要到redis集合中
                            pipline(item, db)  # 数据持久化
                            count += 1
                            print('*************当前正在抓取第%d条数据***************' % count)
                            print(item)
                            time.sleep(random.uniform(0.5, 3))  # 随机延迟一个数据
                        else:
                            not_detail_crawing.append(detail_url)
            else:
                not_house_crawing.append(one_house_url)
        print(not_city_crawing)
        print(not_house_crawing)
        print(not_detail_crawing)


if __name__ == '__main__':
    main()

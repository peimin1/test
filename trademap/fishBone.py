import re
import redis
import pymongo
import requests
import logging
from lxml import etree
from pymongo.errors import DuplicateKeyError
from constant import *
conn = redis.Redis(host="", port="")


def deal_requests(method, url, headers, data):
    """重新登录并重新请求"""
    login()
    cookies = conn.get('login_cookie')
    return f_requests(method, url, headers, cookies, data=data)


def reload_requests(method, url, headers, data):
    cookies = conn.get('login_cookie')
    return f_requests(method, url, headers, cookies, data=data)


def f_requests(method, url, headers, proxies='', cookies='', data='', timeout=20):
    """
    2018-12-15 ： 需不需要加载一个封IP的更换方式，不封IP的更换方式
    """
    if method == 'get':
        try:
            res = requests.get(url, headers=headers, proxies=proxies, cookies=cookies, verify=False, timeout=timeout)
            # 判断是否登录或者出现验证码pass
            return res
        except():
            pass

    elif method == 'post':
        cookies = conn.get('login_cookis')
        if cookies:
            try:
                res = requests.post(url, headers=headers, cookies=cookies, data=data, verify=False, timeout=timeout)
                if res.status_code == 200:
                    # 是否登录
                    if is_login():
                        # 是否验证码
                        if is_validate():
                            # 数据是否符合要求
                            return res
                        else:
                            logging.info('出现验证码, 重新登录')
                            return deal_requests(method, url, headers, data=data)
                    else:
                        logging.info('cookies过期， 重新登录cookie')
                        return deal_requests(method, url, headers, data=data)


            except Exception as e:
                logging.info('internet connot conenct !!!, 重新请求')
                return deal_requests(method, url, headers=headers, data=data)
        else:
            logging.info('cookie过期 !!!, 登录')
            return deal_requests(method, url, headers=headers, data=data)


def login():
    return 1


def is_login():
    return 1


def is_validate():
    return 1


if __name__ == '__main__':
    # 需要处理的异常: 1. 判断是否登录(即Cookie是否过期)  2.判断是否出现验证码  3. 判断是否状态码错误
    pass


# 多线程，多进程， 协程， 进程 + 协程等的开启方式
from multiprocessing import Process
from threading import Thread
import time
import asyncio
import aiohttp


def pro(main, number, params):
    """
    多进程开启方式
    :param start: 任务函数
    :param number: 进程数
    :param params: 参数【传入元祖，例如(3,)】
    :return:
    """
    for _ in range(number):
        p = Process(target=main, args=params)
        p.start()
        print("p.name:", p.name)


def vps_pro(start, number, params):
    # 需要注意的是：一些参数需要再进程中初始化，如果直接使用全局变量的话，进程会启动不成功
    pro_list = [
        {'http': 'http://10.0.0.50:9999', 'https': 'http://10.0.0.50:9999'},
        {'http': 'http://10.0.0.51:9999', 'https': 'http://10.0.0.51:9999'},
        {'http': 'http://10.0.0.52:9999', 'https': 'http://10.0.0.52:9999'},
        {'http': 'http://10.0.0.53:9999', 'https': 'http://10.0.0.53:9999'},
        {'http': 'http://10.0.0.54:9999', 'https': 'http://10.0.0.54:9999'}
    ]
    for _ in range(5):
        p = Process(target=start, args=(params, pro_list[_]))
        p.start()
        print("p.name:", p.name)


def thr(start, number, params):
    for _ in range(number):
        t = Thread(target=start, args=params)
        t.start()
        print("t.name:", t.name)


def gev(start, number, params):
    import gevent
    from gevent import socket, monkey
    monkey.patch_all()
    source = []
    for _ in range(number):
        t = gevent.spawn(start, params)
        source.append(t)
    gevent.joinall(source)


def asy(start, number, params):
    pass

    def analy(self, sources):
        semaphore = asyncio.Semaphore(2)
        tasks = [deal_urls(url['href'], semaphore) for url in sources]
        event_loop = asyncio.get_event_loop()  # 事件循环
        results = event_loop.run_until_complete(asyncio.gather(*tasks))
        event_loop.close()  # 关闭事件循环

    async def deal_urls(url, semaphore):
        async with semaphore:
            async with aiohttp.ClientSession() as session:
                print('downing', url)
                async with session.get(url) as html:
                    text = await html.text()
                    print(text)


def pro_gev():
    pass


def parse(*args):
    print('time time')
    time.sleep(3)


if __name__ == "__main__":
    gev(parse, 3, '')

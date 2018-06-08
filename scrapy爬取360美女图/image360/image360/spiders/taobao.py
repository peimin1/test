# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlencode


class TaobaoSpider(scrapy.Spider):
    name = 'taobao'
    allowed_domains = ['www.taobao.com']

    def start_requests(self):
        base_url = 'https://s.taobao.com/search?'
        param = {}
        for keyword in ['ipad', 'iphone', '小米手机']:
            param['q'] = keyword
            for page in range(100):
                param['s'] = page * 44
                full_url = base_url + urlencode(param)
                yield scrapy.Request(url=full_url, callback=self.parse)

    def parse(self, response):
        pass

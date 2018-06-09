# -*- coding: utf-8 -*-
import re
from io import StringIO
import scrapy
from urllib.parse import urlencode

from image360.items import GoodsItem

i = 0

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
                yield scrapy.Request(url=full_url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        item = GoodsItem()
        div_list = response.xpath('//*[@id="mainsrp-itemlist"]/div/div/div[1]/div')
        for elem in div_list:
            global i
            i += 1
            item['discount'] = i
            item['price'] = elem.xpath('div[2]/div[1]/div[1]/strong/text()').extract_first()
            item['address'] = elem.xpath('div[2]/div[3]/div[2]/text()').extract_first()
            item['store_name'] = elem.xpath('div[2]/div[3]/div[1]/a/span[2]/text()').extract_first()
            segments = elem.xpath('div[2]/div[2]/a/text()').extract()
            title = StringIO()
            for segment in segments:
                title.write(re.sub('\s', '', segment))
            item['title'] = title.getvalue()
            yield item

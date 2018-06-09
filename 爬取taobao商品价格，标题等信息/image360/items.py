# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BeautyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    tag = scrapy.Field()
    width = scrapy.Field()
    height = scrapy.Field()
    url = scrapy.Field()


class GoodsItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    goods_url = scrapy.Field()
    store_name = scrapy.Field()
    store_url = scrapy.Field()
    address = scrapy.Field()
    discount = scrapy.Field()
    wangwang_url = scrapy.Field()
    deal = scrapy.Field()
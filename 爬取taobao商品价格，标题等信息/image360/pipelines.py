# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
import logging


# logger = logging.getLogger('SaveImagePipeline')


class SaveImagePipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        yield Request(url=item['url'])

    def item_completed(self, results, item, info):
        # logger.debug('下载完成')
        if not results[0][0]:
            raise DropItem('下载失败')

        return item

    def file_path(self, request, response=None, info=None):
        return request.url.split('/')[-1]


class SaveToMongoPipeline(object):
    def __init__(self, mongo_url, db_name):
        self.mongo_url = mongo_url
        self.db_name = db_name
        self.client = None
        self.db = None
        # conection = pymongo.MongoClient(MONGODB_SERVER, MONGODB_PORT)
        # db = conection[MONGODB_DB]
        # self.collection = db[MONGODB_COLLECTION]

    # def process_item(self, item, spider):
    #     return item

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_url)
        self.db = self.client[self.db_name]
        self.collection = self.db['iamge']

    def process_item(self, item, spider):
        data = [{
            'title': item['title'],
            'tag': item['tag'],
            'width': item['width'],
            'height': item['height'],
            'url': item['url']
        }]
        self.collection.insert(data)


    def close_spider(self, spider):
        self.client.close()

    # 依赖注入方法
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.get('MONGODB_URL'),
                   crawler.settings.get('MONGODB_DB'),
                   )

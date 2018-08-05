import pymongo
from gridfs import *
import requests
import time

client_mongo = pymongo.MongoClient(host='47.106.96.225', port=27017)
mongo_db = client_mongo.test7
mongo_col = mongo_db.test
mongo_fs = GridFS(mongo_db, collection='coll_image')

title = '我在这儿等着你回来，等着你回来，看那桃花开'
img_url = ['https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1533361582882&di=ad58c64e9a83a4ed5923c69352bd6222&imgtype=0&src=http%3A%2F%2Fa5.topitme.com%2Fo025%2F1002536708f56d0bfd.jpg',
           'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1533362132796&di=e75fc45726c48588d8252a74687e8b2a&imgtype=0&src=http%3A%2F%2Fatt.bbs.duowan.com%2Fforum%2F201412%2F19%2F132747jssasjaj4aanpsnc.jpg'
           ]
mongo_dict = {}

for i in img_url:
    image = requests.request(method='get',url=i).content #获取图片内容
    img_id = mongo_fs.put(image,filename = str.replace(title, ' ', '') + str.split(str(time.time()),'.')[0] + '.' + str.split(i, '.')[-1],)
    mongo_dict['img_id'] = img_id
    mongo_col.insert(mongo_dict)






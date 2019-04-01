# mongodb配置
MONGO_MC = 'mongodb://rwuser:48bb67d7996f327b@10.2.1.216:57017,10.2.1.217:57017'
MONGO_IP = 'mongodb://root:root962540@10.0.0.55:27017'
# mongodb 库 集合 表
MONGO_DA = 'atobo_com'
MONGO_CL = 'list_results'
MONGO_DE = 'detail_results'
MONGO_CO = 'complete_results'

# redis 配置
REDIS_HOST = '127.0.0.1'
REDIS_PORT = '6379'
REDIS_DB = '8'
REDIS_COM = ''

# ip 相关库与集合
IP_DATABASE = 'ip_db'
IP_DYNAMC = 'ip_results'
IP_STATIC = 'vps_static_ip_results'

# target 相关库与集合

# 默认请求头和代理
DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'
}
DEFAULT_PROXIES = {'http': 'http://10.0.0.50:9999', 'https': 'http://10.0.0.50:9999'}

# 配置请求头的RULERS
RULERS = []
RULER_404 = ''

# 初始URL
BASE_URL = 'https://www.atobo.com.cn/Companys/'

import re
import requests
from bs4 import BeautifulSoup
import time
import random
from tc58.user_agent_proxy import full_headers

# 测试是否可用
# ip为传入的ip :  0.0.0.0:8000
# test_url 为测试的目标网站, 可以看作你将要爬取得网站
# tiem_out 请求的延迟
def test_ip(ip, test_url='http://wh.58.com/ershoufang/35004226671936x.shtml?fzbref=0&from=1-list-1&psid=150582061200995105861835482&iuType=gz_2&ClickID=1&apptype=0&key=&entinfo=35004226671936_0&params=rankesfjxpclranxuanalphapriceAB5099^desc&cookie=||https%3A%2F%2Fwww.google.com.hk%2F|c5/nn1rHJj4KaL4lJGRfAg&PGTID=0d30000c-0009-e83a-eea3-e06b1d79a347&local=158&pubid=39373778&trackkey=35004226671936_367a0daf-8328-4360-a97a-0b6abc448463_20180805200925_1533470965440&fcinfotype=gz', time_out=0.3):
    proxies = {'https': ip} # 代理
    global all # 使用全局变量
    j = 0
    while j < 3: # 一共测试3次
        try:
            # 请求目标网址
            r = requests.get(test_url, proxies=proxies, timeout=time_out, headers=full_headers)
            # 如果返回的状态码为200, 则表示成功
            if r.status_code == 200:
                print('***************测试通过%s**************' % ip)
                all.append(ip) # 将通过的ip加入到列表中
                break
            else:
                print('请求失败%s' % ip)
        except:
            print('请求过程错误%s' % ip)
        j += 1
        print('-----------------这是第  %d 次测试----------------' % j)

url = 'http://www.xicidaili.com/nn/'
# 请求头池, 也是防止反爬手段的一种
user_list = ["Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3"]
# 设置全局变量, 用来存取测试通过的IP
all = []
# 一个装爬下来IP的容器
ip_list = []
# 爬取20页的数据
for page in range(5, 7):
    url += str(page)
    headers = {
        # 每一次爬取选择随机的请求头
        'User-Agent': random.choice(user_list)
    }
    #每一次爬取随机暂停秒数, 采用是随机浮点数
    time.sleep(random.uniform(0, 4))
  # 解析西刺代理的页面结构
    res = requests.get(url, headers=headers).text
    soup = BeautifulSoup(res, 'lxml')
    ips = soup.find_all('', {'class': 'odd'})
    for ip_ in ips:
        ip = re.findall(r'<td>(.*)</td>', str(ip_))
        ip_list.append(ip[0] + ':' + ip[1])
        print(ip[0] + ':' + ip[1])

# 测试爬取得每个ip
for ip in ip_list:
    test_ip(ip)
# 打印出测试通过的ip, 当然也可以持久化到数据库中或者存放到本地中
print(all)
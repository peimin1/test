from lxml import etree
from fishBone import f_requests


headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, br',
           'Accept-Language': 'zh-CN,zh;q=0.9',
           'Connection': 'keep-alive',
           'Host': 'www.trademap.org',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36  '}

url = 'https://www.trademap.org/Index.aspx'

cookies = {'AspxAutoDetectCookieSupport': '1', 'ASP.NET_SessionId': 'xbxrcd55v4d5htz5xbrw0gfq', 'trademap.org': '0CA53501F9993FDDF62A5C73AEC20F1855F68B1C77244393B06FAD3EB32D9E3117F526E102BFED7AD3BCFD642DDF12059BDD7963B128F729B6569B1BFB81EF3AAB23B6751A1BEA80FC40D71F9D7B0E43A6CE395843551EEDD83B5A36CEB1DDEA5E63BDFC00A5036D67B04A2CC337E3936BE3C1A7DA81DE230A59759095A0D4F9067421A5'}

res = f_requests('get', url, headers, cookies=cookies)
print(res.status_code)
print(res.text)
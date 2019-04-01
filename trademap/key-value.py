text = """
AspxAutoDetectCookieSupport=1; ASP.NET_SessionId=xbxrcd55v4d5htz5xbrw0gfq; trademap.org=0CA53501F9993FDDF62A5C73AEC20F1855F68B1C77244393B06FAD3EB32D9E3117F526E102BFED7AD3BCFD642DDF12059BDD7963B128F729B6569B1BFB81EF3AAB23B6751A1BEA80FC40D71F9D7B0E43A6CE395843551EEDD83B5A36CEB1DDEA5E63BDFC00A5036D67B04A2CC337E3936BE3C1A7DA81DE230A59759095A0D4F9067421A5     
        """

import re

# Chrome头处理
# info = dict()
# for i, j in re.findall('(.*?):(.*)\\n', text):
#     info[i] = j
#
# print(info)

# Chrome cookie处理

info = dict()
for i in text.split(';'):
    j, k = re.findall('(.*?)=(.*)', i.strip())[0]
    info[j] = k
print(info)
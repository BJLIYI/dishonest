import requests
import re
import js2py

# 生成需要cookie信息
# 1. 获取发送请求session对象, session对象, 会自动处理服务设置过来的cookie信息
session = requests.session()

# 2. 公告信息页面的URL:
url = 'http://www.gsxt.gov.cn/corp-query-entprise-info-xxgg-100000.html'
# 发送GET请求
response = session.get(url)
print(response.status_code)
# print(response.content.decode())
# 使用正则re, script标签中js代码
js = re.findall('<script>(.+?)</script>', response.content.decode())[0]
# print(js)
# 对于加密的js代码中, 一般eval函数的参数, 就是最终要执行的js; 我们要获取最终js怎么办呢?
# 我们不要使用eval来执行这段代码, 而是赋值给一个变量
js = re.sub('\s*eval\s*\(', 'code=(', js)
# print(js)
# 执行修改后的js
# 获取执行js的环境
context = js2py.EvalJs()
context.execute(js)
# 打印执行后code的值
# print(context.code)
# 从真正执行的内容中,提取生成cookie的js代码
cookie_code = re.findall("document.(cookie=.+)\+';Expires", context.code)[0]
print(cookie_code)
# 替换掉document的相关代码
cookie_code = re.sub(r"var (\w+)=document.createElement\('div'\);\w+\.innerHTML='<a href=.+>\w+</a>';\w+=\w+.firstChild.href;", r"var \1='http://www.gsxt.gov.cn';", cookie_code)
print(cookie_code)
# 执行生成cookie信息的js, 生成cookie信息
context.execute(cookie_code)


# 打印cookie信息
print(context.cookie)





print(session.cookies)



# 一个cookie 绑定 User-Agent -> IP
url = 'http://www.gsxt.gov.cn/affiche-query-area-info-paperall.html?noticeType=21&areaid=100000&noticeTitle=&regOrg=210000'
# noticeType=21 公告类型id, 失信企业公告
# areaid=100000 固定10000
# noticeTitle= 公告标题
# regOrg=210000  公告区域
# data = {
#     'start': '20',
#     'length': '10'
# }
#
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
#     # 'User-Agent':"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
#     # 'Cookie': '__jsluid=f9e44db64d48febe3f78d769d02c120b; __jsl_clearance=1546431318.666|0|fnAceLTbQOHQnwMKFmDeZT0GTzI%3D; SECTOKEN=7178421171339920844; JSESSIONID=FCA3BA33B1087FCAE1D09C368FD46E5D-n2:-1; tlb_cookie=S172.16.12.42'
# }
#
# proxies = {
#     'http':'http://119.101.115.40:9999'
# }
#
# response = requests.post(url, data=data, headers=headers)
#
# print(response.status_code)
# print(response.content.decode())


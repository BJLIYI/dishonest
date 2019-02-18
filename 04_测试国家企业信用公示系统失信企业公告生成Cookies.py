import requests
import re
import js2py

index_url = 'http://www.gsxt.gov.cn/corp-query-entprise-info-xxgg-100000.html'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'}

# 获取request的session对象, 可以自动合并cookie信息;
session = requests.session()
session.headers = headers

# 使用session发送请求
response = session.get(index_url)
# print(session.cookies)
# print(response.content.decode())
#



# 1. 提取script标签中的js
js = re.findall('<script>(.+?)</script>', response.content.decode())[0]
# print(js)
# 2. 由于这种加密js, 最终指向的js代码, 都是在eval函数中的, 所以 `{eval(` 替换为 {code=(, 然后就可以通过code, 获取真正要执行的js了
js = js.replace('{eval(', '{code=(')
print(js)
# 3. 获取要执行的js
# 3.1 获取执行js的环境
context = js2py.EvalJs()
context.execute(js)
# 打印code的值
print(context.code)
# 获取生成Cookie的js
cookie_code = re.findall("document.(cookie=.+)\+';Expires", context.code)[0]
# print(cookie_code)
# 在js2py中, 是不能使用 `document`, 'window' 这些浏览器中对象
# var _1k=document.createElement('div');_1k.innerHTML='<a href=\'/\'>_D</a>';_1k=_1k.firstChild.href;
# js2py是无法处理.
# `var _31=document.createElement('div');_31.innerHTML='<a href=\'/\'>_8</a>';_31=_31.firstChild.href`
# 替换为
# _
# cookie_code = re.sub(r"var\s+(\w+)=document.createElement\('\w+'\);\w+.innerHTML='<a href=\\'/\\'>\w+</a>';\w+=\w+.firstChild.href", r"var \1='http://www.gsxt.gov.cn'", cookie_code)
cookie_code = re.sub(r"var\s+(\w+)=document.+?firstChild.href", r"var \1='http://www.gsxt.gov.cn'", cookie_code)
# print(cookie_code)
# 执行js, 生成我们需要cookie信息
context.execute(cookie_code)
# 打印cookie信息
print(context.cookie)
cookies = context.cookie.split('=')
session.cookies.set(cookies[0], cookies[1])
session.get(index_url)

# print(session.cookies)
# 获取cookie字典
cookies = requests.utils.dict_from_cookiejar(session.cookies)
print(cookies)

url = 'http://www.gsxt.gov.cn/affiche-query-area-info-paperall.html?noticeType=21&areaid=100000&noticeTitle=&regOrg=110000'

data = {
    # 'draw': '0',
    'start': '0',
    'length': '10'
}

# 准备请求头
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
#     # 'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
#     # 'Referer': 'http://www.gsxt.gov.cn/corp-query-entprise-info-xxgg-100000.html',
#     # 'Cookie': '__jsluid=fb0718dce34ccf53c4b94d15e9ab13d5; SECTOKEN=7178252594204902863; __jsl_clearance=1546475343.133|0|QZ7AOWMecndqD4CZG4hqoBAHtVw%3D;'
# }
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'}


proxies = {
    'http': 'http://110.52.235.85:9999'
}

response = requests.post(url, cookies=cookies, data=data, headers=headers)
print(response.status_code)
print(response.content.decode())

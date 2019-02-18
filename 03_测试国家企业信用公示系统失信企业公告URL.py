import requests


url = 'http://www.gsxt.gov.cn/affiche-query-area-info-paperall.html?noticeType=21&areaid=100000&noticeTitle=&regOrg=110000'

data = {
    # 'draw': '0',
    'start': '0',
    'length': '10'
}

# 准备请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
    # 'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    # 'Referer': 'http://www.gsxt.gov.cn/corp-query-entprise-info-xxgg-100000.html',
    'Cookie': '__jsluid=d64820f144b22b07b13de4650f9547fe;SECTOKEN=7156985003733944739;__jsl_clearance=1550471875.682|0|iJ65RtWk1bFpCT0sPi5bGIrwofQ%3D; '
}

proxies = {
    'http':'http://110.52.235.85:9999'
}

response =  requests.post(url, data=data, headers=headers)
print(response.status_code)
print(response.content.decode())
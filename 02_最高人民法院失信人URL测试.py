import requests

url = 'http://jszx.court.gov.cn/api/front/getPublishInfoPageList'

# 准备数据
data = {
    "pageSize": 10,
    "pageNo": 2360,
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
}

response = requests.post(url, data=data, headers=headers)

print(response.content.decode())


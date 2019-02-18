from gevent import monkey
monkey.patch_all()
from gevent.pool import Pool

from redis import StrictRedis
import random
import requests
import re
import js2py
import pickle

from dishonest.settings import REDIS_URL, USER_AGENTS
from dishonest.settings import COOKIES_KEY, COOKIES_PROXY_KEY, COOKIES_USER_AGENT_KEY, REDIS_COOKIES_KEY
"""
实现生成cookie的脚本

1. 创建gen_gsxt_cookies.py文件, 在其中创建GenGsxtCookie的类
2. 实现一个方法, 用于把一套代理IP, User-Agent, Cookie绑定在一起的信息放到Redis的list中
    随机获取一个User-Agent
    随机获取一个代理IP
    获取request的session对象
    把User-Agent, 通过请求头, 设置给session对象
    把代理IP, 通过proxies, 设置给session对象
    使用session对象, 发送请求, 获取需要的cookie信息
    把代理IP, User-Agent, Cookie放到字典中, 序列化后, 存储到Redis的list中
3. 实现一个run方法, 用于开启多个异步来执行这个方法.

注: 为了和下载器中间件交互方便, 需要再settings.py中配置一些常量.
"""

class GenGsxtCookie(object):

    def __init__(self):
        """建立Redis数据库连接"""
        self.redis = StrictRedis.from_url(REDIS_URL)
        # 创建协程池对象
        self.pool = Pool()

    def push_cookie_to_redis(self):

        while True:
            try:
                """
                2. 实现一个方法, 用于把一套代理IP, User-Agent, Cookie绑定在一起的信息放到Redis的list中
                """
                # 1. 随机获取一个User-Agent
                user_agent = random.choice(USER_AGENTS)
                # 2. 随机获取一个代理IP
                response = requests.get('http://localhost:16888/random?protocol=http')
                proxy = response.content.decode()
                # 3. 获取requests的session对象
                session = requests.session()
                # 4. 把User-Agent, 通过请求头, 设置给session对象
                session.headers = {
                    'User-Agent': user_agent
                }
                # 5. 把代理IP, 通过proxies, 设置给session对象
                session.proxies = {
                    'http': proxy
                }
                # 6. 使用session对象, 发送请求, 获取需要的cookie信息
                index_url = 'http://www.gsxt.gov.cn/corp-query-entprise-info-xxgg-100000.html'

                # 使用session发送请求
                response = session.get(index_url)
                print(response.status_code)
                # print(response.content.decode())
                # 1. 提取script标签中的js
                js = re.findall('<script>(.+?)</script>', response.content.decode())[0]
                # print(js)
                # 2. 由于这种加密js, 最终指向的js代码, 都是在eval函数中的, 所以 `{eval(` 替换为 {code=(, 然后就可以通过code, 获取真正要执行的js了
                js = js.replace('{eval(', '{code=(')
                # print(js)
                # 3. 获取要执行的js
                # 3.1 获取执行js的环境
                context = js2py.EvalJs()
                context.execute(js)
                # 打印code的值
                # print(context.code)
                # 获取生成Cookie的js
                cookie_code = re.findall("document.(cookie=.+)\+';Expires", context.code)[0]
                # print(cookie_code)
                # 在js2py中, 是不能使用 `document`, 'window' 这些浏览器中对象
                # var _1k=document.createElement('div');_1k.innerHTML='<a href=\'/\'>_D</a>';_1k=_1k.firstChild.href;
                # js2py是无法处理.
                # `var _31=document.createElement('div');_31.innerHTML='<a href=\'/\'>_8</a>';_31=_31.firstChild.href`
                # 替换为
                # _31='http://www.gsxt.gov.cn'
                # cookie_code = re.sub(r"var\s+(\w+)=document.createElement\('\w+'\);\w+.innerHTML='<a href=\\'/\\'>\w+</a>';\w+=\w+.firstChild.href", r"var \1='http://www.gsxt.gov.cn'", cookie_code)
                cookie_code = re.sub(r"var\s+(\w+)=document.+?firstChild.href", r"var \1='http://www.gsxt.gov.cn'", cookie_code)
                # print(cookie_code)
                # 执行js, 生成我们需要cookie信息
                context.execute(cookie_code)
                # 打印cookie信息
                # print(context.cookie)
                cookies = context.cookie.split('=')
                session.cookies.set(cookies[0], cookies[1])
                session.get(index_url)
                # print(session.cookies)
                # 获取cookie字典
                cookies = requests.utils.dict_from_cookiejar(session.cookies)
                # print(cookies)
                # 7. 把代理IP, User-Agent, Cookie放到字典中, 序列化后, 存储到Redis的list中
                cookies_dict = {
                    COOKIES_KEY:cookies,
                    COOKIES_USER_AGENT_KEY:user_agent,
                    COOKIES_PROXY_KEY:proxy
                }
                # 序列化后, 存储到Redis的list中
                self.redis.lpush(REDIS_COOKIES_KEY, pickle.dumps(cookies_dict))
                print(cookies_dict)
                break
            except Exception as ex:
                print(ex)

    def run(self):
        # 清空之前的cookie信息
        self.redis.delete(REDIS_COOKIES_KEY)
        # 3. 实现一个run方法, 用于开启多个异步来执行这个方法.
        for i in range(100):
            self.pool.apply_async(self.push_cookie_to_redis)
        # 让主线程等待所有的, 协程任务完成
        self.pool.join()

if __name__ == '__main__':
    ggc = GenGsxtCookie()
    ggc.run()
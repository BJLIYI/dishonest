FROM python:3.6.5-stretch
COPY pip.conf /root/.config/pip/

RUN pip install ipython

# 安装涉及的python第三方模块
RUN pip install requests &&\
    pip install aiohttp &&\
    pip install tornado &&\
    pip install gevent &&\
    pip install incremental &&\
    pip install twisted[tls] &&\
    pip install eventlet &&\
    pip install dnspython &&\
    pip install celery[redis] &&\
    pip install django==1.11 &&\
    pip install sqlalchemy &&\
    pip install mongoengine &&\
    pip install redis &&\
    pip install six &&\
    pip install pymysql &&\
    pip install psycopg2  &&\
    pip install lxml &&\
    pip install bs4 &&\
    pip install pyquery &&\
    pip install wxpy &&\
    pip install pika &&\
    pip install pycurl &&\
    pip install selenium &&\
    pip install Appium-Python-Client

# 为celery启动设置用户和用户组，当序列化是pickle等类型时，启动celery时，必须指定非root用户运行
RUN groupadd --gid 800 celery \
  && useradd --uid 800 --gid celery --shell /bin/bash --create-home celery

# 安装confluent-kafka
#RUN apt-get install git   # 如果没有git，需要先安装
RUN git clone https://github.com/edenhill/librdkafka.git &&\
    cd librdkafka &&\
    ./configure &&\
    make &&\
    make install &&\
    pip install confluent-kafka

# 安装scrapy，scrapy-redis, jsonpath,
RUN set -ex &&\
    pip install scrapy && pip install scrapy-redis && pip install jsonpath &&\
    pip install scrapy_fake_useragent && pip install fake-useragent

# 执行js
RUN set -ex &&\
    pip install js2py
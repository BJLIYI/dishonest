# -*- coding: utf-8 -*-
import scrapy
import json
from datetime import datetime

from dishonest.items import DishonestItem

"""
- 4.3. 完善爬虫
  - 构建起始URL
  - 获取总页数, 构建所有页面请求
  - 解析页面数据
"""

class CourtSpider(scrapy.Spider):
    name = 'court'
    allowed_domains = ['court.gov.cn']
    # start_urls = ['http://court.gov.cn/']
    post_url = 'http://jszx.court.gov.cn/api/front/getPublishInfoPageList'

    # 构建起始请求
    def start_requests(self):
        data  = {
         "pageSize": "10",
         "pageNo": "1",
        }
        # 构建POST请求, 交个引擎
        yield scrapy.FormRequest(self.post_url, formdata=data, callback=self.parse)

    def parse(self, response):
        # 把响应的json字符串, 转换为字典
        results = json.loads(response.text)
        # 解析第一页数据, 获取总页数
        page_count = results['pageCount']
        # 构建每一个的请求
        for page_no in range(page_count):
            data = {
                "pageSize": "10",
                "pageNo": str(page_no),
            }
            yield scrapy.FormRequest(self.post_url, formdata=data, callback=self.parse_data)


    def parse_data(self, response):
        """解析数据"""
        results = json.loads(response.text)
        # 获取失信人信息列表
        datas = results['data']
        # 遍历数据
        for data in datas:
            item = DishonestItem()
            # 失信人名称
            item['name'] = data['name']
            # 失信人号码
            item['card_num'] = data['cardNum']
            # 失信人年龄
            item['age'] = data['age']
            # 区域
            item['area'] = data['areaName']
            # 法人(企业)
            item['business_entity'] = data['buesinessEntity']
            # 失信内容
            item['content'] = data['duty']
            # 公布日期
            item['publish_date'] = data['publishDate']
            # 公布 /执行单位
            item['publish_unit'] = data['courtName']
            # 创建日期
            item['create_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # 更新日期
            item['update_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # print(item)
            yield item
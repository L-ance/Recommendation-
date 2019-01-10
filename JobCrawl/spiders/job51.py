# -*- coding: utf-8 -*-
from urllib import parse  # 如果url不是完整的就加上这个,用来对query 进行格式的转化

import scrapy
from scrapy.http import Request

from JobCrawl.utils.parse_detail import parse_detail_utils


class Job51Spider(scrapy.Spider):
    name = 'job51'

    def __init__(self, keywords='python', *args, **kwargs):
        super(Job51Spider, self).__init__(*args, **kwargs)
        self.keywords = keywords
        # self.allowed_domains = ['jobs.51job.com', 'search.51job.com']
        # allowed_domains 没有必要存在,会限制爬取的网站
        self.start_urls = ['https://search.51job.com/list/000000%%252C00,000000,0000,00,9,99,%s,2,1.html/' % keywords]
    """
    start_urls = ['https://search.51job.com/list/000000%%252C00,000000,0000,00,9,99,%s,2,1.html/' % keywords]
    keyword = "python"
    """
    def parse(self, response):
        # 1获取到每一条招聘的url并将url给具体的解析函数进行解析字段
        url_list = response.xpath('//*[@id="resultList"]//div/p/span/a/@href').extract()
        for url in url_list:
            yield Request(url=parse.urljoin(response.url, url), callback=self.parse_detail, )

        # 2获取下一页的url并交给scrapy下载
        next_url = response.xpath('//*[@id="resultList"]/div[55]/div/div/div/ul/li[8]/a/@href').extract_first("")
        if next_url:
            # yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse)
            yield Request(url=next_url, callback=self.parse)
    #         在scrapy框架中,全部都需要用yield提交数据

    def parse_detail(self, response):
        yield parse_detail_utils(self, response, self.keywords)

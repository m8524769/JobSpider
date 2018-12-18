# -*- coding: utf-8 -*-
import scrapy
import re
import time


class RelatedSpider(scrapy.Spider):
    name = 'related'
    base_url = 'www.zhipin.com'
    allowed_domains = [base_url]
    start_urls = ['https://www.zhipin.com/c100010000']

    def parse(self, response):
        for job in response.css('div.job-primary'):
            if self.start > 0:
                self.start -= 1
                break
            if self.limit == 0:
                break

            link = job.xpath('.//a/@href').extract_first()
            yield response.follow(link, self.parse_detail)
            time.sleep(10)

        next_page = response.css('a.next::attr("href")').extract_first()
        if next_page is not None and self.limit > 0:
            yield response.follow(next_page, self.parse)

    def parse_detail(self, response):
        description = response.css('div.text::text').extract()[:-1]
        if 'linux' in description:
            yield {
                '职位': response.css('div.name > h1::text').extract_first(),
                '薪资': re.sub(r'\s+', '', response.css('span.badge::text').extract_first()),
                '公司名称': response.css('div.info-company > h3 > a::text').extract_first(),
                '要求': response.css('div.info-primary > p::text').extract()[:3],
                '发布时间': response.css('span.time::text').extract_first(),
                'url': response.url,
                '职位描述': description,
                '公司介绍': response.css('div.text::text').extract()[-1],
            }
            self.limit -= 1

    def __init__(self, start=0, limit=10):
        self.start = int(start)
        self.limit = int(limit)

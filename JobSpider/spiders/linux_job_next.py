# -*- coding: utf-8 -*-
import scrapy
import re

class LinuxJobNextSpider(scrapy.Spider):
    name = 'linux_job_next'
    base_url = 'www.zhipin.com'
    allowed_domains = [base_url]
    start_urls = ['https://www.zhipin.com/c100010000/?query=linux']

    def parse(self, response):
        for job in response.css('div.job-primary'):
            if self.count == 0:
                break

            link = job.xpath('.//a/@href').extract_first()
            yield response.follow(link, self.parse_detail)
            self.count -= 1

        next_page = response.css('a.next::attr("href")').extract_first()
        if next_page is not None and self.count > 0:
            yield response.follow(next_page, self.parse)

    def parse_detail(self, response):
        yield {
            '职位': response.css('div.name > h1::text').extract_first(),
            '薪资': re.sub(r'\s+', '', response.css('span.badge::text').extract_first()),
            '公司名称': response.css('div.info-company > h3 > a::text').extract_first(),
            '要求': response.css('div.info-primary > p::text').extract()[:3],
            '发布时间': response.css('span.time::text').extract_first(),
            'url': response.url,
            '公司网址': response.css('div.info-company > p::text').extract()[-1],
            '职位描述': response.css('div.text::text').extract()[:-1],
            '公司介绍': response.css('div.text::text').extract()[-1],
        }

    def __init__(self, count=1):
        self.count = int(count)

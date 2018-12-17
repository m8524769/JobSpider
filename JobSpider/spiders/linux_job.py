# -*- coding: utf-8 -*-
import scrapy
import json

class LinuxJobSpider(scrapy.Spider):
    name = 'linux_job'
    base_url = 'www.zhipin.com'
    allowed_domains = [base_url]
    start_urls = ['https://www.zhipin.com/c100010000/?query=linux']

    def parse(self, response):
        for job in response.css('div.job-primary'):
            if self.limit == 0:
                break

            if self.more == True:
                title = job.css('div.info-primary > h3')
                jid = title.css('a::attr("data-jid")').extract_first()
                lid = title.css('a::attr("data-lid")').extract_first()
                yield scrapy.FormRequest(
                    url='https://www.zhipin.com/view/job/card.json',
                    formdata={'jid': jid, 'lid': lid},
                    callback=self.parse_detail,
                )

            requirements = job.css('div.info-primary > p::text').extract()
            yield {
                '职位': job.css('div.job-title::text').extract_first(),
                '薪资': job.css('span.red::text').extract_first(),
                '公司名称': job.css('div.company-text > h3 > a::text').extract_first(),
                '工作地点': requirements[0],
                '工作经验': requirements[1],
                '学历要求': requirements[2],
                '发布时间': job.css('div.info-publis > p::text').extract_first(),
                'url': self.base_url + job.css('div.info-primary > h3 > a::attr("href")').extract_first(),
            }

            self.limit -= 1

        next_page = response.css('a.next::attr("href")').extract_first()
        if next_page is not None and self.limit > 0:
            yield response.follow(next_page, self.parse)

    def parse_detail(self, response):
        jsonResponse = json.loads(response.body)
        htmlResponse = scrapy.http.HtmlResponse(
            url=response.url,
            body=jsonResponse['html'],
            encoding='utf-8'
        )
        detail = htmlResponse.css('div.detail-bottom-text::text').extract()
        yield {
            '职责描述': detail
        }

    def __init__(self, limit=10, more=False):
        self.limit = int(limit)
        if more in ['True', 'true']:
            self.more = True
        else:
            self.more = False

# -*- coding: utf-8 -*-
import scrapy


class ProxySpider(scrapy.Spider):
    name = 'proxy'
    base_url = 'www.xicidaili.com'
    allowed_domains = [base_url]
    start_urls = ['https://www.xicidaili.com/wt/']

    def parse(self, response):
        for proxy in response.xpath('//table[@id="ip_list"]/tr')[2:]:
            if self.count == 0:
                break

            ip = proxy.xpath('.//td/text()').extract()[0]
            port = proxy.xpath('.//td/text()').extract()[1]

            yield {
                'proxy': 'http://{}:{}'.format(ip, port)
            }
            self.count -= 1

        next_page = response.css('a.next_page::attr("href")').extract_first()
        if next_page is not None and self.count > 0:
            yield response.follow(next_page, self.parse)

    def __init__(self, count=10):
        self.count = int(count)

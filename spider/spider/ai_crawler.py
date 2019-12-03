# -*- coding: utf-8 -*-

import json
import scrapy
from scrapy.crawler import CrawlerProcess
from spider.items import SpiderItem

class ai_spider(scrapy.Spider):
    name = 'aispyder'
    allowed_domains = ['aitopics.org']
    start_urls = ['https://aitopics.org/search']
    doc_id = 0
    dict_page = {}
    counter = 0
    goal = 10000

    def parse(self,response):
        item = SpiderItem()
        if self.counter < self.goal:
            print(self.counter)
            self.counter += 1
            # h1, h2, h3, h4, h5, h6, li, a, span
            title = response.xpath("//h1/text()").extract()
            p = response.xpath('//p/text()').extract()
            span = response.xpath('//span/text()').extract()
            li = response.xpath('//li/text()').extract()
            a = response.xpath('//a/text()').extract()
            # h1 = response.xpath('//h1/text()').extract()
            h2 = response.xpath('//h2/text()').extract()
            h3 = response.xpath('//h3/text()').extract()
            h4 = response.xpath('//h4/text()').extract()
            h5 = response.xpath('//h5/text()').extract()
            h6 = response.xpath('//h6/text()').extract()
            text = str(p).strip() + str(span).strip() + str(a).strip()\
                    + str(h2).strip() + str(h3).strip()\
                   + str(h4).strip() + str(h5).strip() + str(h6).strip() \
                   + str(li) + str(title)
            text = text.replace('\\r', '').replace('\\n', '').replace('\\t', '')
            if str(response.url) not in self.dict_page.keys():
                self.doc_id += 1
                self.dict_page[str(response.url)] = [[self.doc_id], [text]]
            item['text'] = text
            item['title'] = title
        else:
            print("Writing dictionary into file. " + "Dictionary size: " + str(len(self.dict_page)))
            with open("/Users/lekangdu/Desktop/my_spider/spider/res/ai_res" + str(self.goal) + ".json",'w') as f:
                json.dump(self.dict_page,f)
            self.crawler.engine.close_spider(self, 'Spider closed.')

        links = response.xpath('.//a/@href').extract()
        for url in links:
            if url.endswith('.html'):
                next_url = response.urljoin(url)
                yield scrapy.Request(next_url, callback=self.parse)


if __name__ == "__main__":
    run_scrapy = CrawlerProcess()
    run_scrapy.crawl(ai_spider)
    run_scrapy.start()
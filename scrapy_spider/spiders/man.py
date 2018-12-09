# -*- coding: utf-8 -*-
import scrapy
from scrapy_spider.items import ManItem
from scrapy.http import Request

class ManSpider(scrapy.Spider):
    name = 'man'
    allowed_domains = ['91jinwandalaohu.rocks']
    start_urls = ['http://5.91jinwandalaohu.rocks/pw/thread-htm-fid-3-page-1.html']
                 ['http://5.91jinwandalaohu.rocks/pw/thread-htm-fid-3-page-1.html']

    # interests = ['国产','國產']
    interests = ['大放送']
    outfile = './test.html'

    # 把网页URL转化为接口URL
    def start_requests(self):
        for i in range(207):
            origin_url = 'http://5.91jinwandalaohu.rocks/pw/thread-htm-fid-3-page-{}.html'.format(i+1)
            print("page", i)
            yield Request(origin_url, callback=self.parse)

    def parse(self, response):
        self.lines = []
        self.update_url(response)
        self.handle_interest(response)
        # self.write_file()
        pass
    
    def write_file(self, line):
        f = open(self.outfile, 'a')
        f.write(line)
        f.close()
    
    def expect(self, ctx):
        for instrs in self.interests:
            if instrs in ctx:
                return True
        return False
    
    def handle_interest(self, response):
        items = response.xpath('//h3')
        for h3 in items:
            try:
                url = h3.xpath('./a/@href').extract()[0]
                # print(url)
                ctx = h3.xpath('./a/text()').extract()[0]
                # print(ctx)
            except Exception as e:
                # print(e)
                continue

            try:
                item = h3.xpath('../..')
                # print(item.xpath('./@class').extract()[0])
                ts = item.xpath('./td/a[@class="f10"]/text()').extract()[0]
                # ts = item.xpath('./td/a[@class="f10"]/text()').extract()[0]
                # print(ts)
            except Exception as e:
                print (e)
                ts = 1
            
            if not self.expect(ctx):
                # pass
                continue
            url = self.url_prefix + url
            line = '<div><a href="{}">{}</a><span>{}</span></div>\n'.format(url, ctx, ts)
            self.write_file(line)
            # print(line)
        # items = response.xpath('//tr[@class="tr3 t_one"]')
        # for item in items:
        #     h3 = item.xpath('./td/h3')
        #     try:
        #         url = h3.xpath('./a/@href').extract()[0]
        #         # print(url)
        #         ctx = h3.xpath('./a/text()').extract()[0]
        #         # print(ctx)
        #         ts = item.xpath('./td/a[@class="f10"]/text()').extract()[0]
        #         # print(ts)
        #     except Exception as e:
        #         # print(e)
        #         continue
            
        #     # if not self.expect(ctx):
        #     #     continue
                    
        #     url = self.url_prefix + url
        #     line = '<div><a href="{}">{}</a><span>{}</span></div>\n'.format(url, ctx, ts)
        #     # self.lines.append(line, ctx)
        #     self.write_file(line)
        #     print(line)
            
            # print(ctx, url, ts)
            #title = 

        # pages = response.xpath('//div[@class="main-wrap"]').xpath('./tr[@class="tr3 t_one"]/text()').extract()
        # print(pages)

        # pages = response.xpath('//h3')
        # for page in pages:
        #     cc = page.xpath('./a/@id').extract()
        #     print (page.xpath('./a/text()').extract())
        #     # print(cc)
        # pass

    
    def update_url(self, response):
        return
        pages = response.xpath('//div[@class="pages cc"]')
        pages = pages[0].xpath('./a')
        print(pages.xpath('./text()').extract())
        for page in pages:
            url = page.xpath('./@href').extract()[0]
            ctx = page.xpath('./text()').extract()[0]
            print(url, ctx)


#   _*_ coding:utf-8 _*_

import scrapy

from spidermeizi.items import SpidermeiziItem


class MeiziSpider(scrapy.Spider):
    name = "meizi"
    host = "http://www.mzitu.com/"
    start_urls = [
        "http://www.mzitu.com/"
    ]

    def parse(self, response):
        urls = response.xpath('//div[@class="postlist"]/ul/li/a/@href').extract()
        print("urls", urls)
        for url in urls:
            send = url + "/2"
            yield scrapy.Request(send, callback=self.parse_item)

    def parse_item(self, response):
        item = SpidermeiziItem()
        imgurl = response.xpath('//div[@class="main-image"]/p/a/img/@src').extract()[0]
        name = response.xpath('//div[@class="main-image"]/p/a/img/@alt').extract()[0]
        total = int(response.xpath('//div[@class="pagenavi"]/a/span/text()').extract()[-2])
        baseimg = imgurl[0:-6]
        urllist = []
        for i in range(1, total):
            urllist.append(baseimg + ("%02d" % i) + ".jpg")
        item["imgurls"] = urllist
        item["name"] = name
        yield item

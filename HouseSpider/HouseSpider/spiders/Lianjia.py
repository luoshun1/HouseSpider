# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from HouseSpider.items import LianJiaItem

import math
import urllib


class LianjiaSpider(CrawlSpider):
    name = 'Lianjia'
    allowed_domains = ['lianjia.com', ]
    start_urls = ['http://www.lianjia.com/city/']

    rules = (
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'//[a-z]{2,5}\.lianjia\.com/?$'), follow=True),

        Rule(LinkExtractor(allow=r'//[a-z]{2,5}\.lianjia\.com/ershoufang/?$'), follow=True),
        Rule(LinkExtractor(allow=r'//[a-z]{2,5}\.lianjia\.com/ershoufang/pg\d+$'), follow=True),
        Rule(LinkExtractor(allow=r'//[a-z]{2,5}\.lianjia\.com/ershoufang/\d+\.html'), callback='parse_ershoufang'),

        Rule(LinkExtractor(allow=r'//[a-z]{2,5}\.lianjia\.com/zufang/?$'), follow=True),
        Rule(LinkExtractor(allow=r'//[a-z]{2,5}\.lianjia\.com/zufang/pg\d+/'), follow=True),
        Rule(LinkExtractor(allow=r'//[a-z]{2,5}\.lianjia\.com/zufang/\w+\.html'), callback='parse_zufang'),

        Rule(LinkExtractor(allow=r'//[a-z]{2,5}\.fang\.lianjia\.com/?$'), follow=True),
        Rule(LinkExtractor(allow=r'//[a-z]{2,5}\.fang\.lianjia\.com/loupan/?$'), callback='parse_xinfang_page'),
        Rule(LinkExtractor(allow=r'//[a-z]{2,5}\.fang\.lianjia\.com/loupan/pg\d+'), follow=True),
        Rule(LinkExtractor(allow=r'//[a-z]{2,5}\.fang\.lianjia\.com/loupan/p_\w+'), callback='parse_xinfang'),
        # Rule(LinkExtractor(allow=r'//[a-z]{2,5}\.fang\.lianjia\.com/loupan/p_\w+/xiangqing/?$'), callback=''), # 待优化
    )

    def parse_item(self, response):
        print('-' * 100)
        item = {}
        self.write_file(response.text)
        self.write_file('=' * 100)

        return item

    def parse_ershoufang(self, response):
        item = LianJiaItem()
        item['houseType'] = 'ershoufang'
        item['houseUrl'] = response.request.url
        item['houseTitle'] = response.xpath('//title/text()').extract_first()
        item['houseCity'] = self.check_empty(response.xpath('//script').re(r'cityName:\'(.*?)\','))
        # item['houseCityURL'] = response.xpath('//div[@class="intro clear"]/div/div/a[2]/@href').extract_first()
        item['houseName'] = self.check_empty(response.xpath('//script').re(r'resblockName:\'(.*?)\','))
        # item['housePublishedTime'] = response.xpath('//div[@class="transaction"]/ul/li[1]/span[2]/text()').extract_first()
        item['housePublishedTime'] = self.check_empty(response.xpath('//script').re(r'"pubDate": "(.*?)",'))
        item['housePrice'] = self.check_empty(response.xpath('//script').re(r'totalPrice:\'([0-9\.]+)\','))
        item['housePrice'] = int(float(item['housePrice']) * 10000) if item['housePrice'] else None
        item['houseArea'] = self.check_empty(response.xpath('//script').re(r'area:\'([0-9\.]+)\','))
        item['houseArea'] = float(item['houseArea']) if item['houseArea'] else None
        item['houseBaiduLongitude'] = self.check_empty(response.xpath('//script').re(r'resblockPosition:\'(.*?),.*?\','))
        item['houseBaiduLatitude'] = self.check_empty(response.xpath('//script').re(r'resblockPosition:\'.*?,(.*?)\','))

        return item

    def parse_zufang(self, response):
        item = LianJiaItem()
        item['houseType'] = 'zufang'
        item['houseUrl'] = response.request.url
        item['houseTitle'] = response.xpath('/html/head/title/text()').extract_first()
        item['houseCity'] = response.xpath('/html/head/meta[@name="location"]/@content').extract_first()
        item['houseCity'] = item['houseCity'].split('=')[-1] if item['houseCity'] else None
        item['houseName'] = self.check_empty(response.xpath('//script').re('g_conf\.name = \'(.*?)\';'))
        item['housePrice'] = self.check_empty(response.xpath('//script').re('g_conf\.rent_price = \'(\d+)\';'))
        item['housePrice'] = int(item['housePrice']) if item['housePrice'] else None
        item['houseArea'] = self.check_empty(response.xpath('//div[@id="info"]/ul[1]/li[2]/text()').re(r'\d+'))
        item['houseBaiduLongitude'] = self.check_empty(response.xpath('//script').re('longitude: \'([\d\.]+)\','))
        item['houseBaiduLatitude'] = self.check_empty(response.xpath('//script').re('latitude: \'([\d\.]+)\''))

        return item

    def parse_xinfang_page(self, response):
        total_page = response.xpath('//div[@class="page-box"]/@data-total-count').extract_first()
        total_page = math.ceil(int(total_page)) if total_page else None
        if total_page:
            for i in range(total_page):
                url = urllib.parse.urljoin(response.request.url, 'pg' + str(i))

                yield scrapy.Request(
                    url,
                    callback=self.parse,
                )

    def parse_xinfang(self, response):
        item = LianJiaItem()
        item['houseType'] = 'xinfang'
        item['houseUrl'] = response.request.url
        item['houseTitle'] = response.xpath('/html/head/title/text()').extract_first()
        item['houseCity'] = response.xpath('//a[@class="s-city"]/text()').extract_first()
        item['houseName'] = response.xpath('//div[@class="title-wrap"]/div/h2[@class="DATA-PROJECT-NAME"]/text()').extract_first()
        item['housePublishedTime'] = response.xpath('//div[@class="open-date"]/span[@class="content"]/text()').extract_first()
        item['housePrice'] = response.xpath('//div[@class="price"]/span[4]/text()').extract_first()
        item['houseUnitPrice'] = response.xpath('//div[@class="price"]/span[2]/text()').extract_first()
        coord = response.xpath('//div[@class="album "]/span[@class="btn-s hide"]/@data-coord').extract_first()
        item['houseBaiduLongitude'] = float(coord.split(',')[0]) if coord else None
        item['houseBaiduLatitude'] = float(coord.split(',')[1]) if coord else None

        return item

    def write_file(self, text):
        with open('log/test.txt', 'a', encoding="utf-8") as f:
            f.write(text)

    def check_empty(self, target_list):
        target_list = target_list[0] if len(target_list) > 0 else None
        return target_list

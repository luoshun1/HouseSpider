# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HousespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class LianJiaItem(scrapy.Item):
    houseTitle = scrapy.Field() # 房屋标题
    houseCity = scrapy.Field() # 房屋所在城市
    # houseCityURL = scrapy.Field() # 城市url
    houseName = scrapy.Field() # 小区名
    houseUrl = scrapy.Field() # 房屋url
    houseType = scrapy.Field() # 新房/二手房/租房
    housePublishedTime = scrapy.Field() # 挂牌时间
    housePrice = scrapy.Field() # 房屋价格
    # houseHistoryPrice = scrapy.Field() # 房屋价格历史
    houseArea = scrapy.Field() # 房屋面积
    # houseAddress = scrapy.Field()
    # houseDistrict = scrapy.Field()
    houseBaiduLongitude = scrapy.Field() # 经度
    houseBaiduLatitude = scrapy.Field() # 纬度

    houseUnitPrice = scrapy.Field() # 新房单价


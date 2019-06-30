# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    super_father = scrapy.Field()
    grandfather = scrapy.Field()
    father = scrapy.Field()
    title = scrapy.Field()
    sum_rating = scrapy.Field()
    avg_rating = scrapy.Field()
    ratings = scrapy.Field()
    price = scrapy.Field()

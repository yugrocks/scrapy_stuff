# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BlogscrapperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ProfileItem(scrapy.Item):
    heading = scrapy.Field(serializer=str)
    description = scrapy.Field(serializer=str)
    replies = scrapy.Field(serializer=str)


class PostItem(scrapy.Item):
    heading = scrapy.Field(serializer=str)
    description = scrapy.Field(serializer=str)
    replies = scrapy.Field(serializer=str)



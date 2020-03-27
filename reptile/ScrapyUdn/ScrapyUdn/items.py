# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyudnItem(scrapy.Item):
    title=scrapy.Field()
    link=scrapy.Field()
    report=scrapy.Field()
    content=scrapy.Field()
    time=scrapy.Field()
    # name = scrapy.Field()

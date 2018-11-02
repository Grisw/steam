# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GameItem(scrapy.Item):
    name = scrapy.Field()
    total_reviews = scrapy.Field()
    reviews_percent = scrapy.Field()
    price = scrapy.Field()
    id = scrapy.Field()


class TagItem(scrapy.Item):
    name = scrapy.Field()
    id = scrapy.Field()


class GameTagItem(scrapy.Item):
    game_id = scrapy.Field()
    tag_ids = scrapy.Field()

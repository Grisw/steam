# -*- coding: utf-8 -*-
import scrapy

from steam.items import TagItem


class TagSpider(scrapy.Spider):
    name = 'tag'
    allowed_domains = ['steampowered.com']
    start_urls = ['https://store.steampowered.com/tag/browse']

    def parse(self, response):
        tags = response.xpath('//*[@id="tag_browse_global"]/div')
        for tag in tags:
            t = TagItem()
            t['id'] = tag.xpath('./@data-tagid').extract_first()
            t['name'] = tag.xpath('./text()').extract_first()
            yield t

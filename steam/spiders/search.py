# -*- coding: utf-8 -*-
import scrapy

from steam.items import GameItem, GameTagItem
import re
import pymysql


class SearchSpider(scrapy.Spider):
    name = 'search'
    allowed_domains = ['steampowered.com']
    start_urls = ['https://store.steampowered.com/tag/browse']

    crawled_appids = [False] * 1000000

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db = pymysql.connect("localhost", "root", "lxt514335188", "steam")
        cur = db.cursor()
        try:
            cur.execute("select id from games")
            results = cur.fetchall()
            for row in results:
                id = row[0]
                self.crawled_appids[id] = True
        finally:
            db.close()

    def parse(self, response):
        tags = response.xpath('//*[@id="tag_browse_global"]/div')

        for tag in tags:
            id = tag.xpath('./@data-tagid').extract_first()
            name = tag.xpath('./text()').extract_first()
            yield scrapy.Request(
                f'https://store.steampowered.com/search/?term={name}&category1=998&page=1',
                meta={
                    'item': {
                        'tag': name,
                        'tag_id': id,
                        'p': 1
                    }
                },
                callback=self.parse_search_page
            )

    def parse_search_page(self, response):
        items = response.xpath('//a[@class="search_result_row ds_collapse_flag "]')
        if items and len(items) > 0:
            yield scrapy.Request(
                f'https://store.steampowered.com/search/?term={response.meta["item"]["tag"]}&category1=998&page={response.meta["item"]["p"] + 1}',
                meta={
                    'item': {
                        'tag': response.meta["item"]["tag"],
                        'tag_id': response.meta["item"]["tag_id"],
                        'p': response.meta["item"]["p"] + 1
                    }
                },
                callback=self.parse_search_page
            )

        for item in items:
            try:
                appid = int(item.xpath('./@data-ds-appid').extract_first())
            except ValueError:
                continue
            if self.crawled_appids[appid]:
                continue
            else:
                self.crawled_appids[appid] = True

            tags = []
            matches = re.finditer('(\d+)[,\]]', item.xpath('./@data-ds-tagids').extract_first())
            for match in matches:
                tags.append(match.group(1))

            url = item.xpath('./@href').extract_first()
            yield scrapy.Request(
                url,
                meta={
                    'item': {
                        'tagids': tags
                    }
                },
                cookies={
                    "birthtime": "-31564799",
                    "lastagecheckage": "1-January-1969"
                },
                callback=self.parse_item
            )

    def parse_item(self, response):
        item = GameItem()
        item['id'] = response.xpath('//*[@id="review_appid"]/@value').extract_first()
        if item['id'] is None:
            return
        item['name'] = response.xpath('//div[@class="apphub_AppName"]/text()').extract_first()
        user_reviews = response.xpath('//div[@itemprop="aggregateRating"]/@data-tooltip-text').extract_first()
        matches = re.search(r'(\d+)% of the ([\d,]+) user', user_reviews)
        if matches is None:
            item['total_reviews'] = '0'
            item['reviews_percent'] = '0'
        else:
            item['total_reviews'] = matches.group(2)
            item['reviews_percent'] = matches.group(1)
        item['price'] = response.xpath('//div[@class="game_purchase_price price"]/text()').extract_first()
        if item['price'] is None:
            item['price'] = response.xpath('//div[@class="discount_original_price"]/text()').extract_first()
            if item['price'] is None:
                item['price'] = '0'
        yield item

        gt = GameTagItem()
        gt['game_id'] = item['id']
        gt['tag_ids'] = response.meta['item']['tagids']
        yield gt

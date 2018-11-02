# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
import re


class SteamPipeline(object):
    def process_item(self, item, spider):
        if 'price' in item:
            matches = re.search(r'¥ ([\d,.]+)', item['price'])
            item['price'] = '0' if matches is None else matches.group(1).replace(',', '')
            item['total_reviews'] = item['total_reviews'].replace(',', '')
        return item


class MySQLPipeline(object):

    def __init__(self):
        self.db = pymysql.connect("localhost", "root", "lxt514335188", "steam")
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):
        try:
            if 'price' in item:
                self.cursor.execute(
                    f"insert into games (name, total_reviews, reviews_percent, price, id) values ('{item['name']}', {item['total_reviews']}, {item['reviews_percent']}, {item['price']}, {item['id']})")
            else:
                for tag in item['tag_ids']:
                    try:
                        self.cursor.execute(f"insert into game_tags (game_id, tag_id) values ('{item['game_id']}', {tag})")
                    except:
                        pass
            self.db.commit()
        except:
            self.db.rollback()
        return item

    def __del__(self):
        self.db.close()

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FansItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    tags = scrapy.Field()
    tag_title = scrapy.Field()
    request_id = scrapy.Field()
    del_url = scrapy.Field()
    next_url = scrapy.Field()
    subtitle = scrapy.Field()
    cover = scrapy.Field()
    created_at = scrapy.Field()
    links = scrapy.Field()

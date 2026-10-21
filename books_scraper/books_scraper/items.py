# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass
import scrapy

class BookItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    category = scrapy.Field()
    rating = scrapy.Field()
    availability = scrapy.Field()
    book_id = scrapy.Field()
    url = scrapy.Field()
    downloads = scrapy.Field()

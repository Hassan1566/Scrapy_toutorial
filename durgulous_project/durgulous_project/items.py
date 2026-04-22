# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DrugItem(scrapy.Item):
    category = scrapy.Field()
    subcategory1 = scrapy.Field()
    subcategory2 = scrapy.Field()
    product_name = scrapy.Field()
    brand = scrapy.Field()
    old_price = scrapy.Field()
    price = scrapy.Field()
    image_url = scrapy.Field()
    product_url = scrapy.Field()
    id_invima = scrapy.Field()
    presentation = scrapy.Field()

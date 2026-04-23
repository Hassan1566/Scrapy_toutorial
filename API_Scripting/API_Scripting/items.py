# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FarmaciaItem(scrapy.Item):
    SKU = scrapy.Field()
    Item = scrapy.Field()
    Brand = scrapy.Field()
    Price = scrapy.Field()
    SalePrice = scrapy.Field()
    Image = scrapy.Field()
    Stock = scrapy.Field()
    Category = scrapy.Field()
    SubCategory1 = scrapy.Field()
    SubCategory2 = scrapy.Field()

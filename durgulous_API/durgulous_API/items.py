# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ProductItem(scrapy.Item):
    # Basic Info
    name = scrapy.Field()
    brand = scrapy.Field()
    product_id = scrapy.Field()
    sku = scrapy.Field()

    # Category
    category = scrapy.Field()
    subcat1 = scrapy.Field()
    subcat2 = scrapy.Field()
    subcat3 = scrapy.Field()
    subcat4 = scrapy.Field()

    # URL
    url = scrapy.Field()
    
    # Pricing
    list_price = scrapy.Field()
    discounted_price = scrapy.Field()
    
    # Specs & Stock
    stock = scrapy.Field()
    invima = scrapy.Field()
    pum = scrapy.Field()
    presentacion = scrapy.Field()
    
    # Image
    image_url = scrapy.Field()
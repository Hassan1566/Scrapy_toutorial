import scrapy


class PhilconItem(scrapy.Item):
    category = scrapy.Field()
    subcategory1 = scrapy.Field()
    subcategory2 = scrapy.Field()
    product_name = scrapy.Field()
    product_sku = scrapy.Field()
    product_description = scrapy.Field()
    image_url = scrapy.Field()
    product_url = scrapy.Field()


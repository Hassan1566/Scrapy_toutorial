from chocolatescrapper.items import ChocolatesProduct
from chocolatescrapper.itemloades import ChocolateItemLoader
import scrapy


class ChocolatespySpider(scrapy.Spider):
    name = "chocolatespy"
    allowed_domains = ["chocolate.co.uk"]
    start_urls = ["https://www.chocolate.co.uk/collections/all"]

    def parse(self, response):
        products = response.xpath("//product-item")

        
        for product in products:
            chocolate = ChocolateItemLoader(item=ChocolatesProduct(), selector=product)
            chocolate.add_xpath('name' , './/a[contains(@class, "product-item-meta__title")]/text()')
            chocolate.add_xpath('price' , './/span[contains(@class, "price")]/text()')
            chocolate.add_xpath('url' , './/div[contains(@class, "product-item-meta")]//a/@href')
            yield chocolate.load_item()   
        
        next_page = response.xpath('//link[@rel="next"]/@href').get()
        if next_page is not None:
            next_page_url = "https://www.chocolate.co.uk" + next_page
            yield response.follow(next_page_url, callback=self.parse)

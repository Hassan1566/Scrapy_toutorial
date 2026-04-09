from chocolatescrapper.items import ChocolatesProduct

import scrapy


class ChocolatespySpider(scrapy.Spider):
    name = "chocolatespy"
    allowed_domains = ["chocolate.co.uk"]
    start_urls = ["https://www.chocolate.co.uk/collections/all"]

    def parse(self, response):
        products = response.xpath("//product-item")
        for product in products:
            name = product.xpath('.//a[contains(@class, "product-item-meta__title")]/text()').get()
            prices = product.xpath('.//span[contains(@class, "price")]/text()').getall()
            prices = [p.strip() for p in prices if p.strip()]
            price = prices[0] if prices else None
            
            url = product.xpath('.//div[contains(@class, "product-item-meta")]//a/@href').get()
            url = response.urljoin(url).strip()

            yield {
                'name': name,
                'price': price,
                'url': url
            }   
        
        next_page = response.xpath('//link[@rel="next"]/@href').get()
        if next_page is not None:
            next_page_url = "https://www.chocolate.co.uk" + next_page
            yield response.follow(next_page_url, callback=self.parse)

import scrapy


class ChocolatespySpider(scrapy.Spider):
    name = "chocolatespy"
    allowed_domains = ["chocolate.co.uk"]
    start_urls = ["https://www.chocolate.co.uk/collections/all"]

    def parse(self, response):
        pass

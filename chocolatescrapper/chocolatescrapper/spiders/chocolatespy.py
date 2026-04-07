import scrapy


class ChocolatespySpider(scrapy.Spider):
    name = "chocolatespy"
    allowed_domains = ["chocolate.co.uk"]
    start_urls = ["https://chocolate.co.uk"]

    def parse(self, response):
        pass

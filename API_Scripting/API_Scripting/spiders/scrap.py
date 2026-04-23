import scrapy


class ScrapSpider(scrapy.Spider):
    name = "scrap"
    allowed_domains = ["farmaciatepa.com.mx"]
    start_urls = ["https://farmaciatepa.com.mx/#/"]

    def parse(self, response):
        pass

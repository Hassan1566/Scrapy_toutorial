import scrapy


class WebspySpider(scrapy.Spider):
    name = "Webspy"
    allowed_domains = ["www.drogueriascolsubsidio.com"]
    start_urls = ["https://www.drogueriascolsubsidio.com"]

    def parse(self, response):
        pass

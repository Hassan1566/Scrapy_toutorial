import scrapy


class DrugSpider(scrapy.Spider):
    name = "drug"
    allowed_domains = ["www.drogueriascolsubsidio.com"]
    start_urls = ["https://www.drogueriascolsubsidio.com/"]

    def parse(self, response):
        pass

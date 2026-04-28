import scrapy


class VtexSpider(scrapy.Spider):
    name = "vtex"
    allowed_domains = ["www.drogueriascolsubsidio.com"]
    start_urls = ["https://www.drogueriascolsubsidio.com/sitemap/category-0.xml"]

    def parse(self, response):
        pass

from itertools import product
from unicodedata import name

import scrapy


class WebspySpider(scrapy.Spider):
    name = "Webspy"
    allowed_domains = ["www.drogueriascolsubsidio.com"]
    start_urls = ["https://www.drogueriascolsubsidio.com/medicamentos"]

    def parse(self, response):
        products = response.css("div.ProductItemCard__info")
        for product in products:
            yield {
                'name': product.css('div.ProductItemCard__info--wrap__title.pic::text').get(),
                'price': product.css('div.ProductItemCard__info--wrap__prices').get().replace('<div class="ProductItemCard__info--wrap__prices"><div class="ProductItemCard__info--wrap__prices--inner"><div>$\xa0120.400</div><div>$\xa0',"").replace('</div><div>',"").replace('</div></div></div>',""),
            
            }
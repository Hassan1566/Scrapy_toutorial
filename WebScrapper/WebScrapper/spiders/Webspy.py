import scrapy


class WebspySpider(scrapy.Spider):
    name = "Webspy"
    allowed_domains = ["www.drogueriascolsubsidio.com"]
    start_urls = ["https://www.drogueriascolsubsidio.com/medicamentos"]

    import scrapy


class WebspySpider(scrapy.Spider):
    name = "Webspy"
    allowed_domains = ["www.drogueriascolsubsidio.com"]
    start_urls = ["https://www.drogueriascolsubsidio.com/medicamentos"]

    def parse(self, response):
        products = response.css("div.ProductItemCard__info")

        for product in products:
            name = product.css('div.ProductItemCard__info--wrap__title.pic::text').get()
            price = product.css('div.ProductItemCard__info--wrap__prices--inner div::text').getall()
            price = [p.strip().replace('\xa0', ' ') for p in price]
            url = product.xpath('./ancestor::a/@href').get()
            url = response.urljoin(url)

            yield {
                'name': name,
                'price': price,
                'url': url
            }
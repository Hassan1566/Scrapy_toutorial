import scrapy


class ChocolatespySpider(scrapy.Spider):
    name = "chocolatespy"
    allowed_domains = ["chocolate.co.uk"]
    start_urls = ["https://www.chocolate.co.uk/collections/all"]

    def parse(self, response):
        products = response.css("div.product-item")
        for product in products:
            yield {
                'name': product.css("a.product-item-meta__title::text").get(),
                'price': product.css('span.price').get().replace('<span class="price">\n              <span class="visually-hidden">Sale price</span>',"").replace('</span>',""),
                'url': product.css('div.product-item-meta a').attrib['href'],
            }

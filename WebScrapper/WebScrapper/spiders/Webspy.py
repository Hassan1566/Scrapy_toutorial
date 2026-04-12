import scrapy
import re

class WebspySpider(scrapy.Spider):
    name = "Webspy"
    allowed_domains = ["www.drogueriascolsubsidio.com"]
    start_urls = ["https://www.drogueriascolsubsidio.com/medicamentos"]

    def parse(self, response):
        products = response.xpath("//a[.//div[contains(@class,'ProductItemCard__info')]]")

        for product in products:
            name = product.xpath(".//div[contains(@class,'ProductItemCard__info--wrap__title')]//text()").get()
            prices = product.xpath(".//div[contains(@class,'ProductItemCard__info--wrap__prices--inner')]//div/text()").getall()

            # Clean text
            prices = [p.strip().replace('\xa0', ' ') for p in prices if p.strip()]

            # ✅ Separate real prices and PUM
            real_prices = []
            pum_price = None

            for p in prices:
                if re.match(r'^\$\s?\d[\d.,]*$', p):
                    real_prices.append(p)
                else:
                    pum_price = p

            # ✅ Assign correctly
            original_price = real_prices[0] if len(real_prices) > 0 else None
            discounted_price = real_prices[1] if len(real_prices) > 1 else None
            PUM = pum_price

            # ✅ URL (this part was correct)
            url = product.xpath("./@href").get()
            url = response.urljoin(url)

            yield {
                'name': name,
                'original_price': original_price,
                'discounted_price': discounted_price,
                'PUM': PUM,
                'url': url
            }
        # print(response.text[:2000])
        next_page = response.xpath('//a[@title="Ir para Próxima Página"]/@href').get()

        if next_page:
            next_page_url = "https://www.drogueriascolsubsidio.com" + next_page
            yield response.follow(next_page_url, callback=self.parse)
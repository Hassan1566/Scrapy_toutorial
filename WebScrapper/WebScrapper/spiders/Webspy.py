import scrapy


class WebspySpider(scrapy.Spider):
    name = "Webspy"
    allowed_domains = ["www.drogueriascolsubsidio.com"]
    start_urls = ["https://www.drogueriascolsubsidio.com/medicamentos"]

    def parse(self, response):
        products = response.xpath("//a[.//div[contains(@class,'ProductItemCard__info')]]")

        for product in products:
            # ✅ Correct name XPath
            name = product.xpath(".//div[contains(@class,'ProductItemCard__info--wrap__title')]//text()").get()

            # ✅ Correct price XPath
            prices = product.xpath(".//div[contains(@class,'ProductItemCard__info--wrap__prices')]//div/text()").getall()

            prices = [p.strip().replace('\xa0', ' ') for p in prices if p.strip()]

            original_price = prices[0] if prices else None
            discounted_price = prices[1] if len(prices) > 1 else None
            PUM = prices[2] if len(prices) > 2 else None

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
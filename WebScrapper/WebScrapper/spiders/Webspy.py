import scrapy
import re

class WebspySpider(scrapy.Spider):
    name = "Webspy"
    allowed_domains = ["www.drogueriascolsubsidio.com"]
    start_urls = ["https://www.drogueriascolsubsidio.com"]

    custom_settings = {
        "ROBOTSTXT_OBEY": False,
        "DOWNLOAD_DELAY": 1,
        "CONCURRENT_REQUESTS": 2,
        "AUTOTHROTTLE_ENABLED": True,
    }

    def __init__(self):
        self.seen_urls = set()
     

    def parse(self, response):
        categories = response.xpath('//ul[contains(@class,"HeaderContainer__navbar--menu__links")]//li/a')

        for category in categories:
            name = category.xpath(".//text()").getall()
            url = category.xpath("./@href").get()
            if url and url.startswith('/') and 'productClusterIds' not in url:
                full_url = response.urljoin(url)

            yield response.follow(full_url, callback=self.parse_product, 
            meta={
                'category': name
                })

    def parse_product(self, response):
        
        category = response.meta.get('category')
        
        products = response.xpath("//a[.//div[contains(@class,'ProductItemCard__info')]]")

        for product in products:
            try:
                name = product.xpath(".//div[contains(@class,'ProductItemCard__info--wrap__title')]//text()").getall()

                if not name:
                    continue

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
                        pum_price_raw = re.sub(r'^\w+\s+\w+\s+', '', p)
                        pum_price = pum_price_raw

                # ✅ Assign correctly
                original_price = real_prices[0] if len(real_prices) > 0 else None
                discounted_price = real_prices[1] if len(real_prices) > 1 else None
                PUM = pum_price

                # ✅ URL (this part was correct)
                url = product.xpath("./@href").get()
                url = response.urljoin(url)

                if url in self.seen_urls:
                    continue
                self.seen_urls.add(url)

                yield {
                    'category': category,
                    'name': name,
                    'original_price': original_price,
                    'discounted_price': discounted_price,
                    'PUM': PUM,
                    'url': url
                }
            except Exception as e:
                self.logger.error(f"Error in parsing {e}")
        # print(response.text[:2000])
        next_page = response.xpath('//a[@title="Ir para Próxima Página"]/@href').get()

        if next_page:
            next_page_url = "https://www.drogueriascolsubsidio.com" + next_page
            yield response.follow(next_page_url, callback=self.parse_product, 
            meta={
                'category': category
                })
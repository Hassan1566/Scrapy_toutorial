import scrapy


class PhilcospySpider(scrapy.Spider):
    name = "philcospy"
    allowed_domains = ["philcoiluminacion.com"]
    start_urls = ["https://philcoiluminacion.com"]

    def parse(self, response):
        categories = response.xpath("//ul[@id='Slider-template--17845290631339__collection_list']/li")
        for category in categories:
            cat_name = category.xpath(".//h3/a/text()").get()
            cat_url = category.xpath(".//h3/a/@href").get()
            cat_url = response.urljoin(cat_url)
            yield scrapy.Request(cat_url, callback=self.parse_category, meta={'cat_name': cat_name})
    

    def parse_category(self, response):
        cat_name = response.meta['cat_name']
        items = response.xpath("//ul[contains(@class, 'multicolumn-list')]/li")
    
        for item in items:
            links = item.xpath(".//a")
            
            for link in links:
                sub_name = "".join(link.xpath(".//text()").getall()).replace("->", "").strip()
                sub_url = response.urljoin(link.xpath("./@href").get())
                yield scrapy.Request(sub_url, callback=self.parse_products_list, meta={'cat_name': cat_name, 'sub_name': sub_name})
    
    def parse_products_list(self, response):
        cat_name = response.meta['cat_name']
        sub_name = response.meta['sub_name']
        items = response.xpath("//ul[contains(@class, 'product-grid')]/li")
    
        for item in items:
            product_url = response.urljoin(item.xpath(".//a/@href").get())
            yield scrapy.Request(product_url, callback=self.parse_products_details, meta={'cat_name': cat_name, 'sub_name': sub_name})
    
    def parse_products_details(self, response):
        cat_name = response.meta['cat_name']
        sub_name = response.meta['sub_name']
        product_url = response.url
        product_name = response.xpath("//h1/text()").get()
        image_url = response.xpath("//div[contains(@class,'product__media-wrapper')]//img/@src").get()
        product_sku = response.xpath("//span[contains(@class,'product__sku')]/text()").get()
        product_description = response.xpath("//div[contains(@class,'product__description')]//text()").getall()

        # Clean Description
        product_description = [x.strip() for x in product_description if x.strip()]
        product_description = " ".join(product_description).strip()
        
        # Clean Image Url
        image_url = response.urljoin(image_url)        

        
        yield {
            "cat_name": cat_name,
            "sub_name": sub_name,
            "product_name": product_name,
            "product_sku": product_sku,
            "product_description": product_description, 
            "image_url": image_url + "",
            "product_url": product_url,
        }
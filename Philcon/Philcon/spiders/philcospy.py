import scrapy
from Philcon.items import PhilconItem
from Philcon.itemloaders import PhilconItemLoader
class PhilcospySpider(scrapy.Spider):
    name = "philcospy"
    allowed_domains = ["philcoiluminacion.com"]
    start_urls = ["https://philcoiluminacion.com"]

    def parse(self, response):
        categories = response.xpath("//ul[@id='Slider-template--17845290631339__collection_list']/li")
        for category in categories:
            cat_name = category.xpath(".//h3/a/text()").get()
            #print("cat_name", cat_name)
            cat_url = category.xpath(".//h3/a/@href").get()
            cat_url = response.urljoin(cat_url)
            yield scrapy.Request(cat_url, callback=self.parse_category, meta={'cat_name': cat_name})
    

    def parse_category(self, response):
        cat_name = response.meta['cat_name']
        items = response.xpath("//ul[contains(@class, 'multicolumn-list')]/li")
    
        for item in items:
            # 1. Get the Heading (Subcategory 1)
            sub_cat_text = item.xpath(".//h3//text()").getall()
            sub_cat1 = "".join(sub_cat_text).strip()
            #print("sub_cat1", sub_cat1)
            sub_url1 = item.xpath(".//h3/a/@href").get()
        
            # 2. Check for deeper links (Subcategory 2) inside the 'rte' div
            sub_cat2_links = item.xpath(".//div[contains(@class, 'rte')]//a")
        
            if sub_cat2_links:
                # If sub_cat2 exists, loop through them
                for link in sub_cat2_links:
                    sub_cat2 = "".join(link.xpath(".//text()").getall()).replace("->", "").strip()
                    #print("sub_cat2", sub_cat2)
                    sub_url2 = response.urljoin(link.xpath("./@href").get())
                
                    yield scrapy.Request(
                        sub_url2, 
                        callback=self.parse_products_list, 
                        meta={
                            'cat_name': cat_name, 
                            'subcat1_name': sub_cat1, 
                            'subcat2_name': sub_cat2, 
                        }   
                    )
            else:
                # If no sub_cat2, use the sub_cat from the H3
                if sub_url1:
                    full_sub_url = response.urljoin(sub_url1)
                    yield scrapy.Request(
                        full_sub_url, 
                        callback=self.parse_products_list, 
                        meta={
                            'cat_name': cat_name, 
                            'subcat1_name': sub_cat1,
                            'subcat2_name': ""
                        }
                    )
    
    def parse_products_list(self, response):
        cat_name = response.meta['cat_name']
        subcat1_name = response.meta['subcat1_name']
        subcat2_name = response.meta['subcat2_name']
        items = response.xpath("//a[contains(@class,'full-unstyled-link')]/@href").getall()
    
        for item in items:
            product_url = response.urljoin(item)
            #print("product_url", product_url)
            yield scrapy.Request(
                product_url, 
                callback=self.parse_products_details, 
                meta={
                    'cat_name': cat_name, 
                    'subcat1_name': subcat1_name,
                    'subcat2_name': subcat2_name
                })
        next_page = response.xpath("//a[@aria-label='Página siguiente']/@href").get()

        if next_page:
            yield scrapy.Request(
                url=response.urljoin(next_page),
                callback=self.parse_products_list, 
                meta={'cat_name': cat_name, 'subcat1_name': subcat1_name, 'subcat2_name': subcat2_name} 
            )
    
    def parse_products_details(self, response):
        item = PhilconItemLoader(item=PhilconItem(), selector=response)
        item.add_value('category', response.meta['cat_name'])
        item.add_value('subcategory1', response.meta['subcat1_name'])
        item.add_value('subcategory2', response.meta['subcat2_name'])
        item.add_value('product_url', response.url)
        
        item.add_xpath('product_name', "//h1/text()")
        item.add_xpath('product_description', "//div[contains(@class,'product__description')]//text()") 
        item.add_xpath('product_sku', "//p[contains(@id, 'Sku')]/text()")
        item.add_xpath('image_url', "//div[contains(@class,'product__media')]//img/@src")
        yield item.load_item()
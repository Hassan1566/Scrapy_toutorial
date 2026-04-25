import scrapy
import json
from API_Scripting.items import FarmaciaItem
from API_Scripting.itemloaders import FarmaciaTeapaItemLoader

class FarmaciaTepaSpider(scrapy.Spider):
    name = "scrap"
    start_urls = ["https://farmaciatepa.com.mx/"]
    allowed_domains = ["farmaciatepa.com.mx"]

    def start_requests(self):
        url = "https://farmaciatepa.com.mx/api/products/getCategories"
        yield scrapy.Request(url, callback=self.parse_categories)

    def parse_categories(self, response):
        data = json.loads(response.text)
        for dept in data.get('departments', []):
            payload = {
                'TYPE': "DEPARTMENT",
                'TYPE_ID': dept.get('ID'),
                'PAGE': 1,
                'ORDER': "Relevancia",
                'TOKEN': "",
                'FIREBASE_TOKEN': "",
            }

            yield scrapy.Request(
                url='https://farmaciatepa.com.mx/api/products/searchProductsBy',
                method='POST',
                body=json.dumps(payload),
                callback=self.parse_products,
                meta={'payload': payload}
                )

    def parse_products(self, response):

        #with open('last_response.json', 'w') as f:
        #    f.write(response.text)
        data = json.loads(response.text)
        
        #if not data.get('ok'):
        #    self.logger.error(f"SERVER REJECTED REQUEST: {data.get('info')}")
        #    return

        # Use the key 'products' as seen in your log screenshot
        products = data.get('products', [])
        
        #self.logger.info(f"Retrieved {len(products)} products for group {response.meta.get('group_name')}")

        for p in products:
            loader = FarmaciaTeapaItemLoader(item=FarmaciaItem(), response=response)
            loader.add_value('SKU', p.get('SKU'))
            loader.add_value('Item', p.get('NAME'))
            loader.add_value('Brand', p.get('BRAND'))
            loader.add_value('URLSKU', p.get('SKU'))
            loader.add_value('Price', p.get('PRICE_UNIT'))
            loader.add_value('SalePrice', p.get('PUBLIC_PRICE'))
            loader.add_value('SubCategory2', p.get('CATEGORY_NAME'))
            loader.add_value('SubCategory1', p.get('GROUP_NAME'))
            loader.add_value('Category', p.get('DEPARTMENT_NAME'))
            loader.add_value('Stock', p.get('UNITS_STOCK'))
            loader.add_value('Image', p.get('PHOTO_CODE'))
            yield loader.load_item()

        # Pagination
        if products and len(products) >= 100: 
            new_payload = response.meta['payload']
            new_payload['PAGE'] += 1
            
            yield scrapy.Request(
                url='https://farmaciatepa.com.mx/api/products/searchProductsBy',
                method='POST',
                body=json.dumps(new_payload),
                callback=self.parse_products,
                meta={'payload': new_payload, 'group_name': response.meta.get('group_name')}
            )
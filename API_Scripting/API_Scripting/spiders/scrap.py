import scrapy
import json
from API_Scripting.items import FarmaciaItem

class FarmaciaTepaSpider(scrapy.Spider):
    name = "scrap"
    start_urls = ["https://farmaciatepa.com.mx/"]
    allowed_domains = ["farmaciatepa.com.mx"]

    def start_requests(self):
        url = "https://farmaciatepa.com.mx/api/products/getCategories"
        yield scrapy.Request(url, callback=self.parse_categories)

    def parse_categories(self, response):
        data = json.loads(response.text)
        # Your CURL showed a list of 'groups' within the category response
        for group in data.get('groups', []):
            payload = {
                'TYPE': "GROUP",
                'TYPE_ID': int(group.get('ID')),
                'PAGE': 1,
                'ORDER': "Relevancia",
                'TOKEN': "",
                'FIREBASE_TOKEN': "",
            }
            heaers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
            }
            
            yield scrapy.Request(
                url='https://farmaciatepa.com.mx/api/products/searchProductsBy',
                method='POST',
                body=json.dumps(payload),
                callback=self.parse_products,
                headers=heaers,
                meta={'payload': payload, 'group_name': group.get('NAME')}
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
        
        self.logger.info(f"Retrieved {len(products)} products for group {response.meta.get('group_name')}")

        for p in products:
            item = FarmaciaItem()
            item['SKU'] = p.get('SKU')
            item['Item'] = p.get('NAME')
            item['Brand'] = p.get('BRAND')
            item['Price'] = p.get('PRICE_UNIT')
            item['SalePrice'] = p.get('PUBLIC_PRICE')
            item['SubCategory2'] = p.get('CATEGORY_NAME')
            item['SubCategory1'] = p.get('GROUP_NAME')
            item['Category'] = p.get('DEPARTMENT_NAME')
            item['Stock'] = p.get('UNITS_STOCK')
            
            base = p.get('PHOTO_URL_BASE', '')
            file = p.get('PHOTO_FILE', '')
            item['Image'] = f"{base}{file}" if base and file else None
            
            yield item

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
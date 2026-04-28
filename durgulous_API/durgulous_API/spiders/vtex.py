import scrapy
import base64
import json
from urllib.parse import urlencode

from durgulous_API.items import ProductItem
from durgulous_API.itemloaders import ProductLoader

class VtexSpider(scrapy.Spider):
    name = "vtex"
    start_urls = ["https://www.drogueriascolsubsidio.com/sitemap/category-0.xml"]

    # This is the Persisted Query Hash you found in the network tab
    SHA_256_HASH = "31d3fa494df1fc41efef6d16dd96a96e6911b8aed7a037868699a1f3f4d365de"

    def parse(self, response):
        # Scrapy's .remove_namespaces() handles the 'ns' problem automatically!
        response.selector.remove_namespaces()
        
        # We use XPath to find all <loc> tags directly
        urls = response.xpath('//loc/text()').getall()
        
        for url in urls:
            # Optimization: Use .rstrip instead of .strip for speed with long strings
            category_path = url.replace('https://www.drogueriascolsubsidio.com/', '').rstrip('/')
            
            if category_path:
                yield self.build_vtex_request(category_path, start=0, count=50)
    def build_vtex_request(self, category_path, start, count):
        """Helper to build the GraphQL Request"""
        parts = category_path.split('/')
        
        variables_dict = {
            "hideUnavailableItems": False,
            "skusFilter": "ALL",
            "simulationBehavior": "default",
            "installmentCriteria": "MAX_WITHOUT_INTEREST",
            "productOriginVtex": False,
            "map": ",".join(["c"] * len(parts)), 
            "query": category_path,
            "orderBy": "OrderByScoreDESC",
            "from": start,
            "to": start + count - 1,
            "selectedFacets": [{"key": "c", "value": p} for p in parts],
            "facetsBehavior": "Static",
            "categoryTreeBehavior": "default",
            "withFacets": False,
            "variant": "null-null"
        }

        encoded_vars = base64.b64encode(json.dumps(variables_dict).encode()).decode()

        params = {
            "workspace": "master",
            "maxAge": "short",
            "appsEtag": "remove",
            "domain": "store",
            "locale": "es-CO",
            "__bindingId": "f6e98a9f-25bc-476b-b0df-62ddc6b57b48",
            "operationName": "productSearchV3",
            "variables": "{}",
            "extensions": json.dumps({
                "persistedQuery": {
                    "version": 1,
                    "sha256Hash": self.SHA_256_HASH,
                    "sender": "vtex.store-resources@0.x",
                    "provider": "vtex.search-graphql@0.x"
                },
                "variables": encoded_vars
            })
        }
        
        url = f"https://www.drogueriascolsubsidio.com/_v/segment/graphql/v1?{urlencode(params)}"
        
        return scrapy.Request(
            url=url, 
            callback=self.parse_products,
            meta={'vars_dict': variables_dict}
        )

    def parse_products(self, response):
        raw_data = json.loads(response.text)
        search_data = (raw_data.get('data') or {}).get('productSearch') or {}
        products = search_data.get('products') or []
    
        for p in products:
            print(f"DEBUG URL PATH: {p.get('link')}")
            items = p.get('items') or []
            if not items: continue
                
            first_item = items[0]
            offer = (first_item.get('sellers') or [{}])[0].get('commertialOffer') or {}

            # Use the custom Loader we just created
            loader = ProductLoader(item=ProductItem(), response=response) 
        
            loader.add_value('name', p.get('productName'))
            loader.add_value('brand', p.get('brand'))
            loader.add_value('product_id', p.get('productId'))
            loader.add_value('sku', first_item.get('itemId'))

            # Extract Product URL
            product_path = p.get('link')
            loader.add_value('url', product_path)

            # Extract Category Hierarchy
            all_categories = p.get('categories', [])
            if all_categories:
                # The first one is usually the longest/deepest path
                raw_path = all_categories[0].strip('/')
                
                # Split path to get individual levels
                levels = raw_path.split('/')
                
                if len(levels) >= 1:
                    loader.add_value('category', levels[0])
                if len(levels) >= 2:
                    loader.add_value('subcat1', levels[1])
                if len(levels) >= 3:
                    loader.add_value('subcat2', levels[2])
                if len(levels) >= 4:
                    loader.add_value('subcat3', levels[3])
            
            # Extract Images
            images = first_item.get('images') or []
            if images:
                loader.add_value('image_url', images[0].get('imageUrl'))
        
            # Prices
            prices = p.get('priceRange') or {}
            loader.add_value('list_price', (prices.get('listPrice') or {}).get('lowPrice'))
            loader.add_value('discounted_price', (prices.get('sellingPrice') or {}).get('lowPrice'))
        
            loader.add_value('stock', offer.get('AvailableQuantity'))
        
            # Specs loop
            for group in (p.get('specificationGroups') or []):
                for spec in (group.get('specifications') or []):
                    val = (spec.get('values') or [None])[0]
                    name = spec.get('name')
                
                    if name == 'ID Invima': loader.add_value('invima', val)
                    elif name == 'PUM': loader.add_value('pum', val)
                    elif name == 'Presentación': loader.add_value('presentacion', val)

            yield loader.load_item()

        # Pagination Logic
        records_filtered = search_data.get('recordsFiltered', 0)
        current_vars = response.meta.get('vars_dict')

        if current_vars:
            current_to = current_vars.get('to', 0)
            if current_to < (records_filtered - 1):
                next_from = current_to + 1
                # Trigger next request
                yield self.build_vtex_request(
                    category_path=current_vars.get('query'),
                    start=next_from,
                    count=50
                )
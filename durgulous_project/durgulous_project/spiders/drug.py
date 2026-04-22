import scrapy
import json
from scrapy.selector import Selector
from durgulous_project.itemloader import DrugItemLoader
from durgulous_project.items import DrugItem

class DrugSpider(scrapy.Spider):
    name = "drug"

    def start_requests(self):
        url = "https://www.drogueriascolsubsidio.com/"
        yield scrapy.Request(url=url, meta={
            "playwright": True,
            "playwright_include_page": True,
            'playwright_page_goto_kwargs': {
                "timeout": 90000,
                "wait_until": "domcontentloaded",
            },
        }, callback=self.parse)

    async def parse(self, response):
        page = response.meta['playwright_page']

        # 1. Handle the "Location" Modal (based on previous HTML)
        try:
            await page.wait_for_selector(".AddressSelector__container--window__top button", timeout=5000)
            await page.click(".AddressSelector__container--window__top button", force=True)
            await page.wait_for_timeout(2000)
        except Exception:
            pass

        # 2. Open the Menu and Wait for the Container
        await page.click(".HeaderSectionButton-menu", force=True)
        await page.wait_for_selector(".menuDeskContainer", state="attached", timeout=10000)

        # 3. Get all main Category list items (Left Side)
        main_cats = await page.query_selector_all(".categoriasMenuDesk__menuDesktopLeft ul li.link-level-1")

        for cat in main_cats:
            # Get Category Name
            cat_name = await cat.inner_text()
            #print(f"\n[CATEGORY]: {cat_name.strip()}")

            # 4. HOVER to update the right side
            await cat.hover()
            await page.wait_for_timeout(1000)

            # 5. Extract the Right Side (Subcats) from the LIVE content
            sel = Selector(text=await page.content())
        
            # Each 'columnaSubcat' is a group (Subcat1 + its Subcat2 list)
            columns = sel.xpath(".//div[@class='categoriasMenuDesk__columnaSubcat']")

            for col in columns:
                # Subcategory Level 1 (The Header)
                sub1_item = col.xpath(".//h4")
                s1_name = "".join(sub1_item.xpath(".//text()").getall()).strip()
                s1_url = response.urljoin(sub1_item.xpath("./@data-event-link-url").get())

                # Subcategory Level 2 (The Links inside the <ul>)
                sub2_items = col.xpath(".//ul/li/a[contains(@class,'link-level-3')]")
                if sub2_items:
                    for s2 in sub2_items:
                        s2_parts = s2.xpath(".//text()").getall()
                        s2_name = ''.join(s2_parts).strip()
                        s2_url = response.urljoin(s2.xpath("./@href").get())
                        yield scrapy.Request(url=s2_url, callback=self.parse_product_list, meta={
                           'cat_name': cat_name,
                           'subcat1_name': s1_name,
                           'subcat2_name': s2_name,
                        })
                elif s1_url:
                    yield scrapy.Request(url=s1_url, callback=self.parse_product_list, meta={   'cat_name': cat_name,
                           'subcat1_name': s1_name,
                           'subcat2_name': "N/A",
                    })
        

        await page.wait_for_timeout(20000)
        
        await page.close()
    

    def parse_product_list(self, response):
    # --- 1. EXTRACT PRODUCTS ---
        items = response.xpath('.//section[contains(@class, "vtex-product-summary-2-x-container")]')
        for item in items:
            json_data_str = item.xpath('.//div[contains(@class, "set-click-datalayer")]/@data-ecommerce-select-item').get()
            if json_data_str:
                yield from self.extract_json_data(json_data_str, response)

        # --- 2. PAGINATION (Production Level) ---
        # Look for the "Next Page" link specifically
        next_page_path = response.xpath('//a[@title="Ir para Próxima Página"]/@href').get()
    
        if next_page_path:
            # urljoin handles the relative path "/dermocosmetica/cuidado-facial?page=2..."
            next_page_url = response.urljoin(next_page_path)
            yield scrapy.Request(
                url=next_page_url,
                callback=self.parse_product_list,
                meta=response.meta # Keep category context
            )
    
    def extract_json_data(self, json_data_str, response):
        data = json.loads(json_data_str)
        loader = DrugItemLoader(item=DrugItem())
        # Basic meta data
        loader.add_value('category', response.meta['cat_name'])
        loader.add_value('subcategory1', response.meta['subcat1_name'])
        loader.add_value('subcategory2', response.meta['subcat2_name'])

        # Extract product data
        loader.add_value('product_name', data.get('productName'))
        loader.add_value('brand', data.get('brand'))
        loader.add_value('product_url', response.urljoin(data.get('link')))

        # Price Data
        p_range = data.get('priceRange', {})
        loader.add_value('price', p_range.get('sellingPrice', {}).get('lowPrice'))
        loader.add_value('old_price', p_range.get('listPrice', {}).get('highPrice'))

        # Image Data
        sku_list = data.get('items', [])
        if sku_list:
            img_data = sku_list[0].get('images', [])
            if img_data:
                loader.add_value('image_url', img_data[0].get('imageUrl'))

        # Nested Product Information
        spec_groups = data.get('specificationGroups', [])
        for group in spec_groups:
            for spec in group.get('specifications', []):
                name = spec.get('name', '').lower()
                value = spec.get('values', [None])[0]

                if 'invima' in name:
                    loader.add_value('id_invima', value)
                elif 'presentación' in name:
                    loader.add_value('presentation', value)

        yield loader.load_item()
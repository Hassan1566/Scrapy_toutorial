from itemloaders.processors import TakeFirst, MapCompose
from scrapy.loader import ItemLoader

def clean_price(value):
    """Optional: Convert 209325 to 209325.0 or format it"""
    if value is None:
        return 0
    return float(value)

def make_absolute_url(path):
    base_url = "https://www.drogueriascolsubsidio.com"
    return f"{base_url}{path}"



class ProductLoader(ItemLoader):
    # Default: if we don't specify, just take the first item found
    default_output_processor = TakeFirst()

    image_url_out = TakeFirst()
    url_in = MapCompose(make_absolute_url)



    # Apply specific cleaning to prices
    list_price_in = MapCompose(clean_price)
    discounted_price_in = MapCompose(clean_price)

    # If the category hierarchy comes as a list, we can clean the slashes
    category_in = MapCompose(lambda x: x.strip('/'))
    subcat1_in = MapCompose(lambda x: x.strip('/'))
    subcat2_in = MapCompose(lambda x: x.strip('/'))
    subcat3_in = MapCompose(lambda x: x.strip('/'))
    subcat4_in = MapCompose(lambda x: x.strip('/'))

    def load_item(self):
        item = super().load_item()
        
        # Get the prices from the loaded item dictionary
        list_p = item.get('list_price')
        disc_p = item.get('discounted_price')

        # Logic: If they are the same, make discounted_price None
        if list_p and disc_p and float(list_p) == float(disc_p):
            item['discounted_price'] = None
            
        return item
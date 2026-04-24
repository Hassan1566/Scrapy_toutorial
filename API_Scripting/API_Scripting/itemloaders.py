from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose

class FarmaciaTeapaItemLoader(ItemLoader):


    default_output_processor = TakeFirst()
    
    @staticmethod
    def clean_price(value):
        return float(value)

    @staticmethod
    def clean_stock(values):
        return int(values)

    @staticmethod
    def clean_text(values):
        return values.strip()

    @staticmethod
    def final_url_fix(value):
        if not value:
            return ''
        
        # 1. If it's already a full URL, just return it
        if value.startswith('http'):
            return value
            
        # 2. If it's just the filename, wrap it in the domain
        # Check if it's a UUID (needs SM/) or a SKU (needs root)
        path = ""
        if "-" in value and len(value) > 20:
            path = "SM/"
            
        return f"https://farmaciatepa.com.mx/FT/img/products/{path}{value}"

    # Apply only this one processor to the Image field
    Image_in = MapCompose(final_url_fix)
    Price_in = MapCompose(clean_price)
    Stock_in = MapCompose(clean_stock)
    Item_in = MapCompose(clean_text)
    Brand_in = MapCompose(clean_text)
    Category_in = MapCompose(clean_text)
    SubCategory1_in = MapCompose(clean_text)
    SubCategory2_in = MapCompose(clean_text)
    SKU_in = MapCompose(clean_text)
    SalePrice_in = MapCompose(clean_price)
    Image_in = MapCompose(final_url_fix)
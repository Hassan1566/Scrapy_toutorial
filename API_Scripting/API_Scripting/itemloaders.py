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
    def process_tepa_image(values):
        if values:
            base_url = "https://farmaciatepa.com.mx/FT/img/products/MD/"
            return f"{base_url}{values}.webp"
        return ""
    
    @staticmethod
    def process_sku(values):
        if values:
            return f"https://farmaciatepa.com.mx/#/product_view/{values}"
        return ""
    URLSKU_in = MapCompose(process_sku)
    Image_in = MapCompose(process_tepa_image)
    Price_in = MapCompose(clean_price)
    Stock_in = MapCompose(clean_stock)
    Item_in = MapCompose(clean_text)
    Brand_in = MapCompose(clean_text)
    Category_in = MapCompose(clean_text)
    SubCategory1_in = MapCompose(clean_text)
    SubCategory2_in = MapCompose(clean_text)
    SKU_in = MapCompose(clean_text)
    SalePrice_in = MapCompose(clean_price)
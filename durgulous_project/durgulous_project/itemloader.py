from itemloaders.processors import TakeFirst, MapCompose
from itemloaders import ItemLoader




class DrugItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    
    @staticmethod
    def clean_text(value):
        # Only return if there is actual text after stripping
        return value.strip() if value.strip() else None 
    @staticmethod
    def format_price_with_dots(value):
        """Converts 73000 to '73.000'"""
        if value is None or value == "":
            return None
        try:
            # Convert to float then int to handle cases like 73000.0
            return f"{int(float(value)):,}".replace(",", ".")
        except (ValueError, TypeError):
            return value
        
    @staticmethod
    def clean_link(value):
        if isinstance(value, str):
            return value.strip()
        return None
    
    # Define input processors for each field
    category_in = MapCompose(clean_text)
    subcategory1_in = MapCompose(clean_text)
    subcategory2_in = MapCompose(clean_text)
    product_name_in = MapCompose(clean_text)
    brand_in = MapCompose(clean_text)
    old_price_in = MapCompose(format_price_with_dots)
    price_in = MapCompose(format_price_with_dots)
    image_url_in = MapCompose(clean_text)
    product_url_in = MapCompose(clean_link)
    id_invima_in = MapCompose(clean_text)
    presentation_in = MapCompose(clean_text)


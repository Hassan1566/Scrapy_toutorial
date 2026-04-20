from itemloaders.processors import TakeFirst, MapCompose, Join
from itemloaders import ItemLoader
from itemadapter import ItemAdapter

class PhilconItemLoader(ItemLoader):
    default_output_processor = TakeFirst()

    @staticmethod
    def clean_text(value):
        # Only return if there is actual text after stripping
        return value.strip() if value.strip() else None

    @staticmethod
    def clean_sku(value):
        return value.replace("SKU:","").strip()

    @staticmethod
    def fix_shopify_url(value):
        # Fixes the double domain issue
        if not value:
            return None
        if "philcoiluminacion.com" in value:
            # If it already has the domain but starts with //
            if value.startswith("//"):
                return "https:" + value
            return value
        return 'https://philcoiluminacion.com' + value

    product_name_in = MapCompose(clean_text)
    product_sku_in = MapCompose(clean_sku)
    category_in = MapCompose(clean_text)
    subcategory1_in = MapCompose(clean_text)
    subcategory2_in = MapCompose(clean_text)
    
    # Use the specific fix for image URLs
    image_url_in = MapCompose(fix_shopify_url)
    
    # Use Step 4: MapCompose cleans each fragment, Join merges them
    product_description_in = MapCompose(clean_text)
    product_description_out = Join(" ")
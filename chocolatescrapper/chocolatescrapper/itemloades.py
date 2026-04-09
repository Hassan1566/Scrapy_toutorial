from itemloaders.processors import TakeFirst, MapCompose
from itemloaders import ItemLoader

class ChocolateItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    url_in = MapCompose(lambda x: 'https://www.chocolate.co.uk' + x)
    
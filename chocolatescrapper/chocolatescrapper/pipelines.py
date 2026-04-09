# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class PriceToUsdPipeline:
    gbp_to_usd_rate = 1.25  
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter .get('price'):
            float_price = float(adapter['price'])
            adapter['price'] = float_price * self.gbp_to_usd_rate
            return item
        else:
            raise DropItem("Missing price in %s" % item)

class duplicatepiPipelines:
    def __init__(self):
        self.name_seen = set()
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['name'] in self.name_seen:
            raise DropItem("Duplicate item found: %s" % item)
        self.name_seen.add(adapter['name'])
        return item

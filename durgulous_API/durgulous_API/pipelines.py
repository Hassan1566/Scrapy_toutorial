# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

class DuplicatePipeline:
    def __init__(self):
        self.seen = set()
    def process_item(self, item, spider):
        sku = item.get('sku')
        if sku in self.seen:
            raise DropItem(f"Duplicate item found: {sku}")
        self.seen.add(sku)
        return item

        
        return item

class DurgulousApiPipeline:
    def process_item(self, item, spider):
        return item
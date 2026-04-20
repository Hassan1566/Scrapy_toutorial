# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class DuplicatesPipeline:
    def __init__(self):
        self.url_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['product_url'] in self.url_seen:
            raise DropItem(f"Duplicate product url found: {adapter['product_url']}")
        else:
            self.url_seen.add(adapter['product_url'])
            return item
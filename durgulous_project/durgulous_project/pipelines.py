# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class DurgulousProjectPipeline:
    def __init__(self):
        self.url_seen = set()

    def process_item(self, item, spider):
        # Check if both prices exist
        price = item.get('price')
        old_price = item.get('old_price')

        # If they are identical strings (e.g., both "39.450"), 
        # it means there is no discount.
        if price and old_price and price == old_price:
            item['old_price'] = None

        adapter = ItemAdapter(item)
        if adapter['product_url'] in self.url_seen:
            raise DropItem(f"Duplicate product url found: {adapter['product_url']}")
        else:
            self.url_seen.add(adapter['product_url'])
        return item

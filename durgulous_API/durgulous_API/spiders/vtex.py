import scrapy
import xml.etree.ElementTree as ET
import base64
import json
from urllib.parse import urlencode

class VtexSpider(scrapy.Spider):
    name = "vtex"
    start_urls = ["https://www.drogueriascolsubsidio.com/sitemap/category-0.xml"]

    def parse(self, response):
        # Parse the XML namespace correctly
        namespaces = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        root = ET.fromstring(response.body)
        
        # Extract every <loc> URL
        urls = [loc.text for loc in root.findall('.//ns:loc', namespaces)]
        
        for url in urls:
            # Clean the URL to analyze structure
            path_parts = url.replace('https://www.drogueriascolsubsidio.com/', '').strip('/').split('/')
            
            # depth 1 = Dept, 2 = Category, 3 = Subcategory
            depth = len(path_parts)
            
            yield {
                'url': url,
                'name': path_parts[-1].replace('-', ' ').title()
            }
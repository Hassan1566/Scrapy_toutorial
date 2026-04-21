import scrapy
from quotes_js_scraper.items import QuoteItem


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
     
    def start_requests(self):
        url = "https://quotes.toscrape.com"
        yield scrapy.Request(url=url, meta={"playwright":True, 
                                        "playwright_include_page":True,
                                        "errback":self.errback})


    async def parse(self, response):
        page = response.meta['playwright_page']
        self.logger.info(f"Scraping: {response.url}")
        await page.wait_for_selector("div.quote")
        
        
        
        
        
        for q in response.css('div.quote'):
            quote = QuoteItem()
            quote['text'] = q.css('span.text::text').get()
            quote['author'] = q.css('small.author::text').get()
            quote['tags'] = q.css('div.tags a.tag::text').getall()
            yield quote
        
        await page.close()

    async def errback(self, failure):
        page = failure.request.meta['playwright_page']
        await page.close()
        self.logger.error(repr(failure))
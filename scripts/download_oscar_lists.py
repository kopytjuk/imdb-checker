import scrapy
from scrapy.linkextractors import LinkExtractor

class OscarsSpider(scrapy.Spider):
    name = 'Oscars spider'
    start_urls = [
        r'file://C:/Users/kopyt/Code/imdb-checker/oscar2005.html',
    ]
    link_extractor = LinkExtractor(allow=r"\/title\/tt\d{7,8}\S*")

    def parse(self, response):

        links = list(set(self.link_extractor.extract_links(response)))

        self.logger.info(f"Found {len(links)} urls.")
        
        for link in links:
            yield {"url": link.url}

import scrapy
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import Rule

class SiteScraper(scrapy.Spider):
    name = "linkscraper"
    allowed_domains = ['livetecs.com']
    start_urls = ['https://www.livetecs.com']

    def parse(self, response):
        try:
            for hrefs in response.css('a'):
                try:
                    link = hrefs.xpath('@href').extract()[0]
                    if not (link.startswith('/') or link.startswith('#') or link.startswith('javascript') or link.startswith('mailto')):
                        yield scrapy.Request(link, callback=self.parse_link)
                except:
                    pass
        except:
            pass

    def parse_link(self, response):
        for hrefs in response.css('a'):
            try:
                link = hrefs.xpath('@href').extract()[0]
                if not (link.startswith('/') or link.startswith('#') or link.startswith('javascript') or link.startswith('mailto')):
                    yield {
                        'Link' : link,
                        'Refer' : response.url
                    }
            except:
                pass


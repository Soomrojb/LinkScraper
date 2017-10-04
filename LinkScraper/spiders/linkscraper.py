import scrapy
from urlparse import urljoin
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import Rule
from bs4 import BeautifulSoup

BaseURL = "https://www.livetecs.com/"

class SiteScraper(scrapy.Spider):
    name = "linkscraper"
    allowed_domains = ['livetecs.com']
    start_urls = ['https://www.livetecs.com']

    def parse(self, response):
        Soup = BeautifulSoup(response.body, "lxml")
        for Hrefs in Soup.select('a'):
            link = Hrefs['href']
            if link.startswith('/'):
                link = urljoin(BaseURL, link)
            if not (link.startswith('#') or link.startswith('javascript') or link.startswith('mailto')):
                yield scrapy.Request(link, callback=self.parse_link)
    
    def parse_link(self, response):
        Soup = BeautifulSoup(response.body, "lxml")
        for Hrefs in Soup.select('a'):
            link = Hrefs['href']
            if link.startswith('/'):
                link = urljoin(BaseURL, link)
            yield {
                'Link'      :   link,
                'Referrer'  :   response.url
            }
            if not (link.startswith('#') or link.startswith('javascript') or link.startswith('mailto')):
                yield scrapy.Request(link, callback=self.parse_link)

from scrapy.spider import BaseSpider
from scrapy.http import Request
from bs4 import BeautifulSoup
import time, urllib

class GoogleParser(BaseSpider):

    name = "googleparser"
    
    allowed_urls = ["google.com"]

    max_results = None
    count = 10
    query = ""
    _url = "http://www.google.com/search?q="
    
    def start_requests(self):

        if not self.query:
            self.query = str(urllib.quote(raw_input("What would you like to search Google for?\n")))
            self.max_results = input("How many results would you like before the spider stops?\n")
            self._url += self.query + "&start="
        
        return [Request(url=self._url + str(self.count), callback=self.parse)]

    def parse(self, response):
        if self.count >= self.max_results:
            exit
        else:
            self.count += 10

        soup = BeautifulSoup(response.body)
        
        for link in soup('a'):
            if "/url?q=" in link['href']:
                print str(link['href'].split('&')[0][7:]) + "\n"
                print " -- " + str(link.find_next('div', 's').find('span', 'st')) + "\n"
            
        
        yield Request(url=self._url + str(self.count), callback=self.parse)

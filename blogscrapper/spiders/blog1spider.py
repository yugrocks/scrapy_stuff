from __future__ import absolute_import
import scrapy
from blogscrapper.spiders import clean_write
from functools import partial
from scrapy.exceptions import CloseSpider
import logging
logging.getLogger('scrapy').propagate = False

class Spider1(scrapy.Spider):
    name = "medicalgeekspider"
    pages_visited = set()
    file = open("medical_geek_data.txt", "w")
    total_threads = 0

    def start_requests(self):
        logging.getLogger('scrapy').propagate = False
        start_urls = [
            "http://www.medicalgeek.com/medicalgeek-cafe/patient-s-corner/",
            "http://www.medicalgeek.com/medicalgeek-cafe/patient-s-corner/index2.html",
        ]
        for link in start_urls:
            yield scrapy.Request(url=link, callback=self.parse)

    def parse(self, response):
        links_to_threads = response.css("li.threadbit a.title::attr(href)").extract()
        for link in links_to_threads:
            if (response.url+link) not in self.pages_visited:
                yield response.follow(url=link, callback=self.parse_thread)
                self.pages_visited.add(response.url+link)
            else:
                print("Link already visited")

    def parse_thread(self, response):
        if response.url not in self.pages_visited:
            self.pages_visited.add(response.url)
            self.total_threads += 1
            print("TOTAL THREADS = ",self.total_threads)
            data = response.css("div.content blockquote.postcontent::text").extract()
            self.file.write("\n\n\n")
            clean_write.clean_write(" ".join(" ".join(data).split()), self.file)
            # Now parse the similar threads
            links_to_similar_threads = response.css("div h6 a::attr(href)").extract()[0:] # Exclude 1st one as it containes js shit
            for link in links_to_similar_threads:
                yield response.follow(url=link, callback=self.parse_thread)
        else:
            yield ""

    def spider_closed(self, spider):
        spider.logger.info('Spider closed: %s', spider.name)
        self.file.close()

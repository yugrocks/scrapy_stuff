from __future__ import absolute_import
import scrapy
from .. import items
from blogscrapper.spiders import clean_write
import logging

logging.getLogger('scrapy').propagate = False

class diseasespider(scrapy.Spider):
    name = "diseasespider"

    def start_requests(self):
        logging.getLogger('scrapy').propagate = False
        start_urls = [
            "https://www.mayoclinic.org/diseases-conditions",
                      ]
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse_page)

    def parse_page(self, response):
        # this page is the one with an A-Z list
        links = response.css("ol.alpha li a::attr(href)").extract()
        for link in links:
            yield response.follow(url=link, callback=self.parse_list_page)
        

    def parse_list_page(self, response):
        # this page is the one with diseases named starting with a given alphabet
        links = response.css("div#index li a::attr(href)").extract()
        names = response.css("div#index li a::text").extract()
        for link in links:
            yield response.follow(url=link, callback=self.disease_page)

    def disease_page(self, response):
        # this page is the main disease page that tells the symptoms
        
        first_para = response.xpath("//h2[contains(text(), 'Symptoms')]/following-sibling::p")
        if len(first_para) > 0:
            first_para = first_para[0]
            symptoms_1 = "\n".join(first_para.css("::text").extract())
        else:
            symptoms_1 = ""
        first_list=response.xpath("//h2[contains(text(), 'Symptoms')]/following-sibling::ul")
        if len(first_list) > 0: 
            first_list = first_list[0]
            symptoms_2 = "\n".join(first_list.css("li::text").extract())
        else:
            symptoms_2 = ""
        disease_name = response.css("h1 a::text").extract_first()
        dis = items.DisItem(disease_name=disease_name, symptoms_1=symptoms_1, symptoms_2=symptoms_2)
        print(disease_name)
        yield dis
        
        

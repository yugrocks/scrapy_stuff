from __future__ import absolute_import
import scrapy
from .. import items
from blogscrapper.spiders import clean_write
import logging


class MyTherepyCoachSpider(scrapy.Spider):
    name = "mytherepycoachspider"
    num_posts = 0

    def start_requests(self):
        start_urls = [
            #'http://www.mytherapycouch.com/forums/depression/',
            #'http://www.mytherapycouch.com/forums/parenting/',
            #'http://www.mytherapycouch.com/forums/divorce_and_separation/',
            #'http://www.mytherapycouch.com/forums/abuse/',
            #'http://www.mytherapycouch.com/forums/work_stress/',
            #'http://www.mytherapycouch.com/forums/physical_illness/',
            #'http://www.mytherapycouch.com/forums/self_esteem_and_shyness/',
            #'http://www.mytherapycouch.com/forums/sexuality_and_gender/',
            #'http://www.mytherapycouch.com/forums/post-trauma_stress_disorder/',
            #'http://www.mytherapycouch.com/forums/bipolar_disorder/',
            #'http://www.mytherapycouch.com/forums/anxiety_and_panic_disorders/',
            #'http://www.mytherapycouch.com/forums/eating_disorders/',
            #'http://www.mytherapycouch.com/forums/co-dependency/',
            #'http://www.mytherapycouch.com/forums/obsessive_compulsive_disorder/',
            #'http://www.mytherapycouch.com/forums/schizophrenia_and_psychosis/',
            #'http://www.mytherapycouch.com/forums/addiction/',
            'http://www.mytherapycouch.com/forums/family_and_relationships/',
            ]
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse_page)

    def parse(self, response):
        links = response.xpath("//div[@id='column_a']/ul/li/p/a/@href").extract()
        for link in links:
            yield response.follow(url=link, callback=self.parse_page)

    def parse_page(self, response):
        post_links = response.xpath("//div[@id='page_container']/ul/li/div/h3/a/@href").extract()
        for link in post_links:
            yield response.follow(url=link, callback=self.parse_thread)
        # now handling the ajax thing
        request_url = "http://www.mytherapycouch.com/forums/depression/http://www.mytherapycoach.com/forums/depression/?ajax=1&page="
        pages = response.css("div#pagination ol.styled_list li a::text").extract()
        if len(pages) > 1:
            for page in pages:
                yield response.follow(url=request_url+page, callback=self.parse_next_pages)

    def parse_next_pages(self, response):
        post_links = response.xpath("//div[@id='forum_title']/h3/a/@href").extract()
        for link in post_links:
            yield response.follow(url=link, callback=self.parse_thread)
        
    def parse_thread(self, response):
        heading = " ".join(response.css("div#forum_title h3::text").extract())
        d_a_r = response.xpath("//div[@class='poster_post']/blockquote")
        if len(d_a_r)>0: #description exists
            description = " ".join(d_a_r[0].xpath("text()").extract())
        replies = ""
        delimiter = "__delimiter__"
        if len(d_a_r)>1: #replies exist
            for i in range(1, len(d_a_r)):
                reply = d_a_r[i].xpath("text()").extract()
                replies += delimiter + " ".join(reply)
        post = items.PostItem(heading = heading, description = description, replies = replies)
        self.num_posts += 1
        print("POST No. ",self.num_posts)
        yield post
        
        
                
            

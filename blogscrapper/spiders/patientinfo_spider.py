from __future__ import absolute_import
import scrapy
from .. import items
from blogscrapper.spiders import clean_write
import logging

logging.getLogger('scrapy').propagate = False

class Pinfospider(scrapy.Spider):
    name = "pinfospider"
    num_posts = 0
    txt_file = open("patient_info_blog_posts.txt", "w")

    def start_requests(self):
        logging.getLogger('scrapy').propagate = False
        start_urls = [
            "https://patient.info/forums/discuss/browse/abdominal-disorders-3321",
            "https://patient.info/forums/discuss/browse/anxiety-disorders-70",
            "https://patient.info/forums/discuss/browse/citalopram-2618",
            "https://patient.info/forums/discuss/browse/depression-683",
            "https://patient.info/forums/discuss/browse/hip-replacement-1109",
            "https://patient.info/forums/discuss/browse/irritable-bowel-syndrome-1211",
            "https://patient.info/forums/discuss/browse/knee-problems-1310",
            "https://patient.info/forums/discuss/browse/menopause-1411",
            "https://patient.info/forums/discuss/browse/mirtazapine-2945",
            "https://patient.info/forums/discuss/browse/polymyalgia-rheumatica-and-gca-1708",
        ]
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        links_on_page = response.css("article.post h3.title a::attr(href)").extract()
        for link in links_on_page:
            yield response.follow(url=link, callback=self.parse_blog_page)
        # Look if there is a next page
        next = response.css("a.reply-ctrl-wrap")
        if len(next) == 0:
            pass
        else:
            next_url = next[0].css("::attr(href)").extract()
            yield scrapy.Request(url=next_url[0], callback=self.parse) # Parse that page recursively


    def parse_blog_page(self, response):
        heading = response.css("article.post h1::text").extract_first()
        description = response.xpath("//div[@id='topic']/div/div/div/article/div/p/text()").extract()
        description = " ".join(description)
        replies = response.css("#topic-replies")
        replies = replies.css("div.post-content p::text").extract()
        replies = " ".join(replies)
        profile = items.ProfileItem(heading = heading, description = description, replies = replies)
        string ="\n\n"+ heading+"\n"+description+"\n"+replies+"\n\n"
        clean_write.clean_write(string, self.txt_file)
        yield profile
        self.num_posts += 1
        print("POST NUMBER: ",self.num_posts)

    def spider_closed(self, spider):
        spider.logger.info('Spider closed: %s', spider.name)
        self.txt_file.close()


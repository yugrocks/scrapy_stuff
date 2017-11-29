from __future__ import absolute_import
import scrapy
from .. import items
from blogscrapper.spiders import clean_write
import logging

class medhelpspider(scrapy.Spider):
    name = "medhelpspider"
    total_posts = 0

    def start_requests(self):
        start_urls = [

            # General health:
            #"http://www.medhelp.org/forums/Cold--Flu/show/151",
            #"http://www.medhelp.org/forums/General-Health/show/164",
            #"http://www.medhelp.org/forums/Radiology-/show/905",
            #"http://www.medhelp.org/forums/Adults-with-Special-Needs/show/232",
            #"http://www.medhelp.org/forums/Chronic-Fatigue-Syndrome/show/1209",
            #"http://www.medhelp.org/forums/Disaster-Preparedness/show/100",
            #"http://www.medhelp.org/forums/Emphysema/show/1221",
            #"http://www.medhelp.org/forums/General-Surgery/show/1265",
            #"http://www.medhelp.org/forums/Hemorrhoids/show/1211",
            #"http://www.medhelp.org/forums/Occupational-Health--Safety/show/186",
            #"http://www.medhelp.org/forums/Stress/show/162",
            #"http://www.medhelp.org/forums/Swine-Flu/show/356",
            #"http://www.medhelp.org/forums/Undiagnosed-Symptoms/show/95",
            #"http://www.medhelp.org/forums/Vitamin-D/show/1627",
            #"http://www.medhelp.org/forums/Vitamins--Supplements/show/1206",

            #Healthy Living
            #'http://www.medhelp.org/forums/Bariatric---Weight-Loss-Surgery/show/213',
            #'http://www.medhelp.org/forums/Brain-Health/show/1582',
            #'http://www.medhelp.org/forums/Exercise--Fitness/show/69',
            #'http://www.medhelp.org/forums/Healthy-Cooking/show/280',
            #'http://www.medhelp.org/forums/High-Blood-Pressure---Hypertension/show/1222',
            #'http://www.medhelp.org/forums/Nutrition/show/58',
            #'http://www.medhelp.org/forums/Weight-Loss--Dieting/show/190',
            #'http://www.medhelp.org/forums/Weight-Loss-Alternatives/show/80',
            
            #Womens' health
            #'http://www.medhelp.org/forums/Beauty--Cosmetics/show/40',
            #'http://www.medhelp.org/forums/Birth-Control-Contraception-/show/260',
            #'http://www.medhelp.org/forums/Endometriosis/show/218',
            #'http://www.medhelp.org/forums/Hysterectomy/show/208',
            #'http://www.medhelp.org/forums/Menopause/show/15',
            #'http://www.medhelp.org/forums/Ovarian-Cysts/show/258',
            #'http://www.medhelp.org/forums/Pelvic-Organ-Prolapse-POP/show/1164',
            #'http://www.medhelp.org/forums/Polycystic-Ovarian-Syndrome-PCOS/show/203',
            #'http://www.medhelp.org/forums/Urogynecology/show/743',
            #'http://www.medhelp.org/forums/Womens-Choice/show/1501',
            #'http://www.medhelp.org/forums/Womens-Health/show/81',
            #'http://www.medhelp.org/forums/Womens-Health-Postpartum/show/82',
            #'http://www.medhelp.org/forums/Womens-Health-Postpartum-35/show/249',
            #'http://www.medhelp.org/forums/Womens-Social/show/180',

            #Mens' health
            'http://www.medhelp.org/forums/Mens-Health/show/93',
            ]
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse_page)

    def parse_page(self, response):
        # get the links of posts on page
        links = response.css("div.subject_title a::attr(href)").extract()
        # Then send each post to be processsed
        for link in links:
            yield response.follow(url=link, callback=self.parse_post_page)
        # also check for next page
        navs = response.css("a.page_nav::attr(href)").extract()
        if navs[-1] in navs[0:-1]:
            yield response.follow(url=navs[-1], callback=self.parse_page)

    def parse_post_page(self, response):
        heading = response.css("div.question_title::text").extract_first().strip()
        description_and_replies = response.css("div.post_message")
        delimiter = "__delimiter__"
        if len(description_and_replies) >0:
            description = " ".join(description_and_replies[0].css("::text").extract()).strip()
        replies = ""
        if len(description_and_replies) >1:
            for i in range(1, len(description_and_replies)):
                replies += delimiter+" ".join(description_and_replies[i].css("::text").extract()).strip()
        post = items.PostItem(heading = heading, description = description, replies = replies)
        self.total_posts += 1
        print("POST No. ",self.total_posts)
        yield post






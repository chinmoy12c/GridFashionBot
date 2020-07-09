import json
import scrapy
import logging
from scrapy.crawler import CrawlerProcess

from .spiderInit import SpiderInit

spider_init = SpiderInit()

class DesignSpider(scrapy.Spider):

    name = "designSpider"

    start_urls = [
        'https://www.vogue.co.uk/fashion/fashion-trends',
        'https://www.collezioni.info/en/shows/page/3/',
        'https://patternbank.com/trends',
    ]

    def __init__(self):
        self.data = {}
        self.currentSite = ''
        self.numberOfSections = 10

    def parse(self, response):

        self.currentSite = response.request.url
        self.data[self.currentSite] = {}
        self.data[self.currentSite]["sections"] = {}

        siteId = spider_init.siteRules.get(self.currentSite)["siteId"]
        sectionHead = spider_init.siteRules.get(self.currentSite)["sectionHead"]
        followLinkRule = spider_init.siteRules.get(self.currentSite)["followLink"]
        relativeTo = spider_init.siteRules.get(self.currentSite)["relativeTo"]
        isSrcSet = spider_init.siteRules.get(self.currentSite)["isSrcSet"]
        sectionImageRule = spider_init.siteRules.get(self.currentSite)["sectionImageRule"]
        imgRelativeTo = spider_init.siteRules.get(self.currentSite)["imgRelativeTo"]
        hasSectionImage = spider_init.siteRules.get(self.currentSite)["hasSectionImage"]

        self.data[self.currentSite]["siteId"] = siteId

        for index,section in enumerate(response.css(sectionHead).getall()):
            if (index >= self.numberOfSections):
                return

            section = section.replace("'","")
            self.data[self.currentSite]["sections"][section] = {}
            self.data[self.currentSite]["sections"][section]["sectionImageLink"] = ''
            followLink = response.css(followLinkRule)[index].get()
            followLink = relativeTo + followLink

            self.data[self.currentSite]["sections"][section]["sectionRedirect"] = followLink

            if (hasSectionImage):
                if (isSrcSet):
                    imgUrl = response.css(sectionImageRule)[index].get().split(',')[2].split()[0]
                    imgUrl = imgRelativeTo + imgUrl if imgUrl else ''
                    self.data[self.currentSite]["sections"][section]["sectionImageLink"] = imgUrl
                else:
                    imgUrl = response.css(sectionImageRule)[index].get()
                    imgUrl = imgRelativeTo + imgUrl if imgUrl else ''
                    self.data[self.currentSite]["sections"][section]["sectionImageLink"] = imgUrl

            yield scrapy.Request(followLink, callback = self.subsectionParse, meta = {"section" : section, "site" : self.currentSite})

    def subsectionParse(self, response):
        
        site = response.meta.get("site")
        section = response.meta.get("section")

        subsectionHead = spider_init.siteRules.get(site)["subsectionHead"]
        isSrcSet = spider_init.siteRules.get(site)["isSrcSet"]
        subsectionImgRule = spider_init.siteRules.get(site)["subsectionImgRule"]
        imgRelativeTo = spider_init.siteRules.get(site)["imgRelativeTo"]

        if (self.data[site]["sections"][section]["sectionImageLink"] == ''):
            self.data[site]["sections"][section]["sectionImageLink"] = imgRelativeTo + response.css(subsectionImgRule).get()

        self.data[site]["sections"][section]["subsections"] = {}

        for index,subsection in enumerate(response.css(subsectionHead).getall()):

            if (index >= len(response.css(subsectionImgRule).getall())):
                return

            if (isSrcSet):
                imgUrl = response.css(subsectionImgRule)[index].get().split(',')[2].split()[0]
                imgUrl = imgRelativeTo + imgUrl if imgUrl else ''
                self.data[site]["sections"][section]["subsections"][subsection] = imgUrl
            else:
                imgUrl = response.css(subsectionImgRule)[index].get()
                imgUrl = imgRelativeTo + imgUrl if imgUrl else ''
                self.data[site]["sections"][section]["subsections"][subsection] = imgUrl


process = CrawlerProcess({})
process.crawl(DesignSpider)

def spider_ended(spider, reason):

    if (reason == "finished"):
        spiderData = json.dumps(spider.data)
        logger = logging.getLogger("Out Data")
        logger.info(spiderData + "\nSCRAPEROUT:")
        process.stop()

for crawler in process.crawlers:
    crawler.signals.connect(spider_ended, signal=scrapy.signals.spider_closed)

process.start()
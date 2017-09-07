# -*- coding: utf-8 -*-
import scrapy, re, datetime, logging,os,codecs
from scrapy.http import Request
from paipaidai.items import PaipaidaiItemList

class PaispiderSpider(scrapy.Spider):
    name = "paipaiItems"
    start_urls = [
        'http://invest.ppdai.com/loan/listnew?LoanCategoryId=4',
        #http://invest.ppdai.com/loan/listnew?LoanCategoryId=4&SortType=0&PageIndex=7&MinAmount=0&MaxAmount=0
        'http://invest.ppdai.com/loan/listnew?LoanCategoryId=8',
        'http://invest.ppdai.com/loan/listnew?LoanCategoryId=5'
    ]

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(crawler, settings)

    def read_items(self,filename):
        f = codecs.open(filename, "r+", encoding="utf-8")
        results = f.readlines()
        f.close()
        crawlSet = set()
        for item in results:
            if "item finish" in item:
                id = re.findall("item finish:(\d+)", item)
                if id:
                    crawlSet.add(id[0])
            if  "ERROR: Spider error processing" in item:
                id = re.findall("id=(\d+)",item )
                if id:
                    crawlSet.add(id[0])
        return crawlSet

    def __init__(self, crawler, settings):
        yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        YESTERDAY_LOG_File = "%s.log" % (yesterday)
        self.yesterdayCrawl =set()
        if os.path.exists(YESTERDAY_LOG_File):
            self.yesterdayCrawl = self.read_items(YESTERDAY_LOG_File)
        self.crawler = crawler
        self.yesterdayload = True

    def start_requests(self):
        heasers = {'Host':'invest.ppdai.com','Upgrade-Insecure-Requests':'1'}
        for url in self.start_urls:
            yield Request(url=url,headers=heasers,callback=self.parse)



    def parse(self, response):
        if self.yesterdayload:
            for item in  self.yesterdayCrawl:
                newID = PaipaidaiItemList()
                newID['itemid'] = item
                yield newID
        self.yesterdayload = False
        # 加载此页
        items = response.xpath(".//a[@class='title ell']")
        for item in items:
            href = item.xpath("@href").extract_first()
            item_id = re.findall("id=(\d+)",href)[0]
            newID = PaipaidaiItemList()
            newID['itemid'] = item_id
            yield  newID

        #下一页
        next_page = response.xpath(".//a[@class='nextpage']/@href")
        if next_page:
            nextPage = "http://invest.ppdai.com" + next_page.extract_first()
            yield  Request(url=nextPage, headers={'Host':'invest.ppdai.com'},callback=self.parse)


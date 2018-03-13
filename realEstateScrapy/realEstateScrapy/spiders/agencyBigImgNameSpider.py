# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from realEstateScrapy.items import RealestatescrapyItem,AgencyItem,AgencyBigImgItem
from bs4 import BeautifulSoup


class Agency(CrawlSpider):

    name = "agencyBigImgNameSpider"
    bash_url = 'http://www.realestate.co.nz/rental/page'
    listing_preUrl = 'http://www.realestate.co.nz'
    realEstateList = []
    agencyUrlList=[]
    agencyBigImgList=[]

    #outside page
    def start_requests(self):
        for i in range(1,368):
            url=self.bash_url+str(i)
            yield Request(url,self.parse)

    def parse(self, response):
        selector = Selector(response)
        listingsUrls = selector.xpath('//a[@itemprop="url"]/@href').extract()
        for eachlistingsUrl in listingsUrls:
            eachlistingsUrl = self.listing_preUrl + str(eachlistingsUrl)
            yield Request(eachlistingsUrl, callback=self.parseEachUrl)

    def parseEachUrl(self,response):
        print "-------------------------listing " + str(
            response._url) + " -----------------------------------------------"
        soup = BeautifulSoup(response.text, 'lxml')

        # get agency office id
        divTag = soup.find("div", {"class": "topRight agencyDetailsBox"}).find_all("li")
        li = divTag[0]
        if soup.find("div", {"class": "topRight agencyDetailsBox"}).find_all("li")[0].find("a") is not None:
            classTags = str(soup.find("div", {"class": "topRight agencyDetailsBox"}).find_all("li")[0].find("a")["href"]).split("/")
        else:
            classTags = str(soup.find("div", {"class": "topRight agencyDetailsBox"}).find_all("li")[1].find("a")["href"]).split("/")
        agencyId = classTags[-1]

        div = soup.find("div", {"class": "topRight agencyDetailsBox"})
        if div is not None:
            agencyBigImgName = str(div.find("img")["src"]).split('/')[-1]

        if agencyId not in self.agencyBigImgList:
            item = AgencyBigImgItem()
            item['agencyId'] = agencyId
            item['agencyBigImgName'] = agencyBigImgName
            self.agencyBigImgList.append(agencyId)
            yield item
















# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from realEstateScrapy.items import RealestatescrapyItem,AgencyItem,AgencyBigImgItem,AgencySmallImgItem
from bs4 import BeautifulSoup


class Agency(CrawlSpider):

    name = "agencySmallImgNameSpider"
    bash_url = 'http://www.realestate.co.nz/rental/page'
    listing_preUrl = 'http://www.realestate.co.nz'
    realEstateList = []
    agencyIdList=[]


    #outside page
    def start_requests(self):
        for i in range(1,368):
            url=self.bash_url+str(i)
            yield Request(url,self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        listdivs = soup.find_all("div", {"class": "listDetails"})
        for eachDiv in listdivs:
            div=eachDiv.find("div",{"class":"agencyLogosmall"})
            agencyId=str(div.find("a")["href"]).split("/")[-1]

        for each in listdivs:
            smallImgName=str(each.find("img")["src"]).split("/")[-1]
        if agencyId not in self.agencyIdList:
            item = AgencySmallImgItem()
            item['agencyId'] = agencyId
            item['agencySmallImgName'] = smallImgName
            self.agencyIdList.append(agencyId)
            yield item


















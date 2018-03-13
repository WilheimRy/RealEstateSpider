# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from realEstateScrapy.items import RealestatescrapyItem,AgencyItem,AgentItem
from bs4 import BeautifulSoup


class Agent(CrawlSpider):
    name = "agentSpider"
    bash_url = 'http://www.realestate.co.nz/rental/page'
    listing_preUrl = 'http://www.realestate.co.nz'
    agentIdList=[]

    #outside page
    def start_requests(self):
        for i in range(1,368):
            url=self.bash_url+str(i)
            yield Request(url,self.parse)

    #get lisitng's urls
    def parse(self, response):
        selector = Selector(response)
        listingsUrls = selector.xpath('//a[@itemprop="url"]/@href').extract()
        for eachlistingsUrl in listingsUrls:
            eachlistingsUrl = self.listing_preUrl + str(eachlistingsUrl)
            yield Request(eachlistingsUrl, callback=self.parseEachUrl)

    # listing's url
    def parseEachUrl(self,response):
        print "-------------------------listing " + str(response._url) + " -----------------------------------------------"
        soup = BeautifulSoup(response.text, 'lxml')

        # get agent info
        if soup.find("h5", {"class": "fn agent"}) is not None:
            agentId = str(soup.find("h5", {"class": "fn agent"}).find("a")["href"]).split("/")[-1]
            if agentId not in self.agentIdList:
                agentName=str(soup.find("h5", {"class": "fn agent"}).find("a").string)
                lis = soup.find("h5", {"class": "fn agent"}).find_next_siblings("ul")[0].find_all("li",{"class":"tel"})
                if lis[0] is not None:
                    if len(lis)==1:
                        agentWorkingPhone=str(lis[0].contents[1])
                        agentPhone = "None"
                    elif len(lis)>1:
                        agentPhone = str(lis[0].contents[1])
                        agentWorkingPhone = str(lis[1].contents[1])
                    if soup.find("div", {"class": "agentImageSmall photo"}).find("img") is not None:
                        agentPhotoUrl=str(soup.find("div", {"class": "agentImageSmall photo"}).find("img")["src"])
                        agentPhotoName=agentPhotoUrl.split('/')[-2]+"-"+agentPhotoUrl.split('/')[-1]
                    else:
                        agentPhotoName="None"
                    item=AgentItem()
                    item['agentId']=agentId
                    item['agentName']=agentName
                    item['agentPhone']=agentPhone
                    item['agentWorkingPhone']=agentWorkingPhone
                    item['agentPhotoName']=agentPhotoName
                    self.agentIdList.append(agentId)
                    yield item


























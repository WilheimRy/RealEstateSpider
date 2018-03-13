# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from realEstateScrapy.items import RealestatescrapyItem,AgencyItem
from bs4 import BeautifulSoup


class Agency(CrawlSpider):

    name = "agencySpider"
    bash_url = 'http://www.realestate.co.nz/rental/page'
    listing_preUrl = 'http://www.realestate.co.nz'
    realEstateList = []
    agencyUrlList=[]
    agencySmallImgName=''
    agencyBigImgName=''

    #outside page
    def start_requests(self):
        for i in range(1,368):
            url=self.bash_url+str(i)
            yield Request(url,self.parse)

    #outside page
    def parse(self, response):
        selector = Selector(response)
        listingsUrls = selector.xpath('//a[@itemprop="url"]/@href').extract()

        # get agency small img name
        soup = BeautifulSoup(response.text, 'lxml')
        listdivs = soup.find_all("div", {"class": "listDetails"})
        for each in listdivs:
            self.agencySmallImgName=str(each.find("img")["src"]).split("/")[-1]


        for eachlistingsUrl in listingsUrls:
            eachlistingsUrl = self.listing_preUrl + str(eachlistingsUrl)
            yield Request(eachlistingsUrl, callback=self.parseEachUrl)

    # listing's page
    def parseEachUrl(self,response):

        soup = BeautifulSoup(response.text, 'lxml')

        #get agency's url
        if soup.find("div", {"class": "topRight agencyDetailsBox"}).find_all("li")[0].find("b") is not None:
            agencyPageUrl=self.listing_preUrl+str(soup.find("div", {"class": "topRight agencyDetailsBox"}).find_all("li")[1].find("a")["href"])
        else:
            agencyPageUrl = self.listing_preUrl + str(soup.find("div", {"class": "topRight agencyDetailsBox"}).find_all("li")[0].find("a")["href"])

        #agencyBigImgName
        div = soup.find("div", {"class": "topRight agencyDetailsBox"})
        if div is not None:
            self.agencyBigImgName = str(div.find("img")["src"]).split('/')[-1]

        #visit agency's page
        if agencyPageUrl not in self.agencyUrlList:
            yield Request(agencyPageUrl,callback=self.getAgencyDetail)

    #agency's page
    def getAgencyDetail(self,response):

        # save pageUrl to list
        if response._url not in self.agencyUrlList:
            self.agencyUrlList.append(response._url)
        soup = BeautifulSoup(response.text, 'lxml')
        agencyId=str(response._url).split("/")[-1]
        officeDetails=soup.find("div",{"id":"office-details"})

        # agencytitle, agencyAddress, agencyPhone
        agencytitle=officeDetails.find("h2").string

        if "," in str(officeDetails.find_all("li")[0].string):
            agencyAddress = str(officeDetails.find_all("li")[0].string)
        else:
            agencyAddress="None"

        if "Phone" in str(officeDetails.find_all("li")[1].string):
            agencyPhone = str(officeDetails.find_all("li")[1].string).replace("Phone:", "").strip()
        else:
            agencyPhone="None"


        # agencyWebsite
        if "Rental" in str(officeDetails.find_all("li")[2].string):
            agencyRentalPhone=str(officeDetails.find_all("li")[2].string).replace("Rental Enquiries:","").strip()
            if "website" in str(officeDetails.find_all("li")[3].find("a")):
                agencyWebsite=str(officeDetails.find_all("li")[3].find("a")["href"])
            else:
                agencyWebsite = "None"
        else:
            agencyRentalPhone="None"
            if "website" in str(officeDetails.find_all("li")[2].find("a")):
                agencyWebsite = str(officeDetails.find_all("li")[2].find("a")["href"])
            else:
                agencyWebsite="None"

        item=AgencyItem()
        item['agencyId']=agencyId
        item['agencytitle']=agencytitle
        item['agencyAddress']=agencyAddress
        item['agencyPhone']=agencyPhone
        item['agencyRentalPhone']=agencyRentalPhone
        item['agencyWebsite'] = agencyWebsite
        item['agencySmallImgName']=self.agencySmallImgName
        item['agencyBigImgName']=self.agencyBigImgName
        yield item















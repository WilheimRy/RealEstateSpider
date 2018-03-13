# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from realEstateScrapy.items import RealestatescrapyItem
from bs4 import BeautifulSoup
import re

#time lib
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from datetime import datetime


class RealEstate(CrawlSpider):

    name="realestateSpider"
    bash_url = 'http://www.realestate.co.nz/rental/page'
    listing_preUrl='http://www.realestate.co.nz'
    realEstateList=[]

    def start_requests(self):
        for i in range(1,381):
            url=self.bash_url+str(i)
            yield Request(url,self.parse)

    def parse(self, response):
        selector=Selector(response)
        listingsUrls=selector.xpath('//a[@itemprop="url"]/@href').extract()
        for eachlistingsUrl in listingsUrls:
            print "--------------------------------------------- page "+str(eachlistingsUrl)+" ------------------------------------------"
            eachlistingsUrl=self.listing_preUrl+str(eachlistingsUrl)
            yield Request(eachlistingsUrl,callback=self.parseEachUrl)

    def parseEachUrl(self,response):
        print "-------------------------listing "+str(response._url)+" -----------------------------------------------"
        soup=BeautifulSoup(response.text,'lxml')
        title=str(soup.find("h1",{"itemprop":"name"}).string).strip()
        price=str(soup.find("h1",{"itemprop":"name"}).find_next_siblings("h2")[0].string)
        weeklyPrice=price.replace("$","").replace(" per week","").replace("Plus GST (if any)","").replace(",","").strip()
        addressList=soup.find_all("li",{"itemprop":"itemListElement"})
        region=str(addressList[1].find("span",{"itemprop":"name"}).string).strip()
        district=str(addressList[2].find("span",{"itemprop":"name"}).string).strip()
        suburb=str(addressList[3].find("span",{"itemprop":"name"}).string).strip()
        address=str(addressList[4].find("span",{"itemprop":"name"}).string).strip()
        bedroomCount=str(soup.find("ul",{"class":"leftList"}).find("li",{"class":"bedrooms"}).string).replace("Bedroom","").replace("s","").strip()
        if soup.find("ul",{"class":"leftList"}).find("li",{"class":"carParks"}) is not None:
            carparksCount = str(soup.find("ul", {"class": "leftList"}).find("li", {"class": "carParks"}).string).replace("Car Space","").replace("s", "").strip()
        else:
            carparksCount=0

        bathroomCount=str(soup.find("ul",{"class":"rightList"}).find("li",{"class":"bathrooms"}).string).replace("Bathroom","").replace("s","").strip()

        #propertyIntroHtml=str(soup.find("div",{"class":"description detailsPage"})).strip()
        #listingsId
        listingsId=str(response._url).split("/")[-1]

        #get agency office id
        divTag=soup.find("div",{"class":"topRight agencyDetailsBox"}).find_all("li")
        li=divTag[0]
        if soup.find("div",{"class":"topRight agencyDetailsBox"}).find_all("li")[0].find("a") is not None:
            classTags = str(soup.find("div", {"class": "topRight agencyDetailsBox"}).find_all("li")[0].find("a")["href"]).split("/")
        else:
            classTags = str(soup.find("div", {"class": "topRight agencyDetailsBox"}).find_all("li")[1].find("a")["href"]).split("/")
        agencyId=classTags[-1]

        #get agent id
        if soup.find("h5",{"class":"fn agent"}) is not None:
            agentId = str(soup.find("h5", {"class": "fn agent"}).find("a")["href"]).split("/")[-1]
        else:
            agentId=0

        # get first img name
        # get images urls -> get image names
        script = str(soup.find("div", {"class": "ImageGalleryViewPane"}).find("script").string)
        images = re.findall('http://(.*?).jpg', script, re.S)
        firstImgUrl = ['http://' + s + '.jpg' for s in images][0]
        firstImgName = firstImgUrl.split('/')[-2]+'/'+firstImgUrl.split('/')[-1]



        #assign values for item
        item=RealestatescrapyItem()

        #infoList.extend((title,weeklyPrice,region,district,suburb,address,bedroomCount,carparksCount,bathroomCount,propertyIntroHtml,listingsId,agencyId,agentId))

        item['listingsId'] = listingsId
        item['title']=title
        item['weeklyPrice']=weeklyPrice
        item['region']=region
        item['district']=district
        item['suburb']=suburb
        item['address']=address
        item['bedroomCount']=bedroomCount
        item['carparksCount']=carparksCount
        item['bathroomCount']=bathroomCount
        #item['propertyIntroHtml']=propertyIntroHtml
        item['agencyId']=agencyId
        item['agentId']=agentId
        item['firstImgName']=firstImgName
        yield item





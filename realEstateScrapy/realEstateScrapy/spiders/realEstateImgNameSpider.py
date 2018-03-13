# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from realEstateScrapy.items import RealestatescrapyItem,RealEstateImgNameItem
from bs4 import BeautifulSoup
import re

#time lib
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from datetime import datetime


class RealEstate(CrawlSpider):

    name="realestateImgNameSpider"
    bash_url = 'http://www.realestate.co.nz/rental/page'
    listing_preUrl='http://www.realestate.co.nz'
    realEstateList=[]
    realEstateImgNameId=1


    def start_requests(self):
        for i in range(1,5):
            url=self.bash_url+str(i)
            yield Request(url,self.parse)

    def parse(self, response):
        selector=Selector(response)
        listingsUrls=selector.xpath('//a[@itemprop="url"]/@href').extract()
        for eachlistingsUrl in listingsUrls:
            #print "--------------------------------------------- page "+str(eachlistingsUrl)+" ------------------------------------------"
            eachlistingsUrl=self.listing_preUrl+str(eachlistingsUrl)
            yield Request(eachlistingsUrl,callback=self.parseEachUrl)

    def parseEachUrl(self,response):

        soup = BeautifulSoup(response.text, 'lxml')
        script = str(soup.find("div", {"class": "ImageGalleryViewPane"}).find("script").string)

        # get images urls -> get image names
        images = re.findall('http://(.*?).jpg', script, re.S)
        imagesUrls = ['http://' + s + '.jpg' for s in images]

        # listingsId
        listingsId = str(response._url).split("/")[-1]

        for imgUrl in imagesUrls:
            item=RealEstateImgNameItem()
            item['realEstateImgNameId']=self.realEstateImgNameId
            item['realEstateImgName']=str(imgUrl).split('/')[-2]+"/"+str(imgUrl).split('/')[-1]
            item['listingsId']=listingsId
            self.realEstateImgNameId=self.realEstateImgNameId+1
            yield item






# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field


class RealestatescrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title=Field()
    weeklyPrice=Field()
    region=Field()
    district=Field()
    suburb=Field()
    address=Field()
    bedroomCount=Field()
    carparksCount=Field()
    bathroomCount=Field()
    propertyIntroHtml=Field()
    listingsId=Field()
    agencyId=Field()
    agentId=Field()
    firstImgName=Field()


class AgencyItem(Item):
    agencyId=Field()
    agencytitle=Field()
    agencyAddress=Field()
    agencyPhone=Field()
    agencyRentalPhone=Field()
    agencyWebsite=Field()
    agencySmallImgName=Field()
    agencyBigImgName=Field()

class AgentItem(Item):
    agentId=Field()
    agentName=Field()
    agentPhone=Field()
    agentWorkingPhone=Field()
    agentPhotoName=Field()

class AgencyBigImgItem(Item):
    agencyId=Field()
    agencyBigImgName=Field()

class AgencySmallImgItem(Item):
    agencyId=Field()
    agencySmallImgName=Field()

class RealEstateImgNameItem(Item):
    realEstateImgNameId=Field()
    realEstateImgName=Field()
    listingsId=Field()




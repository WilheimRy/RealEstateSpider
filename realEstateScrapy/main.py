from scrapy import cmdline

# realestate spider
cmdline.execute("scrapy crawl realestateSpider -o realEstateOutput.csv -t csv -a CSV_DELIMITER='|'".split())

# agency spider
#cmdline.execute("scrapy crawl agencySpider -o agencyOutput.csv -t csv -a CSV_DELIMITER='|'".split())

# agent spider
#cmdline.execute("scrapy crawl agentSpider -o agentOutput.csv -t csv -a CSV_DELIMITER='|'".split())

#agency big img Name spider
#cmdline.execute("scrapy crawl agencyBigImgNameSpider -o agencyBigImgNameOutput.csv -t csv -a CSV_DELIMITER='|'".split())


#agency small img Name spider
#cmdline.execute("scrapy crawl agencySmallImgNameSpider -o agencySmallImgNameOutput.csv -t csv -a CSV_DELIMITER='|'".split())

#real Estate img Name spider
#cmdline.execute("scrapy crawl realestateImgNameSpider -o realestateImgNameOutput.csv -t csv -a CSV_DELIMITER='|'".split())



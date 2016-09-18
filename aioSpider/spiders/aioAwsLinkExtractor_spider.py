import scrapy

class aioAwsUrlItem(scrapy.Item):
    urlsToScrape = scrapy.Field()

class aioAwsLinkExtractorSpider (scrapy.Spider):
    name = "aioAwsLinkExtractor"
    allowed_domains = ["aiotestking.com"]
    start_urls = ['http://www.aiotestking.com/amazon/category/exam-aws-saa-aws-certified-solutions-architect-associate/page/%d' %(n) for n in range(2, 43)]
    start_urls.append('http://www.aiotestking.com/amazon/category/exam-aws-saa-aws-certified-solutions-architect-associate/')

    def parse(self, response):
        awsSaaUrlCollection = aioAwsUrlItem()
        
        # Extract the URLs to the post titles from the HTML Content
        urls = response.css("h2.title > a::attr(href)").extract()
        
        # Loops through the URLs and create a dictionary object with an ID and Url Text and push the item to scrapy to write
        for url in urls:
            awsSaaUrlCollection['urlsToScrape'] = url
            yield awsSaaUrlCollection

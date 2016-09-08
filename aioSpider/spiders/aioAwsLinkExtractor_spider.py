import scrapy

class aioAwsUrlItem(scrapy.Item):
    urlData = scrapy.Field()

class aioAwsLinkExtractorSpider (scrapy.Spider):
    name = "aioAwsLinkExtractor"
    allowed_domains = ["aiotestking.com"]
    start_urls = ['http://www.aiotestking.com/amazon/category/exam-aws-saa-aws-certified-solutions-architect-associate/page/%d' %(n) for n in range(2, 42)]

    def parse(self, response):
        item = aioAwsUrlItem()
		
		# Extract the URLs to the post titles from the HTML Content
        urls = response.css("h2.title > a::attr(href)").extract()
        for url in urls:
            item['urlData'] = url
            yield item
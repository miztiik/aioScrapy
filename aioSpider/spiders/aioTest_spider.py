import scrapy

class aioAwsSpider (scrapy.Spider):
    name = "aioAwsSpider"
    allowed_domains = ["aiotestking.com"]
    start_urls = [
        "http://www.aiotestking.com/amazon/which-of-the-following-options-would-enable-an-equivalent-experience-for-users-on-both-continents/",
        "http://www.aiotestking.com/amazon/which-of-the-following-are-use-cases-for-amazon-dynamodb/"
    ]

    def parse(self, response):
        qaData = response.css("#content > p::text").extract()
        print '\t\t---------BEGIN POST-----'
        print qaData, "\t\n\n"
        for sel in response.css("#commentlist > li"):
            qComments = sel.css("p::text").extract()
            qCommentAuthor = sel.css("cite::text").extract()
            print qCommentAuthor, qComments
        print '\t\t---------END POST------- \n\n\n\n'
            
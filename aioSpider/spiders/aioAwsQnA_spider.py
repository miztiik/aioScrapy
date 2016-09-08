import scrapy

class aioAwsQnAItem(scrapy.Item):
    question = scrapy.Field()
    answerChoices = scrapy.Field()
    correctChoices = scrapy.Field()

class aioAwsQnASpider (scrapy.Spider):
    name = "aioAwsQnASpider"
    allowed_domains = ["aiotestking.com"]
    start_urls = [
        "http://www.aiotestking.com/amazon/which-of-the-following-options-would-enable-an-equivalent-experience-for-users-on-both-continents/",
        "http://www.aiotestking.com/amazon/which-methods-will-enable-the-branch-office-to-access-their-data/",
        "http://www.aiotestking.com/amazon/which-two-methods-increases-the-fault-tolerance-of-the-connection-to-vpc-1/"
    ]

    def parse(self, response):
        #qaData = response.css("#content p").xpath('.//text()').extract()
        qaData = response.css("#content > p")
        qItems = []
        qItems = aioAwsQnAItem()
        
        tempList=[]
        tempList=qaData[0].css('::text').extract()
        qItems['question'] = " ".join(tempList)
        
        # Create a two pair(answerID & text) from the remaining to get the answers text
        # Run a join to ensure any long answer text is not broken and unnecessary spaces are removed
        answerText=[]
        for i in range(1,len(qaData),1):
            qaData[i]=qaData[i].css("::text").extract()
            answerText.append("".join(qaData[i]))
       
        # Assing to scrapy Item
        qItems['answerChoices'] = answerText
        
        qItems['correctChoices']=response.css("#content > p").re(r'<p>(.*).<br><font')
        print '\t\t---------BEGIN POST-----'
        print qItems
        yield qItems
        print '\t\t---------END POST------- \n\n\n\n'

import scrapy

class aioAwsQnAItem(scrapy.Item):
    question = scrapy.Field()
    options = scrapy.Field()
    answers = scrapy.Field()
    comments = scrapy.Field()

class aioAwsQnASpider (scrapy.Spider):
    name = "aioAwsQnASpider"
    allowed_domains = ["aiotestking.com"]
    
    # Pass Scrapy Spider a list of URLs to crawl via .txt file
    # http://stackoverflow.com/questions/17307718/pass-scrapy-spider-a-list-of-urls-to-crawl-via-txt-file
    # Pass through strip to remove any trailing newline characters
    def __init__(self, filename=None):
        if filename:
            with open(filename, 'r') as f:
                self.start_urls = [url.strip() for url in f.readlines()]

    def parse(self, response):
        
        # QUESTION - Scraping
        qaData = response.css("#content > p")
        qItems = []
        qItems = aioAwsQnAItem()
        
        tempList = []
        tempList = qaData[0].css('::text').extract()
        qItems['question'] = " ".join(tempList)

        # CHOICES & ANSWERS - Scraping        
        # Create a two pair(Choice ID & Choice Text) from the remaining to get the answers text
        # Run a join to ensure any long answer text is not broken and unnecessary spaces are removed
        qItems['answers'] = qaData.re(r'<p>(.*).<br><font')		

        tempList = []
        for i in range(1,len(qaData),1):
            qaData[i] = qaData[i].css("::text").extract()
            # Create a list with ["choiceID", "ChoiceText"] by join the text and leaving out the first element
			# Store only if we match anything by checking if the list is empty or not
            if qaData[i]:
                choiceID = qaData[i][0]
                choiceText = "".join(qaData[i][1:])
                tempList.append( [ choiceID , choiceText ] )
        qItems['options'] = tempList

        # COMMENTS - Scraping
        tempList = []
        for sel in response.css("#commentlist > li"):
            qComments = sel.css("p::text").extract()
            qCommentAuthor = sel.css("cite::text").extract()
            print qCommentAuthor, qComments
            tempList.append([qCommentAuthor, qComments])
        qItems['comments'] = tempList        

        # Return the JSON to be writtent to file
        yield qItems
        
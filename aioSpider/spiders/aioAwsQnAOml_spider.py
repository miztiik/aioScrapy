import scrapy
from lxml import etree

class aioAwsQnAOmlSpider (scrapy.Spider):
    name = "aioAwsQnAOmlSpider"
    allowed_domains = ["aiotestking.com"]
    
    # Pass Scrapy Spider a list of URLs to crawl via .txt file
    # http://stackoverflow.com/questions/17307718/pass-scrapy-spider-a-list-of-urls-to-crawl-via-txt-file
    # Pass through strip to remove any trailing newline characters
    start_urls = [ "http://www.aiotestking.com/amazon/which-of-the-following-options-would-you-consider-for-configuring-the-web-server-infrastructure/",
                   "http://www.aiotestking.com/amazon/which-metric-should-i-be-checking-to-ensure-that-your-db-instance-has-enough-free-storage-space/"
                 ]

    def writeToFile(self, problem):
        with open('aabbcc', 'a') as f:
            f.write(etree.tostring(problem, pretty_print=True))
        return

    def parse(self, response):
        
        # QUESTION - Scraping
        qaData = response.css("#content > p")

        # Build the custom XML
        problem = etree.Element('problem')
        p =  etree.SubElement(problem, "p")
        p.text =  " ".join(qaData[0].css('::text').extract())
		
        multiplechoiceresponse =  etree.SubElement(problem, "multiplechoiceresponse")
        choicegroup =  etree.SubElement(multiplechoiceresponse, "choicegroup")
        # Lets set the attributes for the choicegroup tag
        choicegroup.set("type", "MultipleChoice")
        choicegroup.set("shuffle", "True")

        for i in range(1,len(qaData),1):
            chkAns = qaData[i].css("font::text").extract()
            # Check if this is wrong choice
            if not chkAns:
                choice =  etree.SubElement(choicegroup, "choice")
                choice.set("correct", "False")
                chkAns = qaData[i].css("::text").extract()
                # We wil leave out the first match as that has Option ID (say A or B or C or D) 
                # Strip to remove any leading or trailing white spaces
                choice.text = ''.join(chkAns[1:]).strip()
            elif chkAns:
                choice =  etree.SubElement(choicegroup, "choice")
                choice.set("correct", "True")
                choice.text = ''.join(chkAns).strip()


        # print etree.tostring(problem, pretty_print=True)
        self.writeToFile(problem)
        # Return the JSON to be writtent to file
        return
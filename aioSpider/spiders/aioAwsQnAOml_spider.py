import scrapy
from lxml import etree

class aioAwsQnAOmlSpider (scrapy.Spider):
    name = "aioAwsQnAOmlSpider"
    allowed_domains = ["aiotestking.com"]
    
    # Pass Scrapy Spider a list of URLs to crawl via .txt file
    # http://stackoverflow.com/questions/17307718/pass-scrapy-spider-a-list-of-urls-to-crawl-via-txt-file
    # Pass through strip to remove any trailing newline characters
    def __init__(self, filename=None):
        if filename:
            self.outputFilename = filename
            with open(filename, 'r') as f:
                self.start_urls = [url.strip() for url in f.readlines()]

    def parse(self, response):
        
        qaDataDict = {}
        # QUESTION - Scraping
        qaData = response.css("#content > p")
        qaDataDict['p'] = " ".join(qaData[0].css('::text').extract())

        # Questions can be of two types "choiceresponse" or "multiplechoiceresponse"
        multiResponse = qaData.css("font").extract()
        if len(multiResponse) > 1:
            # Set the type of question, so we can group them while building the OML
            qaDataDict['questionType'] = "choiceresponse"
        elif len(multiResponse) == 1 and len(multiResponse) != 0:
            qaDataDict['questionType'] = "multiplechoiceresponse"

        tmpList = []
        for i in range(1,len(qaData),1):
            chkAns = qaData[i].css("font::text").extract()
            # Check if this is wrong choice
            if not chkAns:
                chkAns = qaData[i].css("::text").extract()
                tmpList.append([False,''.join(chkAns[1:]).strip()])
            elif chkAns:
                chkAns = qaData[i].css("::text").extract()
                tmpList.append([True,''.join(chkAns[1:]).strip()])
        qaDataDict['choice'] = tmpList

        self.buildOml(qaDataDict)
        return

    # Custion method to build the XML with attributes and text scrapped
    def buildOml(self,qaDataDict):
        # Build the custom XML
        problem = etree.Element('problem')
        p =  etree.SubElement(problem, "p")
        p.text = qaDataDict['p']
        
        if qaDataDict['questionType'] == "choiceresponse":
            choiceresponse = etree.SubElement(problem, "choiceresponse")
            checkboxgroup = etree.SubElement(choiceresponse, "checkboxgroup")
            choiceresponse.set("shuffle", "True")

            # Lets build the choices with answer text
            for item in qaDataDict['choice']:
                if item[0]==True:
                    choice =  etree.SubElement(choiceresponse, "choice")
                    choice.set("correct", "True")
                    choice.text = item[1]
                if item[0]==False:
                    choice =  etree.SubElement(choiceresponse, "choice")
                    choice.set("correct", "False")
                    choice.text = item[1]

        elif qaDataDict['questionType'] == "multiplechoiceresponse":
            multiplechoiceresponse =  etree.SubElement(problem, "multiplechoiceresponse")
            choicegroup =  etree.SubElement(multiplechoiceresponse, "choicegroup")
            # Lets set the attributes for the choicegroup tag
            choicegroup.set("type", "MultipleChoice")
            choicegroup.set("shuffle", "True")		

            # Lets build the choices with answer text
            for item in qaDataDict['choice']:
                if item[0]==True:
                    choice =  etree.SubElement(choicegroup, "choice")
                    choice.set("correct", "True")
                    choice.text = item[1]
                if item[0]==False:
                    choice =  etree.SubElement(choicegroup, "choice")
                    choice.set("correct", "False")
                    choice.text = item[1]

        self.writeToFile(problem)
        return

    # Method to write the XML to file, 
    # The outputFilename(Global) is initialized in the beginning and matching with the urlList filename
    def writeToFile(self, problem):
        with open('%s.xml' % self.outputFilename, 'a') as f:
            f.write(etree.tostring(problem, encoding='utf-8', pretty_print=True))
        return


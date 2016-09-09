# Scraping web content using Scrapy



# Collect the URLs to scrape
```sh
scrapy crawl aioAwsLinkExtractor -t csv -o allAwsSaaUrlCollections.csv
```
### Split the URLs file
```sh
split -l 50 allAwsSaaUrlCollections.csv allAwsSaaUrlCollection
```

# Scrapy the URLs
```sh
scrapy crawl aioAwsQnASpider -a filename=allAwsSaaUrlCollectionaa -t json -o allAwsSaaUrlCollectiona.json
```
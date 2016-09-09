# Using Scrapy to collect web data for analysis
------------------

# Install scrapy
###### The following steps will help you to install scrapy in CentOS 7
```sh
yum install -y epel-release \
               deltarpm

yum install -y gcc \
               libffi-devel \
               python-devel \
               openssl-devel \
               libxslt-devel \
               libxml++-devel \
               libxml2-devel \
               python-pip
```

### Install Scrapy using Python pop
```sh
pip install lxml
pip install scrapy
```


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
scrapy crawl aioAwsQnASpider -a filename=allAwsSaaUrlCollectionaa -t json -o awsSaaQnACommentsA.json
```
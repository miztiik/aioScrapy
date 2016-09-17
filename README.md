# Using Scrapy to collect web data for analysis


# Install scrapy
###### The following dependencies need to be installed in CentOS 7
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

### Use `pip` to install Scrapy
```sh
pip install lxml
pip install scrapy
```


## Collect the URLs to scrape
```sh
scrapy crawl aioAwsLinkExtractor -t csv -o allAwsSaaUrlCollections.csv
```
### Split the URLs file
```sh
split -l 50 allAwsSaaUrlCollections.csv allAwsSaaUrlCollection
```

## Scrapy the URLs
```sh
scrapy crawl aioAwsQnASpider -a filename=allAwsSaaUrlCollectionaa -t json -o awsSaaQnACommentsA.json
```
or, If you want XML as your output format, (note i have written custom as the pipelines XML wouldn't be flexible for Item attributes)
```sh
scrapy crawl aioAwsQnAOmlSpider -a filename=example
```
### Output
If you open the `awsSaaQnACommentsA.json` file, one of the elements should look like this;
```json
[
  {
    "question": "Fill in the blanks: _________ let you categorize your EC2 resources in different ways, for example, by purpose, owner, or environment.",
    "options": [
      [ "A.", " wildcards" ],
      [ "B.", " pointers" ],
      [ "C.", " Tags" ],
      [ "D.", " special filters" ]
    ],
    "answers": [ "C" ],
    "comments": [
      [ [ "Chef" ], [ "Tags." ] ]
    ]
  }
]
```
If you are using the OML Spider, you will be seeing something like this,
```xml
<problem>
  <p>In the Amazon cloudwatch, which metric should I be checking to ensure that your DB Instance has enough free storage space?</p>
  <choiceresponse shuffle="True">
    <checkboxgroup/>
    <choice correct="False">FreeStorage</choice>
    <choice correct="True">FreeStorageSpace</choice>
    <choice correct="False">FreeStorageVolume</choice>
    <choice correct="False">FreeDBStorageSpace</choice>
  </choiceresponse>
</problem>
```

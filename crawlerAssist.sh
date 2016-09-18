#!/bin/bash
set -x

## Collect the URLs to scrape
scrapy crawl aioAwsLinkExtractor -t csv -o allAwsSaaUrlCollections.csv

### Remove the first line
sed -i '1d' "allAwsSaaUrlCollections.csv"

# Create the directories for Input & Outputs
mkdir -p ./awsSaaContent/awsSaaUrlInput
mkdir -p ./awsSaaContent/awsSaaXMLOutput

## Split the URLs file
split -l 30 -d --additional-suffix=.txt  allAwsSaaUrlCollections.csv ./awsSaaContent/awsSaaUrlInput/urlList
mv allAwsSaaUrlCollections.csv ./awsSaaContent/awsSaaUrlInput/

# Get the current working directory
# currDir=${PWD##*/}
cd ./awsSaaContent/awsSaaUrlInput

# Get all the files to be processed into an bash Array
declare -a urlLists=( *.txt )

## now loop through the above array
for i in "${urlLists[@]}"
do
   scrapy crawl aioAwsQnAOmlSpider -a filename="$i" >> crawlerOutput.xml 2>&1
done

# Move all the output file to its own destination
# (one of the dirty hacks to name the output file also as xml)
mv *.xml ./../awsSaaXMLOutput/

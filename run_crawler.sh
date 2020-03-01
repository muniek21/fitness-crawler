#!/bin/bash

while read -r line
  do
    scrapy runspider scraper.py -a"$line"
  done < fitnessClubUrls
#!/bin/bash

while read -r line
  do
    scrapy runspider scraper.py -a fitness_club="$line"
  done < fitnessUrls.txt

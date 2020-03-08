#!/bin/bash

while read line
  do
    scrapy runspider scraper.py -a fitness_club="$line"
  done < fitnessClubUrls
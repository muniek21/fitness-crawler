import scrapy
from enum import Enum
import sys

class Day(Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5 
    SATURDAY = 6
    SUNDAY = 7

class FitnessClass:
    day = Day.MONDAY
    hour = ''
    name = ''
    place = ''

    def __init__(self, day, hour, name, place):
        self.day = day
        self.hour = hour
        self.name = name
        self.place = place
    
    def print_class(self):
        print(self.name + " " + self.day.name + " " + self.hour + " " + self.place)

class FitnessClassScraper(scrapy.Spider):
    name="fitness_class_spider"
    start_urls=[ 'https://metropolitechnika.zdrofit.pl/kalendarz-zajec']

    @staticmethod
    def parse(response):
        print(sys.argv[1])
        fitness_classes = []

        rows = response.css('table.calendar_table tr')

        for row in rows[1:]:
            hour = row.css('.hour ::text').extract_first().strip()

            for num, cell in enumerate(row.css('td')):
                if num == 0:
                    continue
                cell_content = cell.css('.event_name::text').extract_first()
                if cell_content is None:
                    continue
                else:
                    fitness_classes.append(FitnessClass(Day(num), hour, cell_content, 'POLITECHNIKA'))

        for fitness_class in fitness_classes:
            fitness_class.print_class()
       




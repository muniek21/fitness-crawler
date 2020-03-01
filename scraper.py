import scrapy
from enum import Enum

class Day(Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDENSDAY = 3
    THURSDAY = 4
    FRIDAY = 5 
    SATURDAY = 6
    SUNDAY = 7

class FitnessClub(Enum):
    POLITECHNIKA = 1
    GALERIA_MOKOTOW = 2
    MARYNARSKA = 3
    KONSTRUTKTORSKA = 4
    METRO_WILANOWSKA = 5
    EUROPLEX = 6
    PLAC_UNII = 7
    ALEJE_JEROZOLIMSKIE = 8

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
    
    def printClass(self): 
        print(self.name + " " + self.day.name + " " + self.hour + " " + self.place)

class FitnessClassScraper(scrapy.Spider):
    name="fitness_class_spider"
    start_urls=[ 'https://metropolitechnika.zdrofit.pl/kalendarz-zajec']

    def parse(self, response):
        fitness_classes = []

        rows = response.css('table.calendar_table tr')

        for row in rows[1:]:
            hour = row.css('.hour ::text').extract_first().strip()

            for num, cell in enumerate(row.css('td')):
                class_name = ''
                if num == 0:
                    continue
                if (cell.css('.event_name::text').extract_first() is None):
                    # class_name = 'NO_CLASS'
                    continue
                else:
                    class_name = cell.css('.event_name::text').extract_first()

                fitness_classes.append(FitnessClass(Day(num), hour, class_name, FitnessClub.POLITECHNIKA.name))    

        for fitness_class in fitness_classes:
            fitness_class.printClass()       
       




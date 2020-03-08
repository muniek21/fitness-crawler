import scrapy
from enum import Enum
from datetime import datetime, timedelta
import sqlite3


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
    date = ''

    def __init__(self, day, hour, name, place, date):
        self.day = day
        self.hour = hour
        self.name = name
        self.place = place
        self.date = date

    def print_class(self):
        print(self.name + " " + self.day.name + " " + self.hour + " " + self.place + " " + str(self.date))


class FitnessClassScraper(scrapy.Spider):
    name = "fitness_class_spider"

    def __init__(self, fitness_club=None, *args, **kwargs):
        super(FitnessClassScraper, self).__init__(*args, **kwargs)
        self.club = fitness_club.split()[0]
        self.start_urls = [fitness_club.split()[1]]

    def parse(self, response):
        fitness_classes = []

        end_of_the_week = response.css('.week_chooser span::text').extract_first().split('do')[1].strip()
        sunday = datetime.strptime(end_of_the_week, '%d-%m-%Y')
        monday = sunday - timedelta(6)
        rows = response.css('table.calendar_table tr')

        connection = sqlite3.connect(':memory:')
        cursor = connection.cursor()

        cursor.execute('create table fitness_classes (day varchar(20), hour varchar(10), name varchar(50), place varchar(40), date varchar(10))')

        for row in rows[1:]:
            if row.css('.hour ::text').extract_first() is None:
                continue

            hour = row.css('.hour ::text').extract_first().strip()

            for num, cell in enumerate(row.css('td')):
                if num == 0:
                    continue
                cell_content = cell.css('.event_name::text').extract_first()
                if cell_content is None:
                    continue
                else:
                    date = monday + timedelta(num - 1)
                    fitness_classes.append(FitnessClass(Day(num), hour, cell_content, self.club, date.date()))

        for fitness_class in fitness_classes:
            cursor.execute('insert into fitness_classes values(?, ?, ?, ?, ?)', (fitness_class.day.name, fitness_class.hour, fitness_class.name, fitness_class.place, fitness_class.date))
            # fitness_class.print_class()

        cursor.execute('select * from fitness_classes')
        print(cursor.fetchall())

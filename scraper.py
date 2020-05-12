import scrapy
from enum import Enum
from datetime import datetime, timedelta
import sqlite3

from zdrofit_class import ZdrofitClass


class Day(Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7


class FitnessClassScraper(scrapy.Spider):
    name = "fitness_class_spider"

    def __init__(self, fitness_club=None, *args, **kwargs):
        super(FitnessClassScraper, self).__init__(*args, **kwargs)
        self.club_id = fitness_club.split(',')[0]
        self.club = fitness_club.split(',')[1]
        self.start_urls = [fitness_club.split(',')[2]]

    def parse(self, response):
        sql_lite_connection = sqlite3.connect(
            '/Users/monikaangerhoefer/Documents/python-projects/django-test/zdrofit/db.sqlite3')
        cursor = sql_lite_connection.cursor()
        cursor.execute("select max(id) from grafik_class")
        max_class_id = cursor.fetchone()[0]

        fitness_classes = []

        end_of_the_week = response.css('.week_chooser span::text').extract_first().split('do')[1].strip()
        sunday = datetime.strptime(end_of_the_week, '%d-%m-%Y')
        monday = sunday - timedelta(6)
        rows = response.css('table.calendar_table tr')

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
                    fitness_classes.append(ZdrofitClass(Day(num), hour, cell_content, self.club_id, date.date()))

        for fitness_class in fitness_classes:
            max_class_id += 1
            fitness_class.print_class()
            cursor.execute('INSERT INTO grafik_class VALUES(?, ?, ?, ?, ?, ?)', (
                max_class_id, fitness_class.day, fitness_class.hour, fitness_class.name, fitness_class.date,
                fitness_class.place))
            sql_lite_connection.commit()

        sql_lite_connection.close()

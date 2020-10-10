class ZdrofitClass:

    def __init__(self, day, hour, name, place, date, instructor):
        self.day = day
        self.hour = hour
        self.name = name
        self.place = place
        self.date = date
        self.instructor = instructor

    def print_class(self):
        print(self.name + " " + self.day.name + " " + self.hour + " " + self.place + " " + str(self.date) + " " + str(self.instructor))

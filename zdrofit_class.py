class ZdrofitClass:

    def __init__(self, day, hour, name, place, date):
        self.day = day
        self.hour = hour
        self.name = name
        self.place = place
        self.date = date

    def print_class(self):
        print(self.name + " " + self.day.name + " " + self.hour + " " + self.place + " " + str(self.date))

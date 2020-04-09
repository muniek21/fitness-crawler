import sqlite3

from zdrofit_club import ZdrofitClub

sqlLiteConnection = sqlite3.connect('/Users/monikaangerhoefer/Documents/python-projects/django-test/zdrofit/db.sqlite3')
cursor = sqlLiteConnection.cursor()
print("Connected to database!")

fitnessClubData = open("fitnessClubData")
class_id = 2
for line in fitnessClubData:
    name, url, address = line.split(",")
    cursor.execute("INSERT INTO grafik_zdrofitclub VALUES (?, ?, ?, ?)", (class_id, name, address, url))
    class_id += 1
    print("Saved class " + name)

sqlLiteConnection.commit()

sqlLiteConnection.close()






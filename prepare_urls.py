import sqlite3

sqlLiteConnection = sqlite3.connect('/Users/monikaangerhoefer/Documents/python-projects/django-test/zdrofit/db.sqlite3')
cursor = sqlLiteConnection.cursor()

cursor.execute("SELECT * FROM grafik_zdrofitclub")
fitnessClubs = cursor.fetchall()

fitnessUrls = open("fitnessUrls.txt", "w")

for fitnessClub in fitnessClubs:
    fitnessUrls.write(str(fitnessClub[0]) + "," + fitnessClub[1] + "," + fitnessClub[3] + "\n")

sqlLiteConnection.close()
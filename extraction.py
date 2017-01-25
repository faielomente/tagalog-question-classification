import sys
import csv

file = open("/home/faielomente/Downloads/Help a CS Student Graduate.csv")
csv_f = csv.reader(file)

for row in csv_f:
    for item in range(2, len(row)):
        print row[item]

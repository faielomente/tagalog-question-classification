import sys
import os
import csv

def extract():
	file = open(os.path.abspath("Documents/THESIS FILES/Help a CS Student Graduate.csv"))
	csv_f = csv.reader(file)

	for row in csv_f:
		for item in range(2, len(row)):
			if row[item].count(":") == 0 and len(row[item]) > 2:
				row_items = (row[item].split('\n'))
				print (	row_items)

extract()
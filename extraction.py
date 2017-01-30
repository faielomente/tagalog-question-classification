import sys
import os
import csv

def extract(input, output):


	csv_f = csv.reader(input)
	wr = csv.writer(output, delimiter=',', quoting=csv.QUOTE_ALL)

	wr.writerow(["Questions", "Category"])

	for row in csv_f:
		for column in range(2, len(row)):
			if row[column].count(":") == 0:
				row_items = (row[column].split('\n'))
				print ("row_item: ", row_items)
				row_items = delete_empty_string(row_items)
				wr = csv.writer(output, delimiter='\n', quoting=csv.QUOTE_ALL)
				wr.writerow(row_items)


def delete_empty_string(my_list):
	

	for item in my_list:
		if len(item) == 0 or item == " ":
			my_list.remove(item)

	return my_list



input_file = open(os.path.abspath('files/Help a CS Student Graduate.csv'))
output_file = open(os.path.abspath('files/output.csv'), 'w')
extract(input_file, output_file)
input_file.close()
output_file.close()

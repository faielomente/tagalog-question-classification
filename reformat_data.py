import sys
import os
import csv
import my_stemmer

def format_data():
    input_file = open(os.path.abspath('files/cleaning_output.csv'))
    output_file = open(os.path.abspath('files/for_stemming.txt'), 'w+')
    csv_f = csv.reader(input_file)
    ctr = 1

    for row in csv_f:
        if ctr == 1:
            ctr+=1
        else:
            for column in range(0, len(row)):
                sen = row[column].split(" ")
                for word in sen:
					if '?' in word:
						word = word.replace('?', '')
						output_file.write(word)
						output_file.write("\n")
						output_file.write("?")
						output_file.write("\n")
					elif word != "":
						# print(word)
						output_file.write(word)
						output_file.write("\n")

    input_file.close()
    output_file.close()

format_data()
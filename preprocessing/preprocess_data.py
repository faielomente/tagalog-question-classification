import sys
import os
import csv
import re

import numpy as np
from sklearn.feature_extraction import DictVectorizer


def extract(input, output):

	csv_f = csv.reader(input)
	wr = csv.writer(output, delimiter=',', quoting=csv.QUOTE_ALL)

	wr.writerow(["Questions", "Category"])

	for row in csv_f:
		for column in range(2, len(row)):
			if row[column].count(":") == 0:
				row_items = (row[column].split('\n'))
				row_items = delete_empty_string(row_items)
				print ("row_item: ", row_items)
				wr = csv.writer(output, delimiter='\n', quoting=csv.QUOTE_ALL)
				wr.writerow(row_items)


def delete_empty_string(my_list):

	for item in my_list:
		if len(item) == 0 or item == " ":
			my_list.remove(item)

		if re.match("^[0-9]", item) != None:
			index = my_list.index(item)
			tmp = item.lstrip('0123456789.- ')
			my_list.remove(item)
			my_list.insert(index, tmp)
			print item

	return my_list


def sentence_to_object(file):

    text = file.readlines();
    array = list()
    dict = {}

    for line in text:
        data = line.split("\t")
        if data[0] != "?":
            word = data[0];
            pos = data[len(data)-1]
            pos = get_tags(pos, 1)
            dict[word] = pos.strip()
        elif data[0] == '?':
            array.append(dict)
            dict = {}

    return array


def get_tags(tag, level):

    if level == 1:
        tag = tag.split("-")[0]
    elif level == 2:
        temp = tag.split("-")[1]
        tag = temp[:2]
    elif level == 3:
        temp = tag.split("-")[1]
        tag = temp[2:]

    return tag


def transform(data):

    dict = {'NN':0, 'PR':0, 'DT':0, 'LM':0, 'CC':0, 'VB':0, 'JJ':0, 'RB':0, 'CD':0, 'TS':0}
    temp = []

    for sentence in data:
        for key in sentence:
            dict[sentence[key]] += 1

        temp.append(dict)
        dict = {'NN':0, 'PR':0, 'DT':0, 'LM':0, 'CC':0, 'VB':0, 'JJ':0, 'RB':0, 'CD':0, 'TS':0}
     
    return temp


def to_numerical():
    input_file = open(os.path.abspath('files/pos_tagging.out'))
    #sentence_to_object(input_file)
    data = []
    
    vector = DictVectorizer(sparse=False)
    data = sentence_to_object(input_file)
    data = transform(data)
    # print "To_numerical"
    # print data
    X = vector.fit_transform(data)
    
    print X


def category_to_vector():
	input_file = open(os.path.abspath('files/testing_data.csv'))
	csv_f = csv.reader(input_file)

	cat = []
	column = 0

	category = {'entity':1, 'abbreviation':2, 'description':3, 'human':4, 'location':5, 'numeric':6}

	for row in csv_f:
		if "Questions" not in row:
			temp = []
			for column in range(1, 2):
				if row[column] != "Category" and row[column] in category:
					temp.append(category[row[column].lower()])
				else:
					temp.append(0)
			cat.append(temp)

	print cat

	return cat



def main():
	# input_file = open(os.path.abspath('files/Help a CS Student Graduate.csv'))
	# output_file = open(os.path.abspath('files/cleaning_output.csv'), 'w')
	# extract(input_file, output_file)
	# input_file.close()
	# output_file.close()

	# input_file = open(os.path.abspath('files/pos_tagging.out'))
	# sentence_to_object(input_file)
	# to_numerical()
	category_to_vector()


if __name__ == "__main__":
    main()
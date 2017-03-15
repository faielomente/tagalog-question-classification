import os
import sys
import numpy as matrix
import stemmer


def read():
	data_array = []
	with open(os.path.abspath('files/cleaning_output.csv')) as f:
		for line in f:
			# omit punctuation mark
			line = line.replace('?', '')
			
			# array of words na ni without the quotations
			line = line[line.find("\"")+1:line.rfind("\"")]
			word_list = line.split()
			data_array.append(word_list)
		print (data_array)

# def extract_word_parts(data):
# 	for sentence in data:
# 		for word in sentence:
# 			parts = 

read()
stemmer.main("files/stem_words_test.txt")
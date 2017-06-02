import sys
import os
import csv
import re
import string
import math



def to_tuples_array(file):
	text = file.readlines();
	array = []
	sentence = []
	tuple = ()
	ctr = 0

	for line in text:
		data = line.split("\t")
		if data[0] != "?" and len(line.strip()) > 0:
			word = data[0];
			pos = data[len(data)-1]
			pos = get_coarsetag(pos, 1)
			tuple = (word,pos.strip())
			sentence.append(tuple)
		elif data[0] == '?':
			array.append(sentence)
			sentence = []
			tuple = ()

			ctr += 1

			# print ctr

	# for i in range(0, len(array)):
	# 	print array[i]

	return array


def get_coarsetag(tag, level):

	if level == 1:
		tag = tag.split("-")[0]
	elif level == 2:
		temp = tag.split("-")[1]
		tag = temp[:2]
	elif level == 3:
		temp = tag.split("-")[1]
		tag = temp[2:]

	return tag


def get_raw(file, column_no):
	"""
	Get the labelled sentence from the csv file then convert
	it to array
	"""

	r = csv.reader(file)

	if column_no == 0:
		text = []
		for row in r:
			if row[0] != "Questions":
				text.append(row[0].strip())

		print len(text)

		return text
	elif column_no == 1:
		cat = []
		for row in r:
			if row[1] != "Category":
				cat.append(row[1])

		print len(cat)

		return cat


def prune(tuple_array, sentences):

	conj = {"sapagkat", "dahil", "dahil sa", "at saka", "at hindi", "ni hindi", "pero", "datapwat", "ngunit", "subalit", "o", "o kaya", "gayon pa man", "gayumpaman", "gayunman", "kaya", "kung kaya't", "kung kaya", "man", "maging", "hindi lamang", "kundi", "bagaman", "bagama't", "kapag", "kasi", "dahilan sa", "gawa ng", "porke", "porke at", "porke't", "pagkat", "kaya", "kaysa", "kahit", "gayong", "kung", "kung gayon", "habang", "nang", "nang sa gayon", "maging", "maliban kung", "palibhasa", "para", "upang", "parang", "pansamantala", "hanggang"}

	q_words = {'aling', 'alin-alin', 'alin-aling', 'saang', 'saan-saan', 'nasaan', 'nasaang', 'anong', 'anu-ano', 'anu-anong', 'inaano', 'paanong', 'papaano','papaanong', 'sinong', 'sinu-sino', 'sino-sinong', 'kailang', 'alin', 'saan', 'ano', 'kailan', 'paano', 'sino', 'bakit'}

	pruned_array = []
	
	for i in range(0, len(sentences)):
		temp = sentences[i].replace('?', '')
		text = temp.split(" ")
		
		for word in text:
			if word.lower() in conj:
				ind = text.index(word)

				# conjuction should not be too near in the beginning of the sentence
				if len(text) >= 5 and ind >= math.ceil(len(text)/2):
					tuple_array[i] = tuple_array[i][:ind]
				elif ind == 0:
					for j in range(ind, len(text)):
						if text[j].lower() in q_words:
							tuple_array[i] = tuple_array[i][j:len(text)]
							break

	# Scan each tuple array for arrays not starting with a wh-word
	for i in range(0, len(tuple_array)):
		if tuple_array[i][0][0] not in q_words:
			t = sentences[i].split(" ")

			for j in range(0, len(tuple_array[i])):
				if t[j].lower() in q_words:
					tuple_array[i] = tuple_array[i][j:]


	# for i in range(0, len(tuple_array)):
	# 	if tuple_array[i][0][0].lower() not in q_words:
	# 		print tuple_array[i], sentences[i]



	return tuple_array


def to_fpformat(pruned_array, category):
	
	array = []

	for i in range(0, len(pruned_array)):
		data = []

		for j in range(0, len(pruned_array[i])):
			if j == 0:
				data.append(pruned_array[i][j][0].lower())
			else:
				data.append(pruned_array[i][j][1].lower())

		data.append(category[i].lower())
		array.append(data)

	return array


def write_to_file(data):
	output_file = open(os.path.abspath('files/fpFormat.out'), 'w')

	for i in range(0, len(data)):
		for j in range(0, len(data[i])):
			output_file.write(str(data[i][j]))
			output_file.write(" ")
		
		output_file.write("\n")

	output_file.close()


def format():
	input1 = open(os.path.abspath('files/dataset_pos.out'))
	input2 = open(os.path.abspath('files/labelled_data.csv'))
	input3 = open(os.path.abspath('files/labelled_data.csv'))

	tup = to_tuples_array(input1)
	sen = get_raw(input2, 0)
	cat = get_raw(input3, 1)

	input1.close()
	input2.close()
	input3.close()

	pruned_array = prune(tup, sen)
	fpFormat = to_fpformat(pruned_array, cat)

	print len(pruned_array)
	print len(fpFormat)

	write_to_file(fpFormat)

	return fpFormat


if __name__ == '__main__':
    format()
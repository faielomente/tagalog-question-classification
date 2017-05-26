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


def get_raw_sentences(file):
	"""
	Get the labelled sentence from the csv file then convert
	it to array
	"""

	r = csv.reader(file)
	text = []

	for row in r:
		for column in range(0,1):
			if row[column] != "Questions":
				text.append(row[column])

	# print len(text)

	return text


def prune(tuple_array, sentences):

	conj = {"sapagkat", "dahil", "dahil sa", "at saka", "ni", "at hindi", "ni hindi", "pero", "datapwat", "ngunit", "subalit", "o", "o kaya", "gayon pa man", "gayumpaman", "gayunman", "kaya", "kung kaya't", "kung kaya", "man", "maging", "hindi lamang", "kundi", "bagaman", "bagama't", "kapag", "kasi", "dahilan sa", "gawa ng", "porke", "porke at", "porke't", "pagkat", "kaya", "kaysa", "kahit", "gayong", "kung", "kung gayon", "habang", "nang", "nang sa gayon", "maging", "maliban kung", "palibhasa", "para", "upang", "parang", "pansamantala"}

	q_words = {'aling', 'alin-alin', 'alin-aling', 'saang', 'saan-saan', 'nasaan', 'nasaang', 'anong', 'anu-ano', 'anu-anong', 'inaano', 'paanong', 'papaano','papaanong', 'sinong', 'sinu-sino', 'sino-sinong', 'kailang', 'alin', 'saan', 'ano', 'kailan', 'paano', 'sino', 'bakit'}
	
	for i in range(0, len(sentences)):
		temp = sentences[i].replace('?', '')
		text = temp.split(" ")

		for word in text:
			# if '?' in word:
			# 	word = word.replace('?','')

			if word.lower() in conj:
				ind = text.index(word)
				print ind

				# conjuction should not be too near in the beginning of the sentence
				if len(text) >= 5 and ind >= math.ceil(len(text)/2):
					tuple_array[i] = tuple_array[i][:ind]
				elif ind == 0:
					for j in range(ind, len(text)):
						print text[j].lower()
						if text[j].lower() in q_words:
							tuple_array[i] = tuple_array[i][j:len(text)]
							break;

	
	for i in range(0, len(tuple_array)):
		print sentences[i], tuple_array[i]


def main():
	input1 = open(os.path.abspath('files/dataset_pos.out'))
	input2 = open(os.path.abspath('files/labelled_data.csv'))
	x = to_tuples_array(input1)
	y = get_raw_sentences(input2)
	input1.close()
	input2.close()

	prune(x, y)



if __name__ == '__main__':
    main()
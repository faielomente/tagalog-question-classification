import sys
import os
import csv
import re
import string

import numpy as np
from sklearn.feature_extraction import DictVectorizer

from nltk.tokenize import RegexpTokenizer
from nltk.util import ngrams


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


def to_wordpos_dict(file):

    text = file.readlines();
    array = list()
    dict = {}
    ctr = 0

    for line in text:
        data = line.split("\t")
        if data[0] != "?":
            word = data[0];
            pos = data[len(data)-1]
            # pos = get_tags(pos, 1)
            dict[word] = pos.strip()
        elif data[0] == '?':
            array.append(dict)
            dict = {}
        ctr += 1

    # print ctr
    print array
    
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
    ctr = 0

    for sentence in data:
        for key in sentence:
            ctr += 1
            dict[sentence[key]] += 1

        temp.append(dict)
        dict = {'NN':0, 'PR':0, 'DT':0, 'LM':0, 'CC':0, 'VB':0, 'JJ':0, 'RB':0, 'CD':0, 'TS':0}
     

    return temp


def to_numerical():
    input_file = open(os.path.abspath('files/dataset_pos.out'))
    #sentence_to_object(input_file)
    data = []
    
    vector = DictVectorizer(sparse=False)
    data = sentence_to_object(input_file)
    data = transform(data)
    # print "To_numerical"
    # print data
    X = vector.fit_transform(data)
    
    print X


def category_vector(file):
    input_file = file
    csv_f = csv.reader(input_file)

    cat = []
    column = 0
    ctr = 0

    category = {'entity':1, 'abbreviation':2, 'description':3, 'human':4, 'location':5, 'numeric':6}

    for row in csv_f:
        ctr += 1
        if "Questions" not in row:
            temp = []
            for column in range(1, 2):
                if(row[column] != "Category" and (row[column]) > 0):
                    temp.append(category[row[column].lower()])
            cat.append(temp)
            
#     print cat
    
    input_file.close()
            
    return cat


def count_qmark(file):
    text = file.readlines();

    for line in text:
        if line.count("?") > 2:
            print line


def pos_vec(file):
    input_file = file
    data = []
    
    data = to_wordpos_dict(input_file)
    print data
    # data = transform(data) #don't transfor for csr implementation
    
    input_file.close()
    
    return data


def get_wh_question(file):
    reader = csv.reader(file)
    
    q_word_tags = {'alin':1, 'saan':2, 'ano':3, 'kailan':4, 'paano':5, 'sino':6, 'bakit':7 }
    q_words = {'aling', 'alin-alin', 'alin-aling', 'saang', 'saan-saan', 'nasaan', 'nasaang', 'anong', 'anu-ano', 'anu-anong', 'inaano', 'paanong', 'papaano','papaanong', 'sinong', 'sinu-sino', 'sino-sinong', 'kailang'}
    
    vec = []
    
    for row in reader:
#         print row
        sentence = row[0].split(" ")
        temp = []

        for word in sentence:
            if word.lower() in q_word_tags:
                # print word.lower()
                temp.append(q_word_tags[word.lower()])
                vec.append(temp)
                break
            elif word.lower() in q_words:
                for key in q_word_tags:
                    if key in word.lower():
                        temp.append(q_word_tags[key])
                        vec.append(temp)
                        break
        
    # print vec
    
    return vec


def tokenize_word_data(file):
    reader = csv.reader(file)

    tokenizer = RegexpTokenizer(r'\w+')
    data = []
    row = 0

    for row in reader:
        # Escaping the first row because it only contains the column titles
        if row == 0:
            row += 1
        else:
            data.append(tokenizer.tokenize(row[0]))


    print len(data)

    return data


def main():
    """
    1. Preprocessing the raw data.
    """
    # input_file = open(os.path.abspath('files/Help a CS Student Graduate.csv'))
    # output_file = open(os.path.abspath('files/cleaning_output.csv'), 'w')
    # extract(input_file, output_file)
    # input_file.close()
    # output_file.close()
    ########

    """
    2. Checking the equality of the pos tags, wh-words and category gathered.
    Total should be 3077.
    """
    pos_data = pos_vec(open(os.path.abspath('files/dataset_pos.out')))
    wh_vector = get_wh_question(open(os.path.abspath('files/labelled_data.csv')))
    category = category_vector(open(os.path.abspath('files/labelled_data.csv')))

    print "Data Length: ", len(pos_data)
    print "Wh_Question Length: ", len(wh_vector)
    print "Category Length: ", len(category)
    ###########

    # tokenize_word_data(open(os.path.abspath('files/labelled_data.csv')))




if __name__ == '__main__':
    main()
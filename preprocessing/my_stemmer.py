import re
import sys
import csv
import os
    

infix = ['um', 'in'] ##list of infix
prefix = ['makapang','nakapang','nakapan','makapan','nakapam','makapam','nakapag','makapag','nagpati','magpati','nagpaka','magpaka',
    'magpapa','nagpapa','nagkaka','magkaka','ipakipa','ikapang','naipag','mangag','nangag','kasing','ipang','pinag','papag','mapag', 'kapag',
    'napag','ipaki','magka','magsi','nagka','magma','nagma','magpa','nagpa','maipa','naipa','kasim','pagpa','paka','paki','pang','ipag',
    'mang','nang','maka','naka','mapa','napa','ika','pag','isa','ipa','mai','nai','mag','nag','man','nan','mam','nam','ma','na','ka','pa']
suffix = ['han', 'hin', 'an','in'] #suffixes
vowel = ['a','e','i','o','u']

def strip_infix(word):
    dictionary = {'word': "", 'infix': "_"}

    for inf in infix:
        if (inf in word):
            start_pos = re.search(inf, word).start()
            end_pos = re.search(inf, word).end()

            #checks the position of infix; removes infix only if in the middle, start position, or word length > 3
            if (start_pos >= 0 and end_pos < len(word) and len(word) > 4):
                #if word ! in dictionary
                word = re.sub(inf,'',word,1)

            dictionary['infix'] = inf

    dictionary['word'] = word
    
    return dictionary

###

def strip_suffix(word):
    d = {'word':"", 'suffix': "_"}

    for suf in suffix:
        if (suf in word):
            if(word.endswith(suf) and len(word) > 4):
                word = re.sub(suf+'$','',word,1)
                d['suffix'] = suf

    d['word'] = word

    return d

###

def strip_prefix(word):
    # temp_word,prefix_found,the_prefix
    d = {'word': "", 'prefix': "_", 'has_pref': False}

    for pre in prefix:
        if(pre in word):
            if(word.startswith(pre) and len(word) > 5):
                word = re.sub(pre,'',word,1)
                d['prefix'] = pre
                d['has_pref'] = True

        if word.startswith("-"):
            # print ("hello")
            word = word[1:]

        # checks reduplication of vowel prefixes
        for char in vowel:
            if(word.startswith(char) and len(word) > 1):
                if(word[0] == word[1]):
                    word = word[1:]
            # print("Again")

        # word = check_reduplication(word)
        d['word'] = word
        # print (d['word'])

    return d

###
def check_reduplication(word):
    d = {'word': "", 'redup': "_"}

    for i in range(1,3):
        if word[:i] == word[i:i+i]:###python substring;
            word= word[i:]
            d['redup'] = word[:i]
            break
    
    d['word'] = word

    return d

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


def  write_to_file(stemmed_data):
    output_file = open(os.path.abspath('files/for_pos_tagging.txt'), 'w')
    # print(stemmed_data)

    for dict in stemmed_data:
        output_file.write(dict['word'])
        output_file.write(" ")
        output_file.write(dict['root'])
        output_file.write(" ")
        output_file.write(dict['prefix'])
        output_file.write(" ")
        output_file.write(dict['suffix'])
        output_file.write(" ")
        output_file.write(dict['redup'])
        output_file.write(" ")
        output_file.write("XXX")
        output_file.write("\n")

    output_file.close()


def main():
    """
    Rearrange the data into vertical sentences.
    Each sentence ending with a questions mark
    """
    format_data()

    """
    The output file of format_data() will be read.
    And each word is stemmed.
    """
    # wordfile = open(os.path.abspath('files/stem_words_test.txt'))
    wordfile = open(os.path.abspath('files/for_stemming.txt'))

    stemmed_data = list()

    for words in wordfile.readlines():
        infix_dict = {'word': "", 'infix': "_"}
        pref_dict = {'word': "", 'prefix': "_", 'has_pref': False}
        redup_dict = {'word': "", 'redup': "_"}
        suf_dict = {'word':"", 'suffix': "_"}
        morphology = {'word':"", 'root':"", 'prefix':"_", 'infix':"_", 'suffix':"_", 'redup':"_"}
        root = words    
        infix_dict = strip_infix(words.lower())    ###remove any infix first
        temp_word = infix_dict['word']

        if len(temp_word.strip()) > 6: #usually root words are 4-5 characters in length
            pref_dict = strip_prefix(temp_word) #try to check prefixes and suffixes
            temp_word = pref_dict['word']
            suf_dict = strip_suffix(temp_word)
            temp_word = suf_dict['word']
            redup_dict = check_reduplication(temp_word)
            temp_word = redup_dict['word']


        # while((pref_dict['has_pref'] == True) and (len(temp_word) > 7)):
        #     pref_dict = strip_prefix(temp_word)  #try to check prefixes and suffixes
        #     # print("HEEEREEEE!!!!!!!!!!!!!!!!!!!!!!!", pref_dict['has_pref'])
        #       temp_word = pref_dict['word']
        
        root = temp_word

        morphology['word'] = words.strip()
        morphology['root'] = root.strip()
        morphology['prefix'] = pref_dict['prefix']
        morphology['suffix'] = infix_dict['infix']
        morphology['redup'] = redup_dict['redup']

        # print(morphology)
        stemmed_data.append(morphology)

    write_to_file(stemmed_data)
    # print(stemmed_data)


if __name__ == "__main__":
    main()
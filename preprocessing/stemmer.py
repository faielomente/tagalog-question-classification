#!/usr/bin/python
##Erlyn Manguilimotan
##Jan 27, 2017

import sys
import re


wordfile = open(sys.argv[1]) #file of words to process; assumes one word per line

infix = {'um', 'in'} ##list of infix
prefix = {'mag', 'nag', 'magsi', 'nagsi', 'mang', 'nang', 'maka', 'naka','magka','magkaka','nagka','nagkaka', 'magma', 'nagma', 'magpa', 'nagpa', 'magpapa', 'nagpapa', 'magpaka', 'nagpaka', 'magpati', 'nagpati', 'ma', 'na', 'mai', 'nai', 'maipa', 'naipa', 'maipag', 'naigpag', 'makapag', 'nakapag', 'mapa', 'napa', 'makapang', 'nakapang', 'nakapan', 'makapan', 'makapam', 'nakapam', 'mang', 'nang', 'man', 'nan', 'mam', 'nam', 'mangag', 'nangag', 'i', 'ipa', 'ipaki', 'ipakipa', 'isa', 'ka', 'pa', 'pag', 'papag', 'mapag', 'napag', 'pang', 'ipag', 'ipang', 'pinag', 'ika', 'ikapang', 'paka', 'paki', 'kasim', 'kasing', 'pagpa' } #prefixes
suffix = {'an', 'han', 'in', 'hin'} #suffixes
vowel = {'a','e','i','o','u'}

#################################################
def strip_infix (s):

	prev = '' #previous character
	current = ''  #current character
	position = 0
	cand_infix ='' #candidate infix
	for i in s :
		position +=1 # monitor position. if matched affix is at the end, then it's not infix
		current= prev+i ##combine two characters

		if current.strip() in infix and position < (len(s)-1): ##if current combination is in the infix array and not last position
			cand_infix = current  
			
		prev = i

	return  re.sub(cand_infix,'',s,1) #return the string removing the candidate infix
	

#################################################

def strip_suffix(s):
	suffix_candidates = []
	candidate_root = s.strip()
	
	the_suffix =''

	if len(candidate_root) < 5:
               return candidate_root

	

        for suf in suffix:
                if candidate_root.endswith(suf):

                        suffix_candidates.append(suf) ###find possible candidates "han" "an"

       	for suf in suffix_candidates:
                temp1 = re.sub(suf+'$','',candidate_root,1)  ## test to strip out candidate suffix

		if len(temp1) < 3:
			the_suffix=''
			break
	
                temp1 = temp1.strip()
                if temp1[len(temp1)-1] is not 'h': 
		##if word, after removing candidate suffix, does not end with 'h'. tagalog words don't usually end with 'h'
                      the_suffix = suf

	candidate_root = re.sub(the_suffix+'$','',candidate_root,1)
	if candidate_root.endswith('u'):
		candidate_root = re.sub('u$','o',candidate_root,1)
	
	return candidate_root

########################################

def strip_prefix (s): ##usually, the prefix appears with a suffix e.g. paghandaan (pag ~~ an)		


	prefix_candidates = []
	candidate_root =s.strip()
	found = False

	if len(candidate_root) < 6:
		return candidate_root

	
	for pre in prefix:
		if s.startswith(pre):
			prefix_candidates.append(pre) ##possible to have more than one candidate prefix, e.g.'pa', 'pag'
	if len(prefix_candidates) > 0:
		
		found = True

		for p in prefix_candidates:

			temp1 = re.sub('^'+p,'',s,1) ###remove candidate 
		
			temp1 = temp1.strip()
			
			if temp1[0]  not in vowel and temp1[1] in vowel: ## for words that start with consonant or hyphen (mag-ampon, pagkain, paggawa)
				candidate_root = temp1


	candidate_root = re.sub('^\W','',candidate_root,1)	### remove hyphen if found (mag-ampon, pag-asa)

	return candidate_root, found
########################################

def reduplication(word):

	if len(word) > 4:  ##for words with length greater than 4. words like 'baba' should not be included

 		for i in range(1,3):

        		if word[:i] == word[i:i+i]:  ###python substring; 

                		word= word[i:]
                		break


	return word


##########################################

for words in wordfile.readlines():
		

	root = words	
	temp_word = strip_infix(words.lower())	 ###remove any infix first
	prefix_found=False

	
	if len(temp_word.strip()) > 6: #usually root words are 4-5 characters in length


		temp_word,prefix_found = strip_prefix(temp_word) #try to check prefixes and suffixes
		temp_word = strip_suffix(temp_word)

	while(prefix_found == True and len(temp_word) > 7):
		temp_word,prefix_found = strip_prefix(temp_word) #try to check prefixes and suffixes
	
	root = reduplication(temp_word)
	
		
	print words.strip(), root.strip()


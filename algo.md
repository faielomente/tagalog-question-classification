### Preprocessing
1. Extract each question from the survey's .csv file and save it in a file named "cleaning_output.csv"
The file is an n by 2 dimension table. Where n is the number of interrogative sentences gather in the survey.
The first column contains the interrogative sentence and the second is the category.

### Stemming
1. Declare list of infixes, suffixes and vowels.
2. Transform each sentence in the file (cleaning_ouput.csv) into vertical sentences.
	- Each line must contain 1 word.
	- Sentences must end with a punction mark.
	- Each sentence must be separated by a space.
3. Save it in a file named "dataset_pos.in".

4. Read the file and traverse each line(word):
	a. While word length > 5:
		- extract infix, if there is any and save it in the "infix_dict" variable
		- update temp_word
		- extract prefix, if there is any and save it in the "pref_dict" variable
		- update temp_word
		- extract suffix, if there is any and save it in the "suf_dict" variable
		- update temp_word
		- extract redupliaction, if there is any and save it in "redup_dict" variable
		- update temp_word
	b. root  = - temp_word
	c. save all the data gathered in "a" in a dictionary called "morphology"
	d. append the deictionary to the "stemmed_data" listt
5. Replace the contents of the file "dataset_pos.in" with the list items in the "stemmed_data" list

### Rule-based Classification
1. Partition data into testing and training set.
2. Format data so that it can keep track of the frequency.
	The createTree() function doesn't take the input data as lists. It expects a dictionary with the itemsets as the dictionary keys and the frequency as the value. A createInitSet() function does this conversion for you.
3. Create a headerTabble and the Tree.
4. Mine the rules.
	- For each catgory list all the paths.
	- From the list, remove all the paths with nodes that did not reach the minimum support
	- Return the remaining paths. These are the rules.
5. Classificcation
	- Get the ordered rule set from the rules
	- For each data in the testing set:
		- classify the question using the rules mined.
			- if a data in the testing data did not trigger any category:
				- for each pattern in that category, check if any rule is a subset of a sentence
				- if testing data still didn't trigger any rule
	            - assign default class according to its question word
	            - However, if more than one category was triggered by the subset
	            - assign default class according to its question word
	        - else if more than one category was triggered by the subset:
	        	- for each category triggered by data, combine data pattern with category as tuples
	        	- for each rule in ordered list, if combined pattern and category match rule[i] get the index
	        	- get the maximum of all the index gathered, that will be the assigned category
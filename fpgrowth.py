from fim import fpgrowth, fim
from preprocessing import preprocessing_csr as prep

# item base is the set of all considered items
tracts = prep.format()

for t in tracts: 
	print(t)

for r in fpgrowth(tracts):
	print r

# print len(item_base)
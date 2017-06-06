from preprocessing import preprocessing_csr
import collections



class treeNode:
    """variables:
        name of the node, a count
        nodelink used to link similar items
        parent vaiable used to refer to the parent of the node in the tree
        node contains an empty dictionary for the children in the node"""
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None
        self.parent = parentNode      #needs to be updated
        self.children = {}

#increments the count variable with a given amount    
    def inc(self, numOccur):
        self.count += numOccur

#display tree in text. Useful for debugging        
    def disp(self, ind=1):
        print ('  '*ind, self.name, ' ', self.count)
        for child in self.children.values():
            child.disp(ind+1)


def createTree(dataSet, minSup=1): #create FP-tree from dataset but don't mine
    """takes the dataset and the minimum support
    as arguments and builds the FP-tree. This 
    makes two passes through the dataset. The 
    first pass goes through everything in the 
    dataset and counts the frequency of each term. 
    These are stored in the header table."""
    
    headerTable = {}

    #go over dataSet twice
    for trans in dataSet:   #first pass counts frequency of occurance
        print trans
        for item in trans:
            headerTable[item] = headerTable.get(item, 0) + dataSet[trans]

    # for k in list(headerTable):  #remove items not meeting minSup
    #     if headerTable[k] < minSup: 
    #         del(headerTable[k])

    freqItemSet = list(headerTable.keys())
    print 'freqItemSet: ',freqItemSet

    if len(freqItemSet) == 0: 
        return None, None  #if no items meet min support -->get out
    
    for k in headerTable:
        headerTable[k] = [headerTable[k], None] #reformat headerTable to use Node link 
    
    print 'headerTable: ',headerTable

    retTree = treeNode('Null Set', 1, None) #create tree

    for tranSet, count in dataSet.items():  #go through dataset 2nd time
        localD = {}
        for item in tranSet:  #put transaction items in order
            if item in freqItemSet:
                localD[item] = headerTable[item][0]
        if len(localD) > 0:
            orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: p[1], reverse=True)]
            updateTree(orderedItems, retTree, headerTable, count)   #populate tree with ordered freq itemset

    return retTree, headerTable #return tree and header table


def updateTree(items, inTree, headerTable, count):
    """grow the Fp-tree with an itemset"""

    if items[0] in inTree.children:#check if orderedItems[0] in retTree.children
        inTree.children[items[0]].inc(count) #incrament count
    else:   #add items[0] to inTree.children
        inTree.children[items[0]] = treeNode(items[0], count, inTree)
        if headerTable[items[0]][1] == None: #update header table 
            headerTable[items[0]][1] = inTree.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1], inTree.children[items[0]])
    if len(items) > 1:#call updateTree() with remaining ordered items
        updateTree(items[1::], inTree.children[items[0]], headerTable, count)


def updateHeader(nodeToTest, targetNode):   #this version does not use recursion
    while (nodeToTest.nodeLink != None):    #Do not use recursion to traverse a linked list!
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode


def ascendTree(leafNode, prefixPath): #ascends from leaf node to root
    """ which ascends the tree, collecting the names of items it encounters"""

    if leafNode.parent != None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent, prefixPath)


def findPrefixPath(basePat, treeNode): #treeNode comes from header table
    """function iterates through the 
    linked list until it hits the end. 
    For each item it encounters, it 
    calls ascendTree().This list is 
    returned and added to the conditional 
    pattern base dictionary called condPats."""

    condPats = {}
    while treeNode != None:
        prefixPath = []
        ascendTree(treeNode, prefixPath)
        if len(prefixPath) > 1: 
            condPats[frozenset(prefixPath[1:])] = treeNode.count
        treeNode = treeNode.nodeLink
    return condPats


def loadSimpDat():
    simpDat = preprocessing_csr.format()
    return simpDat


def createInitSet(dataSet):
    """the createTree() function doesnt 
    take the input data as lists. It expects
    a dictionary with the itemsets as the 
    dictionary keys and the frequency as the
    value. A createInitSet() function does this
    conversion for you."""

    retDict = {}

    for trans in dataSet:
        retDict[frozenset(trans)] = 1

    return retDict


# testing the tree
# rootNode = treeNode('pyramid',9,None)
# rootNode.children['eye'] = treeNode('eye',13,None)
# rootNode.disp()

#testing the sample data
simpDat = loadSimpDat()
print simpDat

"""
[['saan', 'pr', 'vb', 'abbreviation'], 
['paano', 'pr', 'vb', 'dt', 'dt', 'nn', 'cc', 'pr', 'abbreviation'], 
['ano', 'dt', 'nn', 'vb', 'cc', 'nn', 'pr', 'vb', 'nn', 'abbreviation'], 
['saan', 'pr', 'rb', 'nn', 'cc', 'nn', 'abbreviation'], 
['saan', 'pr', 'vb', 'abbreviation'], 
['saan', 'pr', 'cd', 'vb', 'abbreviation'], 
['ano', 'dt', 'vb', 'vb', 'cc', 'nn', 'abbreviation'], 
['saan', 'pr', 'rb', 'vb', 'abbreviation'], 
['saan', 'pr', 'vb', 'abbreviation'], 
['ano', 'dt', 'vb', 'vb', 'cc', 'nn', 'abbreviation']]
"""

initSet = createInitSet(simpDat)
print initSet



#The FP-tree
myFPtree, myHeaderTab = createTree(initSet, 3)
myFPtree.disp()

# ------------------alternative mining fuction for the fp-tree---------------------------
def mineTree(inTree, headerTable, minSup, preFix, freqItemList):
    bigL = [v[0] for v in sorted(headerTable.items(), key=lambda p: p[1])] # (sort header table)
    print 'headerTable: ', headerTable.items()
#     ['cd', 'paano', 'rb', 'ano', 'cc', 'dt', 'saan', 'nn', 'pr', 'abbreviation', 'vb']
    
#     suffixTable = ['entity', 'abbreviation', 'description', 'human', 'location', 'numeric'] 
    
    for basePat in bigL: # start from bottom of header table
        newFreqSet = list(preFix)
        newFreqSet.append(basePat)
    
        print 'finalFrequent Item: ',newFreqSet #append to set

        freqItemList.append(newFreqSet)
        condPattBases = findPrefixPath(basePat, headerTable[basePat][1])
    
#     print 'condPattBases :' ,basePat, condPattBases

    # 2. construct cond FP-tree from cond. pattern base
        myCondTree, myHead = createTree(condPattBases, minSup)
    
#     print 'head from conditional tree: ', myHead
    
        if myHead != None: # 3. mine cond. FP-tree
            print 'conditional tree for: ',newFreqSet
            myCondTree.disp(1)
            mineTree(myCondTree, myHead, minSup, newFreqSet, freqItemList)

preFix = []
freqItemList = []
mineTree(myFPtree, myHeaderTab, 10, preFix, freqItemList)
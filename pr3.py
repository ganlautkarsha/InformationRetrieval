import pickle
def buildInvertedIndex( wordDict):
    docIdFile = "docID.txt"
    fp = open(docIdFile, "r")
    docLine=fp.readline().split("\n")
    docCount = docLine[0]
    print docCount
    fp.close()
    open the index file and enter the info
    docMappings = "docMappings.txt"
    fp = open(docMappings, "a")
    with open('pickeDict.pickle','wb') as fp:
        pickle.dump(wordDict,fp)
    with open('pickleDict.pickle','rb') as fp:
        b=pickle.load(fp)
    print b
    print "hello"
buildInvertedIndex({'hello':'word'})
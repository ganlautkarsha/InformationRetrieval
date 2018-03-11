import filesort
import math
import math
import filesort
import heapq

#from pymongo import MongoClient
def buildInvertedIndex( wordDict, numberOfDocs):
    print "Inside index build"
    #with open('pickleDict.pickle','wb') as fp:
     #   pickle.dump(wordDict,fp)
    #with open('pickleDict.pickle','rb') as fp:
     #   b=pickle.load(fp)
    #print b
    N = numberOfDocs
    print N
    with open('manualIndex.txt','w') as fp:
        for word,value in wordDict.iteritems():
            fp.write(word)
            fp.write(' ')
            for vals in value:
                for w,v in vals.iteritems():
                    fp.write(w)
                    fp.write(' ')
                    for item in v:
                        #print>>fp, item
                        fp.write(str(item) + ' ')
                    fp.write(' -1 ')
            fp.write('\n')
    filesort.batch_sort('manualIndex.txt','sortedIndex.txt')
    currentDict={}
    # Create connection to MongoDB
    # client = MongoClient()
    # db = client['tfidf']
    # collection = db['index']
    linecount=0
    with open('tf-idf.txt','w') as tfidf:
    #tfidf=anydbm.open('tf-idfdb.txt','c')
        with open('sortedIndex.txt','r') as fp:
            #tfidf.write('Word\tDocID\ttfidf\t...\n')
            for line in fp:
                words = line.split(' ')
                linetowrite = str(words[0])
                count=0
                tf=0
                df=0
                for w in words:
                    if w==str('-1'):
                        df+=1
                idf= math.log(1 + N/df)
                #print idf,N,df
                docid = str(0)
                for w in words:
                    if w==words[0]:
                        continue
                    if '/' in w:
                        docid=w
                        continue
                    if w!=str('-1'):
                        tf+=1
                    if w==str('-1'):
                        tfidfval = math.log(1+tf) * idf
                        #print tf
                        linetowrite += ' ' + docid + ' ' + str(round(tfidfval,5))
                        # currentDict[words[0]]={}
                        # currentDict[words[0]][docid]=str(round(tfidfval,5))
                        # tfidf[words[0]]={}

                        tf=0
                # tfidf[words[0]]=linetowrite
                tfidf.write(linetowrite)
                tfidf.write('\n')
                linecount+=1
    with open('linecount.txt','w') as f:
        f.write(str(linecount))
            #json.dump(currentDict,tfidf)
        # tfidf.close()
    # collection.insert(currentDict)
    #
    # docs = collection.find({"comput":{'$exists':1}})
    # for readstring in docs:
    #     print readstring
    # #print db.command("dbstats")


class Searcher:
    def __init__(self, filename,sizefile):
        self.f = open(filename, 'r')
        tempsize=0
        with open(sizefile,'r') as temp:
            strings=temp.readline()
            tempsize=int(strings)
        print 'filesize '+str(tempsize)
        # self.f.seek(0, 2)
        self.length = tempsize#self.f.tell()
        self.lines = self.f.readlines()
        self.f.close()
    def find(self, string):
        low = 0
        high = self.length
        # print 'length is ' + str(high)
        found=0
        while low < high:
            mid = (low + high) / 2
            line = self.lines[mid].split()
            # print '--', mid, line[0]
            if line[0]==string:
                found=1
                break
            if line[0] < string:
                low = mid + 1
            else:
                high = mid
        if found==1:
            return line
        return []
def querymatch(s,query):

    docs = []
    dict={}
    for w in query:#.split(' '):
        print 'finding ' + w
        line= s.find(w)
        for words in line:
            if words==line[0]:
                continue
            if '/' in words:
                currentword=words
                continue
            if currentword in dict:
                dict[currentword]+=float(words)
            else:
                dict[currentword]=float(words)
    sorteddict=sorted(dict.items(),key=lambda x:x[1],reverse=True)
    return sorteddict




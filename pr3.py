import pickle
import filesort
import math
def buildInvertedIndex( wordDict, numberOfDocs):
    print "Inside index build"
    with open('pickleDict.pickle','wb') as fp:
        pickle.dump(wordDict,fp)
    with open('pickleDict.pickle','rb') as fp:
        b=pickle.load(fp)
    print b
    N = numberOfDocs
    print type(wordDict)
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
    with open('tf-idf.txt','w') as tfidf:
        with open('manualIndex.txt','r') as fp:
            tfidf.write('Word\tDocID\ttfidf\t...\n')
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
                print idf,N,df
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
                        print tf
                        linetowrite += ' ' + docid + ' ' + str(tfidfval)
                        tf=0
                tfidf.write(linetowrite)
                tfidf.write('\n')






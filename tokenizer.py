import json
from bs4 import BeautifulSoup
import re
import indexBuild
from nltk.tokenize import word_tokenize

class tokenize:
    
    dataFolder="WEBPAGES_CLEAN/"
    bookKeepingFile=dataFolder+"bookkeeping.json"
    docIDcount=0
    
    globalDictionary={}
    
    def parse(self):
        listLinkToFileMapping=self.readBookKeeping()
        i=0
        for docID,doc in listLinkToFileMapping.items():
            path=self.dataFolder+docID
            dictionaryWordPosition=self.parseFile(doc,path,docID)
            self.addToGlobalDictionary(dictionaryWordPosition,docID)
            self.docIDcount +=1
            print (self.docIDcount)
            if(self.docIDcount==10):
                break
            
    def readBookKeeping(self):
        with open(self.bookKeepingFile) as urlMappingJSON:
            linkToFileMapping = json.load(urlMappingJSON)
        return (linkToFileMapping)
    
    def getNextDocID(self):
        return self.docIDcount+1
    
#     def getText(self,docID,start,end):
        
    
    def parseFile(self,doc,path,docID):
        print("******"+path+"**********")
        file=open(path).read()
        
        #remove html tags
        docData = BeautifulSoup(file, 'lxml').get_text()
#         dictFileWordPosition={}
        if docData:
            return self.tokenize(docData)
            
    def addToGlobalDictionary(self,dictionaryWordPosition,docID):
        if dictionaryWordPosition==None:
            return
        for word,positions in dictionaryWordPosition.items():
            currentval=self.globalDictionary.get(word,[])
            currentval.append({docID:positions})
            self.globalDictionary[word]=currentval
#         print(self.globalDictionary)

    def getURL(self,docID):
        json=self.readBookKeeping()
        print(docID)
        return json[str(docID)]
    
    
    def processQuery(self,query):
        queryTokens = self.tokenize(query).keys()
        return queryTokens
    
    def tokenize(self,data):
        print("in tokenize")
#         print(data)
        
        tokens = word_tokenize(data)
#         print(tokens)
        dictTokenPosition={}
        for i in range(len(tokens)):
            #convert to lower case
            word=str(tokens[i].lower().encode("ascii","replace"))
            
            if(word.isdigit()):
                if(int(word)>1000):
                    continue
            
            #keep only alpha num characters
            word = re.sub('[^0-9a-zA-Z]+', '', word)
            
            #remove stop words
            from nltk.corpus import stopwords
            stop_words = set(stopwords.words('english'))
            
            if word in stop_words or len(word)<=1:
                continue
            
            #stemming
            # from nltk.stem.porter import PorterStemmer
            # porter = PorterStemmer()
            # word = porter.stem(word)
            
            # from nltk.stem import WordNetLemmatizer
            # lemmatiser = WordNetLemmatizer()
            # word=lemmatiser.lemmatize(word)
            
            
            from nltk.stem import SnowballStemmer
            snowball_Stemmer=SnowballStemmer("english")
            word=snowball_Stemmer.stem(word)
            
            # store word and position in dictionary
            positions=dictTokenPosition.get(word,[])
            positions.append(i)
            dictTokenPosition[str(word)]=positions
                
        # print(dictTokenPosition)
        return dictTokenPosition
        
tokenizer=tokenize()
# # tokenizer.parse()
# print(tokenizer.processQuery("graduate courses at UCI"))

# buildInvertedIndex(tokenizer.globalDictionary,tokenizer.docIDcount)
# print(tokenizer.getURL("0/100"))
s=indexBuild.Searcher('tf-idf.txt','linecount.txt')
def getqueryResult(queryterms):
    stemmed = tokenizer.processQuery(queryterms)
    print stemmed
    queryresult = indexBuild.querymatch(s,stemmed)
    count=0
    returnlist=[]
    for items in queryresult:
        if count>=5:
            break
        count+=1
        returnlist.append(tokenizer.getURL(items[0]))
    #print returnlist
    return returnlist

getqueryResult('crista lopes')
getqueryResult('andrea')
getqueryResult('graduate courses')
getqueryResult('software engineering')
getqueryResult('security')
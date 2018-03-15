import json
from bs4 import BeautifulSoup
import re
import indexBuild
import collections
# from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

class tokenize:
    
    dataFolder="WEBPAGES_CLEAN/"
    bookKeepingFile=dataFolder+"bookkeeping.json"
    docIDcount=0
    docIDTitleDict={}
    globalDictionary={}
    globalDictionaryNgram={}
    docIDTitleMapping={}
    ngramsDict={}
    
    def parse(self):
        listLinkToFileMapping=self.readBookKeeping()
        
        i=0
        for docID,doc in listLinkToFileMapping.items():
            path=self.dataFolder+docID
            
            listTokens=self.parseFile(doc,path,docID)
            dictTokenPosition=self.calPositions(listTokens,1)
            dictionaryNgram=self.calPositions(listTokens,2)
            
    
            self.addToGlobalDictionary(dictTokenPosition,docID,self.globalDictionary)
            self.addToGlobalDictionary(dictionaryNgram,docID,self.globalDictionaryNgram)
            
            print(self.globalDictionary)
            print(self.globalDictionaryNgram)
            
            self.docIDcount +=1
            if(self.docIDcount==1):
                break
            
    def tokenizeQuery(self,query,k=1):
        listTokens=self.tokenize_words(query)
        d=self.calPositions(listTokens,k)
        return d
    
    def readBookKeeping(self):
        with open(self.bookKeepingFile) as urlMappingJSON:
            linkToFileMapping = json.load(urlMappingJSON)
        return (linkToFileMapping)
    
    def getNextDocID(self):
        return self.docIDcount+1
  
    
    def parseFile(self,doc,path,docID):
        print("******"+path+"**********")
        file=open(path).read()
        #remove html tags
        soupObj = BeautifulSoup(file, 'lxml')
        docData = soupObj.get_text()
        if docData:
            title=self.getTitle(soupObj)
            self.docIDTitleMapping[str(docID)]=title
            return self.tokenize_words(docData)
        
    def getTitle(self,soupObj):
        title=soupObj.find("title")
        if(title==None):
            title=(str(soupObj.p))
        if("\n" in title):
            title=title[:str(soupObj.p).index("\n")]
        import HTMLParser
        html = HTMLParser.HTMLParser()
        title=html.unescape(title)
        title = re.sub(r'<[^>]+>','',title)
        title.replace("  ","")
        title = re.sub('[^0-9a-zA-Z ]+', '', title)
         
        #remove stop words
        from nltk.corpus import stopwords
        stop_words = set(stopwords.words('english'))
        from nltk.stem import SnowballStemmer
        snowball_Stemmer=SnowballStemmer("english")
        words=word_tokenize(title)
        for word in words:
            if word in stop_words:
                title=title.replace(word,"")
            title=title.replace(word,snowball_Stemmer.stem(word))
        return title.lower()
            
    def addToGlobalDictionary(self,dictionaryWordPosition,docID,globalDict):
        if dictionaryWordPosition==None:
            return
        for word,positions in dictionaryWordPosition.items():
            currentval=globalDict.get(word,[])
            currentval.append({str(docID):positions})
            globalDict[word]=currentval
#         print(self.globalDictionary)

    def getURL(self,docID):
        json=self.readBookKeeping()
#         print(docID)
        return json[str(docID)]
    
    
    def processQuery(self,query):
        print(self.tokenizeQuery(query))
        queryTokens = self.tokenizeQuery(query).keys()
        return queryTokens
    
    def tokenize_words(self,data):
 
        tokens = word_tokenize(data)
#         print(tokens)
        dictTokenPosition={}
        listTokens=[]
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
            
#             lemmatiser = WordNetLemmatizer()
#             word=lemmatiser.lemmatize(word)
#             listTokens.append(word)
            
            from nltk.stem import SnowballStemmer
            snowball_Stemmer=SnowballStemmer("english")
            word=snowball_Stemmer.stem(word)
            listTokens.append(word)
        return listTokens
        # print(dictTokenPosition)
        
    
    def calPositions(self,tokens,k):
        # store word and position in dictionary
        dictTokenPosition={}
        from nltk.util import ngrams
        j=0
        for ngram in ngrams(tokens, k):
            groupedTokens=' '.join(str(i) for i in ngram)
#             print(groupedTokens)
            positions=dictTokenPosition.get(groupedTokens,[])
            positions.append(j)
            j+=1
            dictTokenPosition[str(groupedTokens)]=positions
            
        return dictTokenPosition
    
    
tokenizer=tokenize()
# tokenizer.parse()
# print(tokenizer.processQuery("graduate courses at UCI"))

# buildInvertedIndex(tokenizer.globalDictionary,tokenizer.docIDcount)
# buildNGrams(tokenizer.globalDictionaryNgram,tokenizer.docIDcount)
# print(tokenizer.getURL("0/100"))

   
s=indexBuild.Searcher('tf-idf.txt','linecount.txt')
def getqueryResult(queryterms):
    stemmed = tokenizer.processQuery(queryterms)
    #print stemmed
    queryresult = indexBuild.querymatch(s,stemmed)
    count=0
    #returnlist=[]
    returnlist=collections.OrderedDict()
    for items in queryresult:
        if count>=5:
            break
        count+=1
        #returnlist.append(tokenizer.getURL(items[0]))
        if "http" in tokenizer.getURL(items[0]):
            returnlist[items[0]] = tokenizer.getURL(items[0])
        else:
            returnlist[items[0]] = "http://"+tokenizer.getURL(items[0])
    #print returnlist
    return returnlist
   
# getqueryResult('crista lopes')
# getqueryResult('andrea')
# getqueryResult('graduate courses')
# getqueryResult('software engineering')
# getqueryResult('security')
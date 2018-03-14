import json
from bs4 import BeautifulSoup
import re
import indexBuild
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

class tokenize:
    
    dataFolder="WEBPAGES_CLEAN/"
    bookKeepingFile=dataFolder+"bookkeeping.json"
    docIDcount=0
    docIDTitleDict={}
    globalDictionary={}
    docIDTitleMapping={}
    
    def parse(self):
        listLinkToFileMapping=self.readBookKeeping()
        
        i=0
        for docID,doc in listLinkToFileMapping.items():
#             docID="13/480"
            path=self.dataFolder+docID
            dictionaryWordPosition=self.parseFile(doc,path,docID)
            self.addToGlobalDictionary(dictionaryWordPosition,docID)
            self.docIDcount +=1
#             print (self.docIDcount)
            if(self.docIDcount==100):
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
        soupObj = BeautifulSoup(file, 'lxml')
#         print(soupObj)
        docData = soupObj.get_text()
#         dictFileWordPosition={}
        if docData:
            title=self.getTitle(soupObj)
            self.docIDTitleMapping[docID]=title
            print(title)
#             index=str(soupObj).index("<body>")
#             print("index=   "+str(str(soupObj).index("<body>")))
#             print("TITLE: "+str(soupObj)[:index])
            return self.tokenize(docData)
        
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
        lemmatiser = WordNetLemmatizer()
        words=word_tokenize(title)
        for word in words:
            if word in stop_words:
                title=title.replace(word,"")
            title=title.replace(word,lemmatiser.lemmatize(word))
        return title.lower()
            
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
#         print("in tokenize")
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
            
            lemmatiser = WordNetLemmatizer()
            word=lemmatiser.lemmatize(word)
            
            
#             from nltk.stem import SnowballStemmer
#             snowball_Stemmer=SnowballStemmer("english")
#             word=snowball_Stemmer.stem(word)
            
            # store word and position in dictionary
            positions=dictTokenPosition.get(word,[])
            positions.append(i)
            dictTokenPosition[str(word)]=positions
                
        # print(dictTokenPosition)
        return dictTokenPosition
        
tokenizer=tokenize()
tokenizer.parse()
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
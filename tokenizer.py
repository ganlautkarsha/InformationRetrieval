import json
from bs4 import BeautifulSoup
import re

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
            i+=1
            print (i)
#             if(i==2):
#                 break
            
    def readBookKeeping(self):
        with open(self.bookKeepingFile) as urlMappingJSON:
            linkToFileMapping = json.load(urlMappingJSON)
        return (linkToFileMapping)
    
    def getNextDocID(self):
        return self.docIDcount+1
    
    def parseFile(self,doc,path,docID):
#         print("******"+path+"**********")
        file=open(path).read()
#         .encode('ascii', 'ignore').decode('ascii')
        
        #remove html tags
        docData = BeautifulSoup(file, 'lxml').get_text()
        dictFileWordPosition={}
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
        
    def tokenize(self,data):
        print("in tokenize")
#         print(data)
        from nltk.tokenize import word_tokenize
        tokens = word_tokenize(data)
#         print(tokens)
        dictTokenPosition={}
        for i in range(len(tokens)):
            #convert to lower case
            word=str(tokens[i].lower().encode("ascii","replace"))
            
            #keep only alpha num characters
            word = re.sub('[^0-9a-zA-Z]+', '', word)
            
            #remove stop words
            from nltk.corpus import stopwords
            stop_words = set(stopwords.words('english'))
            
            if word in stop_words or len(word)<=1:
                continue
            
            #stemming
            from nltk.stem.porter import PorterStemmer#, WordNetLemmatizer
            porter = PorterStemmer()
#             lemmatiser = WordNetLemmatizer()
#             word=lemmatiser.lemmatize(word)
            word = porter.stem(word)
                       
            #store word and position in dictionary
            positions=dictTokenPosition.get(word,[])
            positions.append(i)
            dictTokenPosition[word]=positions
                
        return dictTokenPosition
        
tokenizer=tokenize()
tokenizer.parse()   
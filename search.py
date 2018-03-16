import tokenizer
import re
from bs4 import BeautifulSoup
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import collections
from flask import Flask, render_template, request, redirect

def getTitle(soupObj,url):
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
    if title.lower() != 'none':
        return title.lower()
    else:
        return url

def getText(soupObj,query,query_modified):
    soup = soupObj.get_text()
    soup = re.sub('\W',' ',soup)
    soup = soup.lower().split()
    a = '.'
    soup = [a] + [a] + [a] + soup
    soup = soup + [a] + [a] + [a] 
    if query_modified.lower() in soup:
        i = soup.index(query_modified.lower())
        string1 = ' '.join(str(e) for e in soup[i-3:i])
        string2 = ' '.join(str(e) for e in soup[i+1:i+4])
        return "..."+string1, soup[i], string2+"..."
    else:
        return "...",query,"..."

def getBigramText(soupObj,query,query_modified):
    soup = soupObj.get_text()
    soup = re.sub('\W',' ',soup)
    soup = soup.lower().split()
    a = '.'
    soup = [a] + [a] + [a] + soup
    soup = soup + [a] + [a] + [a]
    if query_modified[0].lower() in soup and query_modified[1].lower() in soup:
        indices = [i for i, x in enumerate(soup) if x == query_modified[0].lower()]
        for index in indices:
            if soup[index+1] == query_modified[1].lower():
                string1 = ' '.join(str(e) for e in soup[index-3:index])
                string2 = ' '.join(str(e) for e in soup[index+2:index+4])
                return "..."+string1, soup[index]+" "+soup[index+1], string2+"..."
                break
        string1 = ' '.join(str(e) for e in soup[indices[0]-3:indices[0]])
        string2 = ' '.join(str(e) for e in soup[indices[0]+1:indices[0]+4])
        return "..."+string1, soup[indices[0]], string2+"..."
    elif query_modified[0].lower() in soup:
        i = soup.index(query_modified[0].lower())
        string1 = ' '.join(str(e) for e in soup[i-3:i])
        string2 = ' '.join(str(e) for e in soup[i+1:i+4])
        return "..."+string1, soup[i], string2+"..."
    elif query_modified[1].lower() in soup:
        i = soup.index(query_modified[1].lower())
        string1 = ' '.join(str(e) for e in soup[i-3:i])
        string2 = ' '.join(str(e) for e in soup[i+1:i+4])
        return "..."+string1, soup[i], string2+"..."
    else:
        return "...",query,"..."

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('search.html')

@app.route('/search', methods = ['POST'])
def search():
    query = request.form['query']
    
    url_dict = collections.OrderedDict()
    titles = collections.OrderedDict()

    url_dict = tokenizer.getqueryResult(query)
    
    for docID,url in url_dict.items():
        path="WEBPAGES_CLEAN/"+docID
        file=open(path).read()
        soup = BeautifulSoup(file, 'lxml')
        titles[url] = [getTitle(soup,url)]
        if len(query.split()) == 2:
            query_modified = query.split()
            str1, str2, str3 = getBigramText(soup,query,query_modified)
        else:
            query_modified = query.split()[0]
            str1, str2, str3 = getText(soup,query,query_modified)
        titles[url].append(str1)
        titles[url].append(str2)
        titles[url].append(str3)
    
    return render_template('results.html',query = query,titles = titles)

if __name__ == "__main__":
    app.run()

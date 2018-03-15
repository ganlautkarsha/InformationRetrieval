import urllib2
import tokenizer
import re
from bs4 import BeautifulSoup
import collections
from flask import Flask, render_template, request, redirect
app = Flask(__name__)

@app.route('/')
def main():
    return render_template('search.html')

@app.route('/search', methods = ['POST'])
def search():
    query = request.form['query']
    query_modified = query.split()[0]

    url_dict = collections.OrderedDict()
    titles = collections.OrderedDict()

    url_dict = tokenizer.getqueryResult(query)
    
    for docID,url in url_dict.items():
        path="WEBPAGES_CLEAN/"+docID
        file=open(path).read()
        
        title_soup = BeautifulSoup(urllib2.urlopen(url),'lxml')
        titles[url] = [title_soup.title.string]
        
        soup = BeautifulSoup(file, 'lxml').get_text()
        soup = re.sub('\W',' ',soup)
        soup = soup.lower().split()
        
        a = '.'
        soup = [a] + [a] + [a] + soup
        soup = soup + [a] + [a] + [a]
        
        i = soup.index(query_modified)
        
        string1 = ' '.join(str(e) for e in soup[i-3:i])
        string2 = ' '.join(str(e) for e in soup[i+1:i+4])
        titles[url].append("..."+string1+" "+soup[i]+" "+string2+"...")
    
    return render_template('results.html',query = query,titles = titles)

if __name__ == "__main__":
    app.run()

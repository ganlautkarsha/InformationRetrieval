import urllib2
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, redirect
app = Flask(__name__)

@app.route('/')
def main():
    return render_template('search.html')

@app.route('/search', methods = ['POST'])
def search():
    query = request.form['query']
    #soup = BeautifulSoup(urllib2.urlopen(query))
    url_list = ['http://www.ics.uci.edu/','http://www.ics.uci.edu/about/','http://www.ics.uci.edu/dept/','http://www.ics.uci.edu/faculty/area/','http://www.ics.uci.edu/grad/admissions/index']
    titles = {}
    for item in url_list:
    	title_soup = BeautifulSoup(urllib2.urlopen(item))
    	titles[item] = title_soup.title.string

    #return render_template('results.html',query=soup.title.string, url = query, titles = titles)
    return render_template('results.html',titles = titles)

if __name__ == "__main__":
    app.run()

from flask import Flask, render_template, request, redirect
app = Flask(__name__)

@app.route('/')
def main():
    return render_template('search.html')

@app.route('/search', methods = ['POST'])
def search():
    query = request.form['query']
    return render_template('results.html',query=query)

if __name__ == "__main__":
    app.run()

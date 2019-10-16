import pymongo
from flask import Flask, render_template
from scrape import scrape

app = Flask(__name__)


conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.mars_db

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape')
def scraped():
    db.mars.drop()
    db.mars.insert_one(scrape())
    return render_template('index.html', elems=list(db.mars.find())[0])



if __name__ == "__main__":
    app.run(debug=True)
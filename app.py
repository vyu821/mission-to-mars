# import dependencies
from flask import Flask, render_template
from flask_pymongo import flask_pymongo
import scraping

# set up flask app instance
app = Flask(__name__)

# use flask_pymongo to set up mongo connection
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mars_app'
mongo = PyMongo(app)

# first route
@app.route('/')
# function links our visual representation of our work, our web app, to the code that powers it
def index():
    # uses pymongo to find 'mars' collection in our database
    mars = mongo.db.mars.find_one()
    # return html template using index.html file, use 'mars' collection in mongodb
    return render_template('index.html', mars = mars)

# scrape route
@app.route('/scrape')
def scrape():
    # uses pymongo to find 'mars' collection in our database
    mars = mongo.db.mars
    # scrape new data using our scraping.py
    mars_data = scraping.scrape_all()
    # .update(query_parameter, data, options)
    # updates database, inserting data, first parameter is empty JSON object {}
    # use the data stored in mars_data
    # upsert indicates to mongo to create a new doc if one doesn't already exist, and new data will always be saved
    mars.update({}, mars_data, upsert = True)
    return 'Scraping Successful'

# tells Flask to run
if __name__ == "__main__":
   app.run()
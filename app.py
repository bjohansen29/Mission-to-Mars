from flask import Flask, render_template, redirect, url_for
#use flask to make a template, redirecting to another url, and creating a url
from flask_pymongo import PyMongo
#use PyMongo to interact with Mongo db
import scraping
#to use the scraping code, convert from ipynb to py


#set up flask
app = Flask(__name__)

#tell Python how to connect to Mongo using PyMongo
#Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
#tells Python app will connect to Mongo using a URI (uniform resource identifier)
#"mongodb://localhost:27017/mars_app" is the URI to connect app to Mongo
#tells app to reach Mongo through localhost server, port 27017, database named mars_app
mongo = PyMongo(app)

#define route for html page
@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    #mars = mongo.db.mars.find_one() uses PyMongo to find the "mars" collection 
    # in our database, which we will create when we convert our Jupyter scraping 
    # code to Python Script. We will also assign that path to themars variable for use later.
    return render_template("index.html", mars=mars)
    #return render_template("index.html" tells Flask to return an HTML template using 
    # an index.html file. We'll create this file after we build the Flask routes.
    #, mars=mars) tells Python to use the "mars" collection in MongoDB.

#define scrape route
@app.route("/scrape")
def scrape():
#define the scrape
   mars = mongo.db.mars
    #assign a new variable pointing to Mongo db
   mars_data = scraping.scrape_all()
   #create a new variable to hold scraped data (referincing the scrape_all function inside the scraping.py file)
   mars.update_one({}, {"$set":mars_data}, upsert=True)
   #update the db
   return redirect('/', code=302)

if __name__ == "__main__":
   app.run()
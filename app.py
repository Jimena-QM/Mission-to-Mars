#Dependencies
#use Flask to render a template, redirecting to another url, and creating a URL
from flask import Flask, render_template, redirect, url_for
#use PyMongo to interact with our Mongo database
from flask_pymongo import PyMongo
#use the scraping code, we will convert from Jupyter notebook to Python
import Scraping
import os
from flask import send_from_directory

#set up Flask
app = Flask(__name__)
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')
#Use flask_pymongo to set up mongo connection
#tells Python that our app will connect to Mongo using a URI, 
# a uniform resource identifier similar to a URL.
#the URI we'll be using to connect our app to Mongo. This URI is 
# saying that the app can reach Mongo through our localhost server, 
# using port 27017, using a database named "mars_app"
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

#Setting up App Routes
#tells Flask what to display when we're looking at the home page, index.html
@app.route("/")
#This function is what links our visual representation 
# of our work, our web app, to the code that powers it.
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)
#Adding Scraping Route
#This route will be the "button" of the web application, the one that will scrape 
# updated data when we tell it to from the homepage of our web app. It'll be tied 
# to a button that will run the code when it's clicked.
@app.route("/scrape")

def scrape():
    mars = mongo.db.mars
    mars_data = Scraping.scrape_all()
    mars.update_one({}, {"$set": mars_data}, upsert=True)
    return redirect('/', code=302)

if __name__ == "__main__":
    app.run()
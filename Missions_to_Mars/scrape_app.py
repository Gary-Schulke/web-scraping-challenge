#!/usr/bin/env python
# coding: utf-8

# Assignment: web-scraping-challenge
# Gary Schulke 11/27/2019

from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")


# Route to render index.html template using data from Mongo
# Uses existing data in Mongo, database: mars_db, container: marsdata
# This also gets called following /scrape
@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars_data = mongo.db.marsdata.find_one()

    # Return template and data
    return render_template("index.html", marsdata=mars_data)


# Route that will trigger the scrape function and put it in Mongo.
# Stores data in Mongo, database: mars_db, container: marsdata
# Calls / when complete
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_data = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mongo.db.marsdata.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")

# This starts the server and should be the main module.
if __name__ == "__main__":
    app.run(debug=True)

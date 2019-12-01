#!/usr/bin/env python
# coding: utf-8

# Assignment: web-scraping-challenge
# Gary Schulke 11/27/2019

# Import BeautifulSoup
from bs4 import BeautifulSoup


# Import Splinter and set the chromedriver path
from splinter import Browser
from time import sleep
# A Mac Thing
#executable_path = {"executable_path": "/usr/local/bin/chromedriver"}

#PC chromedriver path set in environment path
executable_path = {"executable_path": "chromedriver"}
browser = Browser("chrome", **executable_path, headless=True)

# Visit the NASA Mars News URL
def get_mars_news():
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    news_title = soup.find("div", class_="content_title").text
    news_p = soup.find("div", class_="article_teaser_body").text
    return([{'news_title': news_title}, {'news_p': news_p}])


# ## Mars Featured Image
# Scrape the browser into soup and use soup to find the full resolution image of Mars
# Returns string (url)
def get_featured_image():
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    sleep(1)
    browser.click_link_by_partial_text('FULL')
    sleep(1)
    xpath = "//*[@id='fancybox-lock']/div/div[1]/img"
    xpic = browser.find_by_xpath(xpath)
    featured_image_url = xpic['src']
    return featured_image_url


# ## Mars Weather Tweet
# Gets the latest Mars weather.
# Returns a string.
def get_mars_weather():
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    tweet = soup.find("div", class_="js-tweet-text-container")
    mars_weather = tweet.find("p").text
    return mars_weather

# ## Mars Facts

# Gets the basic planitary facts about mars.
# Returns a list of lists[heading, descroptive text]
def get_mars_facts():
    url = "https://space-facts.com/mars/"
    browser.visit(url)
    sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Step through each section until we get to the table.
    side_bar = soup.find("section", class_="sidebar")
    side_bar = side_bar.find("aside", class_="widget")
    side_bar = side_bar.find("div", class_="textwidget")
    side_bar = side_bar.find("table")
    side_bar = side_bar.find("tbody")
    heading_list = [each.find("td", class_="column-1").get_text()
                    for each in side_bar]
    value_list = [each.find("td", class_="column-2").get_text()
                  for each in side_bar]
   # mars_table = zip(heading_list, value_list)
    mars_table = list(map(list, zip(heading_list, value_list)))
    return mars_table
# ## Mars Hemispheres

# Finds the four Mars hemisphere pictures.
# Returns a list of dictionaries
def get_mars_hemispheres():
    base_url = 'https://astrogeology.usgs.gov'
    cerberus_url = "https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced"
    schiaparelli_url = "https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced"
    syrtis_url = "https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced"
    valles_url = "https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced"
    hemi_urls = [cerberus_url, schiaparelli_url, syrtis_url, valles_url]
    hemisphere_image_urls = []

    for each_hemi in hemi_urls:
        browser.visit(each_hemi)
        sleep(1)    # Time in seconds
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find('h2', class_="title").text
        img_url = base_url + soup.find("img", class_="wide-image")['src']
        hemisphere_image_urls.append({'title': title, 'img_url': img_url})

    return hemisphere_image_urls

# Calls all the scrape functions and assembles it into the document format for Mongodb.
# Returns one Mongo document.
# scrape_app.py stores the return in Mongo.
def scrape():
    news = get_mars_news()
    featured = get_featured_image()
    weather = get_mars_weather()
    facts = get_mars_facts()
    hemi = get_mars_hemispheres()

    final_dict = {}
    final_dict.update(news[0])
    final_dict.update(news[1])
    final_dict['featured_image'] = featured
    final_dict['weather'] = weather
    final_dict['facts'] = facts
    final_dict['hemispheres'] = hemi

    return final_dict

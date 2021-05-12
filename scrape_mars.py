#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Dependencies
from bs4 import BeautifulSoup as bs
import requests
import os
from splinter import Browser
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from pprint import pprint
import pymongo
from flask import Flask, render_template
import time
import numpy as np
import json
from selenium import webdriver
# In[2]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[3]:

def news_url (browser):
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    #print(soup.prettify())
    try:
        elem = soup.select_one("ul.item_list li.slide")
        newstitle = elem.find("div", class_="content_title").get_text()
        newspara = elem.find("div", class_="article_teaser_body").get_text()
    except:
        return " "
    return newstitle, newspara

# ## News Titles and paragraph

# In[4]:


latest_title = soup.find('div', class_="content_title").get_text()
latest_para = soup.find('div', class_="rollover_description_inner").get_text()
print("Title: {}".format(latest_title))
print("Description: {}".format(latest_para))


# # JPL Mars Space Images - Featured Image


#Use splinter to navigate the site 
#browser.visit('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')

url="https://www.jpl.nasa.gov/images?search=&category=Mars"
response =requests.get(url)
soup = bs(response.text, 'html.parser')
#print(soup.prettify())


#find the image url for the current Featured Mars Image 
image = soup.find('div', class_='sm:object-cover object-cover')

for featured in image:
    featured_image_url = featured.get('data-src')

print(f"featured_image_url: {featured_image_url}")


# # Mars Facts 



#Visit the Mars Facts webpage
mars_facts_url = "https://space-facts.com/mars/"
table = pd.read_html(mars_facts_url)
table[0]



#use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
#type(table)
mars_df = pd.DataFrame(table[0])
mars_df .columns = ["Facts", "Value"]
mars_df .set_index(["Facts"])
mars_df



#Use Pandas to convert the data to a HTML table string.
converted_to_html = mars_df.to_html()
print(converted_to_html)


# # Mars Hemispheres  

#Visit the USGS Astrogeology site
url_hem = ('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')
browser.visit(url_hem)



import time 
html = browser.html
soup = bs(html, 'html.parser')
#print(soup.prettify())


mars_hemisphere=[]



# loop through the four tags and load the data to the dictionary
links = browser.find_by_css("a.product-item h3")

for i in range (len(links)):
    link_dict= {}
    browser.find_by_css("a.product-item h3")[i].click()
    sample_list = browser.links.find_by_text('Sample').first
    link_dict['img_url'] = sample_list['href']
    link_dict['title'] = browser.find_by_css("h2.title").text
    mars_hemisphere.append(link_dict)  
    browser.back()
mars_hemisphere    

mars_data= {}
def mars_news_scrape():
     browser = init_browser()
    #Visit Nasa News url  using splinter module

     Nasa_url = 'https://mars.nasa.gov/news/'
     browser.visit(Nasa_url)
     #create HTMl Object
     html = browser.html
     #parse HTML with beautiful soup
     Nasa_soup = bs(html, 'html.parser')

     # Extract title text
     nasa_news_title = Nasa_soup.find('div',class_='content_title').find('a').text
     print(f"title {nasa_news_title}")
     mars_data['nasa_news_title']=nasa_news_title
     # Extract Paragraph text
     nasa_news_paragraph=Nasa_soup.find('div',class_='article_teaser_body').text
     mars_data['nasa_news_paragraph'] = nasa_news_paragraph
     #print(nasa_news_paragraph)
     print(f"paragraph {nasa_news_paragraph}")

     return mars_data
     
def img_scrape():
     browser = init_browser()
     #Visit Nasa's JPL Mars Space url  using splinter module
     jplNasa_url='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
     browser.visit(jplNasa_url)
     #create HTML object
     html = browser.html
     soup = bs(html, 'html.parser')

     #get base Nasa link
     main_url ='https://www.jpl.nasa.gov'
     #get image url from the soup object.
     featured_image_url = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

     #Create one full image url link
     full_image_url=main_url+featured_image_url
     mars_data['full_image_url']= full_image_url
     print(full_image_url )     

     return mars_data


def mars_weather():
     browser = init_browser()
     #Visit the Mars Weather twitter account
     Tweet_url='https://twitter.com/marswxreport?lang=en'
     # Retrieve page with the requests module
     browser.visit(Tweet_url)
     #create HTML object
     html=browser.html
     twit_soup=bs(html,'html.parser')

     # Extract title text
     mars_data['mars_weather'] = twit_soup.find('p',class_='TweetTextSize').text
     #print('mars_weather = '+ mars_weather.text)
     return mars_data

def mars_facts():
     # Visit the Mars Facts webpage
     mars_facts_url='https://space-facts.com/mars/'
     mars_fact_table=pd.read_html(mars_facts_url)

     #Create Dataframe to store table data
     df = mars_fact_table[0]
     df.columns = ['Mars-Earth Comparison', 'Mars', 'Earth']
     mars_facts = df.to_html()
     mars_data['mars_facts'] = mars_facts
     return mars_data


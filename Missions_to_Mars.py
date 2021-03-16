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


# In[2]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[3]:


url = 'https://mars.nasa.gov/news/'
response = requests.get(url)
soup = bs(response.text, 'html.parser')
#print(soup.prettify())


# ## News Titles and paragraph

# In[4]:


latest_title = soup.find('div', class_="content_title").get_text()
latest_para = soup.find('div', class_="rollover_description_inner").get_text()
print("Title: {}".format(latest_title))
print("Description: {}".format(latest_para))


# # JPL Mars Space Images - Featured Image

# In[14]:


#Use splinter to navigate the site 
#browser.visit('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')

url="https://www.jpl.nasa.gov/images?search=&category=Mars"
response =requests.get(url)
soup = bs(response.text, 'html.parser')
#print(soup.prettify())


# In[15]:


#find the image url for the current Featured Mars Image 
image = soup.find('div', class_='sm:object-cover object-cover')

for featured in image:
    featured_image_url = featured.get('data-src')

print(f"featured_image_url: {featured_image_url}")


# # Mars Facts 

# In[7]:


#Visit the Mars Facts webpage
mars_facts_url = "https://space-facts.com/mars/"
table = pd.read_html(mars_facts_url)
table[0]


# In[8]:


#use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
#type(table)
mars_df = pd.DataFrame(table[0])
mars_df .columns = ["Facts", "Value"]
mars_df .set_index(["Facts"])
mars_df


# In[9]:


#Use Pandas to convert the data to a HTML table string.
converted_to_html = mars_df.to_html()
print(converted_to_html)


# # Mars Hemispheres  

# In[31]:


#Visit the USGS Astrogeology site
url_hem = ('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')
browser.visit(url_hem)


# In[32]:


import time 
html = browser.html
soup = bs(html, 'html.parser')
#print(soup.prettify())


mars_hemisphere=[]


# In[36]:



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


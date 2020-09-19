#!/usr/bin/env python
# coding: utf-8

# In[1]:


# import splinter and beautifulsoup
from splinter import Browser
from bs4 import BeautifulSoup as soup

import pandas as pd


# In[2]:


# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path)


# In[3]:


# mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# In[4]:


# html parser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')


# In[5]:


# find article title
slide_elem.find("div", class_='content_title')


# In[6]:


# Use the parent element to find the first `a` tag and save it as `news_title`
# get_text() returns only texst and not any of the html tags or elements
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


# In[7]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p


# ### Featured Images

# In[8]:


# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)


# In[9]:


# Find and click the full image button
# variable to hold scraping result, browser finds element by its id
full_image_elem = browser.find_by_id('full_image')
# splinter will click the image
full_image_elem.click()


# In[10]:


# Find the more info button and click that
# search for an element that has "more info" text
browser.is_element_present_by_text('more info', wait_time=1)
# take our string "more info" to find the link associated with the "more info" text
more_info_elem = browser.links.find_by_partial_text('more info')
# splinter will click the link
more_info_elem.click()


# In[11]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[12]:


# Find the relative image url
# look inside <figure class="lede" /> tag for an <a /> tag, then look within that <a /> tag 
# for an <img /> tag
img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel


# In[13]:


# Use the base URL to create an absolute URL
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url


# In[14]:


# finds and returns list of tables found in the html, index 0 for the first table
df = pd.read_html('http://space-facts.com/mars/')[0]
# assign column names
df.columns=['description', 'value']
# turning description column into the df's index, inplace=true means updated index will remain in place
# without having to reassign df to new variable
df.set_index('description', inplace=True)
df


# In[15]:


# convert df back to html-ready code
df.to_html()


# In[16]:


# end automated browsing session
browser.quit()


# # Challenge

# In[20]:


# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd


# In[21]:


# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path)


# ### Visit the NASA Mars News Site

# In[22]:


# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# In[23]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('ul.item_list li.slide')


# In[24]:


slide_elem.find("div", class_='content_title')


# In[25]:


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


# In[26]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p


# ### JPL Space Images Featured Image

# In[27]:


# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)


# In[28]:


# Find and click the full image button
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()


# In[29]:


# Find the more info button and click that
browser.is_element_present_by_text('more info', wait_time=1)
more_info_elem = browser.links.find_by_partial_text('more info')
more_info_elem.click()


# In[30]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[31]:


# find the relative image url
img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel


# In[32]:


# Use the base url to create an absolute url
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url


# ### Mars Facts

# In[33]:


df = pd.read_html('http://space-facts.com/mars/')[0]

df.head()


# In[34]:


df.columns=['Description', 'Mars']
df.set_index('Description', inplace=True)
df


# In[35]:


df.to_html()


# ### Mars Weather

# In[36]:


# Visit the weather website
url = 'https://mars.nasa.gov/insight/weather/'
browser.visit(url)


# In[37]:


# Parse the data
html = browser.html
weather_soup = soup(html, 'html.parser')


# In[38]:


# Scrape the Daily Weather Report table
weather_table = weather_soup.find('table', class_='mb_table')
print(weather_table.prettify())


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[138]:


# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# In[139]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
# Parse the resulting html with soup
html = browser.html
hemi_soup = soup(html, 'html.parser')

# holds all the tags that contain links to the images
all_pics = hemi_soup.find_all('div', class_='description')
# counter to iterate through h3 tags
i = 0

# loops through the tags
for pic in all_pics:
    
    # empty dictionary to hold title and full-res image URL string of each hemisphere iamge
    hemispheres = {}
    # finds all h3 tags, these contain the links
    element = browser.find_by_tag('h3')
    # checks to see if browser has loaded
    if browser.is_element_present_by_tag('h3'):
        
        # gets the title of each hemisphere image
        title = element[i].text
        # clicks the link to the full-res image
        element[i].click()
        # parse the second page containing the full-res image
        html_2 = browser.html
        hemi_2_soup = soup(html_2, 'html.parser')
        
        # holds all tags that contain the link
        full_res = hemi_2_soup.find('div', class_='downloads')
        # gets the full-res image URL
        image = full_res.find('a')['href']
        
        # create dictionay with title and URL
        hemispheres['img_url'] = image
        hemispheres['title'] = title
        # updates list with dictionary
        hemisphere_image_urls.append(hemispheres)
        
    # add one for the next tag    
    i = i + 1
    # go back to main page for next image
    browser.back()


# In[140]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[141]:


# 5. Quit the browser
browser.quit()


# In[ ]:





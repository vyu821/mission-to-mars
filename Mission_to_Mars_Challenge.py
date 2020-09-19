# import splinter and beautifulsoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd

# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path)

# Challenge

### Visit the NASA Mars News Site

# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('ul.item_list li.slide')

slide_elem.find("div", class_='content_title')

# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()


### JPL Space Images Featured Image

# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()

# Find the more info button and click that
browser.is_element_present_by_text('more info', wait_time=1)
more_info_elem = browser.links.find_by_partial_text('more info')
more_info_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# find the relative image url
img_url_rel = img_soup.select_one('figure.lede a img').get("src")

# Use the base url to create an absolute url
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'


# ### Mars Facts

df = pd.read_html('http://space-facts.com/mars/')[0]

df.columns=['Description', 'Mars']
df.set_index('Description', inplace=True)

df.to_html()


### Mars Weather

# Visit the weather website
url = 'https://mars.nasa.gov/insight/weather/'
browser.visit(url)

# Parse the data
html = browser.html
weather_soup = soup(html, 'html.parser')

# Scrape the Daily Weather Report table
weather_table = weather_soup.find('table', class_='mb_table')
#print(weather_table.prettify())


# D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

### Hemispheres

# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)

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

# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls

# 5. Quit the browser
browser.quit()




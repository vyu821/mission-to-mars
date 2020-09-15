# import splinter and beautifulsoup
from splinter import Browser
from bs4 import BeautifulSoup as soup

import pandas as pd

# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path)

# mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

# html parser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')

# find article title
slide_elem.find("div", class_='content_title')

# Use the parent element to find the first `a` tag and save it as `news_title`
# get_text() returns only texst and not any of the html tags or elements
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p

### Featured Images

# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)

# Find and click the full image button
# variable to hold scraping result, browser finds element by its id
full_image_elem = browser.find_by_id('full_image')
# splinter will click the image
full_image_elem.click()

# Find the more info button and click that
# search for an element that has "more info" text
browser.is_element_present_by_text('more info', wait_time=1)
# take our string "more info" to find the link associated with the "more info" text
more_info_elem = browser.links.find_by_partial_text('more info')
# splinter will click the link
more_info_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative image url
# look inside <figure class="lede" /> tag for an <a /> tag, then look within that <a /> tag 
# for an <img /> tag
img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel

# Use the base URL to create an absolute URL
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url

# finds and returns list of tables found in the html, index 0 for the first table
df = pd.read_html('http://space-facts.com/mars/')[0]
# assign column names
df.columns=['description', 'value']
# turning description column into the df's index, inplace=true means updated index will remain in place
# without having to reassign df to new variable
df.set_index('description', inplace=True)
df

# convert df back to html-ready code
df.to_html()

# end automated browsing session
browser.quit()



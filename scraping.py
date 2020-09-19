# import splinter and beautifulsoup
from splinter import Browser
from bs4 import BeautifulSoup as soup

import pandas as pd
import datetime as dt

# function that initializes browser
# create data dictionary
# end webdriver and return scraped data
def scrape_all():

    # Set the executable path and initialize the chrome browser in splinter
    browser = Browser('chrome', executable_path = 'chromedriver', headless = True)
    # use mars_news function to pull this data
    news_title, news_paragraph = mars_news(browser)

    # data dictionary
    data = {
        'news_title': news_title,
        'news_paragraph': news_paragraph,
        'featured_image': feature_image(browser),
        'facts': mars_facts(),
        'last_modified': dt.datetime.now(),
        'hemispheres': mars_hemis(browser)
    }

    # stop webdriver and return data
    # end automated browsing session
    browser.quit()
    return data

# function that returns news title and paragraph
def mars_news(browser):

    # visit mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # convert browser html to soup object, then quit browser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    # add try/except for error handling
    try:

        slide_elem = news_soup.select_one('ul.item_list li.slide')

        # find article title
        # Use the parent element to find the first `a` tag and save it as `news_title`
        # get_text() returns only texst and not any of the html tags or elements
        news_title = slide_elem.find("div", class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None

    return news_title, news_p

# function that returns the featured image
def feature_image(browser):

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

    # try/except for errors
    try:

        # Find the relative image url
        # look inside <figure class="lede" /> tag for an <a /> tag, then look within that <a /> tag 
        # for an <img /> tag
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
    
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'

    return img_url

# function that returns mars facts
def mars_facts():

    # try/except for errors
    try:
        # finds and returns list of tables found in the html, index 0 for the first table
        df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
        return None
    
    # assign column names
    df.columns=['description', 'value']
    # turning description column into the df's index, inplace=true means updated index will remain in place
    # without having to reassign df to new variable
    df.set_index('description', inplace=True)

    # convert df back to html-ready code
    return df.to_html(classes="table table-striped")

# function that returns hemisphere data
def mars_hemis(browser):
    
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # list to hold the images and titles.
    hemisphere_image_urls = []

    # retrieve the image urls and titles for each hemisphere.
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

    return hemisphere_image_urls

# tells Flask our script is complete and ready for action
if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())
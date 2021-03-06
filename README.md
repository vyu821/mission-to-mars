# Mission to Mars

## Challenge Overview
You are to create a web app that displays information you have scraped about Mars. This information includes the most recent news article, a featured image, mars facts, and pictures of mars' hemispheres.

## Resources
- [Nasa Mars News](https://mars.nasa.gov/news/), [JPL Mars Images](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars), [Mars Facts](http://space-facts.com/mars/), [Mars Hemispheres](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars)
- Software: Jupyter Notebook 6.0.3, Python 3.7.7, Visual Studio Code 1.47.2, MongoDB 4.4.1, Flask 1.1.2

## Challenge Summary
We have sucessfully automated the [scraping](/scraping.py) process of the Mars data. We then stored the data onto a Mongo database and used [Flask](/app.py) to display the data. We also altered the [design](templates/index.html) of the web app to accomadate the hemisphere images.
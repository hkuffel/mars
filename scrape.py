import pandas as pd
import requests
from bs4 import BeautifulSoup
from splinter import Browser

executable_path = {'executable_path': '/venv/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)

def news():
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    title = soup.find('div', class_='content_title').find('a').text
    dek = soup.find('div', class_='article_teaser_body').text
    return title, dek

def featured_image():
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    footers = soup.find_all('footer')
    fimg = footers[0].find('a')
    return 'https://www.jpl.nasa.gov' + fimg.get('data-fancybox-href')

def weather():
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    mars_weather = soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')
    return mars_weather.text

def facts():
    url = 'https://space-facts.com/mars/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    facts = soup.find(id='tablepress-comp-mars')
    df = pd.read_html(str(facts))[0].rename(columns={'Mars - Earth Comparison': 'Metric', 'Mars': 'Mars', 'Earth': 'Earth'})
    df = df.set_index('Metric').drop('Earth', axis = 1)
    mt = df.to_html()
    mt = mt[197:-9].replace('\n', '')
    return mt

def hemispheres():
    hem_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hem_url)
    hemispheres = []
    hem_names = ['Cerberus', 'Valles Marineris', 'Schiaparelli', 'Syrtis Major']
    for hem in hem_names:
        browser.click_link_by_partial_text(hem)
        himg = browser.find_by_text('Sample').first
        hemispheres.append({'title': f'{hem} Hemisphere', 'img_url': himg['href']})
    return hemispheres

def scrape():
    elems = {'title': news()[0], 'dek': news()[1],
    'featured_image': featured_image(),
    'weather': weather(), 'facts': facts(), 
    'hemispheres': hemispheres()}
    return elems
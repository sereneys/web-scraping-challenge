    #!/usr/bin/env python
    # coding: utf-8
import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests
import re
import time

import sys

if not sys.warnoptions:
   import warnings
   warnings.simplefilter("ignore")


def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():

    browser = init_browser()
    # # Scraping NASA Mars News

    # In[3]:


    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    


    # In[4]:


    time.sleep(2)
    news_html = browser.html
    news_soup = bs(news_html, 'html.parser')


    # In[5]:


    titles = news_soup.find_all("div", class_="content_title")
    articles = news_soup.find_all("div", class_="article_teaser_body")


    # In[6]:


    news_title = titles[1].text
    news_p = articles[0].text


    # In[7]:


    results_dic = {"news_title":news_title, "news_p":news_p}


    # # JPL Mars Space Images - Featured Image

    # In[8]:


    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    time.sleep(1)

    # In[9]:


    image_html = browser.html
    image_soup = bs(image_html,'html.parser')


    # In[10]:


    image_result = image_soup.find("a", class_="button fancybox")


    # In[11]:


    featured_image_url = "https://www.jpl.nasa.gov" + image_result["data-fancybox-href"]


    # In[12]:


    results_dic["featured_image_url"] = featured_image_url


    # # Mars Weather

    # In[13]:


    weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)
    time.sleep(2)


    # In[14]:


    weather_html = browser.html
    weather_soup = bs(weather_html,'lxml')


    # In[15]:


    pattern = re.compile(r'InSight sol')
    mars_weather = weather_soup.find('span', text=pattern).text

    # In[16]:


    results_dic["mars_weather"] = mars_weather


    # # Mars Facts

    # In[17]:


    facts_url = "https://space-facts.com/mars/"


    # In[18]:


    tables = pd.read_html(facts_url)
    fact_df = tables[0]


    # In[19]:


    fact_df


    # In[20]:


    html_table = fact_df.to_html(index = False, header=False)

    results_dic["html_table"] = html_table


    # In[21]:


    html_table


    # # Mars Hemispheres

    # In[22]:


    hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemi_url)
    time.sleep(1)

    # In[23]:


    hemi_list = ["Cerberus", "Schiaparelli", "Syrtis Major", "Valles Marineris"]


    # In[24]:


    hemisphere_image_urls = []

    for hemi in hemi_list:
        
        browser.click_link_by_partial_text(hemi)
        
        hemi_html = browser.html
        hemi_soup = bs(hemi_html,'html.parser')
       
        img_url = hemi_soup.find_all("li")[0].a["href"]
        title = hemi + " Hemisphere"
        
        hemisphere_image_urls.append({"title":title, "img_url":img_url})


    # In[25]:


    results_dic["hemi_img_urls"] = hemisphere_image_urls


   # Quite the browser after scraping
    browser.quit()

    return(results_dic)


    # In[ ]:





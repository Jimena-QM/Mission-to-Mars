#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Splinter and BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[2]:


# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site

# In[3]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[4]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# In[5]:


slide_elem.find('div', class_='content_title')


# In[6]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[7]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### JPL Space Images Featured Image

# In[8]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[9]:


# Find and click the full image button. The [1] we tell the browser that we want it to click the second element.
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[10]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# In[11]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[12]:


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts

# In[13]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df


# In[14]:


df.to_html()


# ### D1: Scrape High-Resolution Mars' Hemisphere Images and Titles

# ## Hemispheres

# In[15]:


# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

browser.visit(url)


# In[16]:


# Parse the data
hemisphere_html = browser.html
hemisphere_soup = soup(hemisphere_html, 'html.parser')


# In[17]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []
url_main = "https://astrogeology.usgs.gov/"
# 3. Write code to retrieve the image urls and titles for each hemisphere.
# Retrieve all hemispheres information items 
items = hemisphere_soup.find_all('div', class_='item')

for i in items:
    hemisphere = {}
    titles = i.find('h3').text
    # Link for full image
    link_reference = i.find('a', class_='itemLink product-item')['href']
    # Use the base URL to create an absolute URL and browser visit
    browser.visit(url_main + link_reference)
    # Parse Data
    image_html = browser.html
    image_soup = soup(image_html, 'html.parser')
    download = image_soup.find('div', class_= 'downloads')
    img_url = download.find('a')['href']
    # append list
    hemisphere['img_url'] = img_url
    hemisphere['title'] = titles
    hemisphere_image_urls.append(hemisphere)
    browser.back()


# In[18]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[19]:


# 5. Quit the browser
browser.quit()


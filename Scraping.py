
    # Import Splinter and BeautifulSoup\n"
    
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

#-------Code prior to adding functions
#Set up executable path
#executable_path = {'executable_path': ChromeDriverManager().install()}
#browser = Browser('chrome', **executable_path, headless=False)
#---------

#Function to initalize the browser, create a data dictionary and end the WebDriver and
#return the scraped data
def scrape_all():
    #Initiate headless driver for deployemnt
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
#Set up executable path
#executable_path = {'executable_path': ChromeDriverManager().install()}
#browser = Browser('chrome', **executable_path, headless=False)
    news_title, news_paragraph = mars_news(browser)
    #Run all scraping functions and store results in dictionary
    data = {
        'news_title': news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemispheres(browser),
        "last_modified": dt.datetime.now()
    }
    #Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)
    #Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    #Add trye/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        #The specific data is in a <div /> with a class of 'content_title'"
        slide_elem.find('div', class_='content_title')
        
        # Use the parent element to find the first `a` tag and save it as `news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None

    return news_title, news_p

# ## JPL Spac Images Featured
def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)
    
    # Find and click the full image button. The [1] we tell the browser that we want it to click the second element.\n",
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    try:
        #Find the relative image url\n
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    

    return img_url

# ## Mars Facts
def mars_facts():
    try:
        #Use 'read_html' to scarpe the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None
    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)
    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

# ## Hemispheres Images
def hemispheres(browser):
    #Visit URL
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    #Parse with soup
    hemisphere_html = browser.html
    hemisphere_soup = soup(hemisphere_html, 'html.parser')
    #List to hold images and titles
    hemisphere_image_urls = []
    #Retrieve items for hemisphere info
    items = hemisphere_soup.find_all('div', class_='item')

    #Retreive the image urls and titles for each hempisphere
    url_main = "https://astrogeology.usgs.gov/"

    #For loop to scrape through all hemispheres
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
    return hemisphere_image_urls


if __name__ == "__main__":
    #If running as script, print scraped data
    print(scrape_all())
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import datetime as dt
import pandas as pd


#add a function to initialize browser, create data dictionary, end WebDriver and return scraped data
def scrape_all():
    #Initiate headless driver for deployment
    #set executable path for splinter browser and set url
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemisphere": hemisphere(browser)
    }

    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):
    #added browser to function to tell Python we'll use browser variable defined outside the function
    #bc all scraping code utilizes an automated browser, need this to make function work

    #assign url and instruct browser to visit it
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)
    #this specifies combo of div tag and list_text attribute (i.e. ul.item_list would tell html = <ul class="item_list">)
    #also adds 1 second wait before starting search (to allow dynamic pages to load, especially if image heavy)

    #set up html parser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    #Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None

    return news_title, news_p


# ### Featured Images
def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()
    #indexing 1 tells browser to click the second button (there are 3)

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    #Add try/except for error handling
    try:

        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        #img tag is nested in the html, so it's included in search
        # get src pulls the link to the image
        #What we've done here is tell BeautifulSoup to look inside the <img /> tag 
        # for an image with a class of fancybox-image. Basically we're saying, "This is where the 
        # image we want lives—use the link that's inside these tags."
    except AttributeError:
        return None
    
    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    #because the above is only a partial link- this will build a full, usable link

    return img_url


### Mars Facts Table

def mars_facts():
    try:
        #use read_html to scrape the facts table into a data frame
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    #Assign columns and set index of df
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
    
#this will scrape the table with the Pandas read html function
#df = pd.read_htmldf = pd.read_html('https://galaxyfacts-mars.com')[0] With this line, 
# we're creating a new DataFrame from the HTML table. The Pandas function read_html() 
# specifically searches for and returns a list of tables found in the HTML. By 
# specifying an index of 0, we're telling Pandas to pull only the first table it 
# encounters, or the first item in the list. Then, it turns the table into a DataFrame.
# df.columns=['description', 'Mars', 'Earth'] Here, we assign columns to the new DataFrame for additional clarity.
#df.set_index('description', inplace=True) By using the .set_index() function, we're 
# turning the Description column into the DataFrame's index. inplace=True means that the updated 
# index will remain in place, without having to reassign the DataFrame to a new variable.
    #Convert df into html format, add boostrap
    return df.to_html()
    #Pandas converts a dataframe back into html ready code

def hemisphere(browser):
    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'

    browser.visit(url)
    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    for image in range(4,11,2):
        hemispheres = {}
        full_image_elem = browser.find_by_tag('a')[image]
        full_image_elem.click()
        mars_html = browser.html
        mars_img_soup = soup(mars_html, 'html.parser')
        img_url_rel = mars_img_soup.find_all('a', target='_blank')[2].get('href')
        img_url = f'{url}{img_url_rel}'
        title = mars_img_soup.find('h2')
        hemispheres['img_url'] = img_url
        hemispheres['title'] = title.text
        hemisphere_image_urls.append(hemispheres)
        browser.back()
    # 4. Print the list that holds the dictionary of each image url and title.
    return hemisphere_image_urls


if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())


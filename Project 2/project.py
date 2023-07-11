"""
422 Individual Project 2
Shaolong (Fred) Xue
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from pymongo import MongoClient
import time
import re
import requests
import json
import http.client, urllib.parse
import ast

## global paths and valules
bayc_url = "https://opensea.io/collection/boredapeyachtclub?search[sortAscending]=false&search[stringTraits][0][name]=Fur&search[stringTraits][0][values][0]=Solid%20Gold"

driver_path = "/Users/shaolongxue/Documents/_Misc./chromedriver"

user_agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}

yp_url = "https://www.yellowpages.com/search?search_terms=pizzeria&geo_location_terms=San+Francisco%2C+CA"

client = MongoClient("localhost", 27017)

#######################################################################
#### Selenium: The Bored Ape Yacht Club (Question 1 and Question 2)####
#######################################################################

### Question 1 - Get the URL

def Question1():
    print(bayc_url)

### Question 2 - Save Top 8 Most expensive Bored Apes
def Question2(bayc_url, driver_path):

    driver = webdriver.Chrome(executable_path=driver_path)
    classname = "sc-1f719d57-0.fKAlPV.Asset--anchor"

    driver.get(bayc_url)
    time.sleep(3)

    # loop through the first 8 items
    for i in range(8):
        # look for nft item pages, limit to the first 8
        # this line also refreshes the search so the click() function works in the next iteration
        items = driver.find_elements(By.CLASS_NAME, classname)[:8]
        
        # click on the item
        items[i].click()
        time.sleep(5)
        
        # save the html to htm file
        # tried to clean up the file a bit
        with open(f"bayc_{i+1}.htm", 'w', encoding = 'utf-8') as f:
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            for tag in soup(['script', 'style']):
                tag.decompose()
            clean_htm = soup.prettify()
            f.write(clean_htm)
        
        # go back to the original page with the list of items
        driver.back()
        time.sleep(5)

#######################################################################
#### MongoDB (Question 3) #############################################
#######################################################################

### Question 3 - Insert to MongoDB collection
def Question3():
    
    db = client["bayc"]
    collection = db["TopEight"]

    # loop through 8 files
    for i in range(1,9):
        filename = f"bayc_{i}.htm"

        with open(filename, 'r', encoding = 'utf-8') as f:
            html = f.read()

        soup = BeautifulSoup(html, 'html.parser')

        # extract item number from the title
        title = soup.title.text.strip()
        item_num = re.match(r'^(\d+)', title).group(1)

        # extract item attribute information
        attributes = {}
        # iterate two soup select statements together
        for property_type, property_value in zip(soup.select('.Property--type'), soup.select('.Property--value')):
            att_name = property_type.text.strip()
            att_val = property_value.text.strip()
            attributes[att_name] = att_val

        # insert into MongoDB collection
        collection.insert_one({'Item_Name/Number': item_num, 'Attributes': attributes})

#######################################################################
#### Regular Webscraping (Question 4 and Question 5) ##################
#######################################################################

### Question 4

def Question4():
    response = requests.get(yp_url, headers = user_agent)
    soup = BeautifulSoup(response.text, 'html.parser')

    with open("sf_pizzeria_search_page.htm", 'w', encoding = 'utf-8') as f:
        f.write(str(soup.prettify()))

### Question 5

def Question5():

    # read the file
    with open("sf_pizzeria_search_page.htm", 'r', encoding = 'utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    # pinpoint 30 pizzeria listings under the div class named 'search-results organic'
    main_content = soup.find('div', class_ = 'search-results organic').find_all('div', class_ = 'result')

    # iterate through rank and each listing to extract info
    for rank, pizzeria in enumerate(main_content, start = 1):
        ## get name and link
        name = pizzeria.find('a', class_ = 'business-name').get_text().strip()
        sublink = pizzeria.find('a', class_ = 'business-name').get('href')
        link = "https://yellowpages.com" + sublink

        # trying for cases when a pizzeria doesn't have certain pieces of info
        ## get YP Star rating
        try:
            # the rating is the second part of the class attribute value
            rating = pizzeria.find('div', class_ = 'result-rating').get('class')
            yp_rating = rating[1]
            # for cases when the rating class has another word, "half"
            if "half" in rating:
                yp_rating += " " + rating[2]
            
            mappings = {"one": 1, "one half": 1.5, "two": 2, "two half": 2.5, "three": 3, "three half": 3.5, "four": 4, "four half": 4.5, "five": 5}
            yp_rating = mappings.get(yp_rating.lower())
        except Exception as e:
            yp_rating = None

        ## get YP review count
        try:
            # find the next span element after the result-rating div
            # strip the parenthesis around the number
            yp_review_count = pizzeria.find('div', class_ = 'result-rating').find_next('span', class_='count').get_text().strip()[1:-1]
        except Exception as e:
            yp_review_count = None

        ## get TA rating and TA review count
        try:
            # extract from the json dictionary that contains the trip advisor info
            ta_info = pizzeria.find('div', class_ = 'ratings').get("data-tripadvisor")
            ta_info = json.loads(ta_info)
            ta_rating = ta_info.get("rating")
            ta_review_count =ta_info.get("count")
        except Exception as e:
            ta_rating = None
            ta_review_count = None
        
        ## get the price range
        try:
            # logc is the same as extracting yp_review_count
            price_range = pizzeria.find('div', class_ = 'price-range').get_text().strip()
            # returns None for pizzerias with 'price-range' div but no value in it 
            if price_range:
                price_range
            else:
                price_range = None
        except Exception as e:
            price_range = None
        
        ## get the year in business (YIB)
        try:
            YIB = pizzeria.find('div', class_ = 'number').get_text().strip()
        except Exception as e:
            YIB = None

        ## get the review 
        try:
            review = pizzeria.find('p', class_ = 'body with-avatar').text.strip()
        except Exception as e:
            review = None
        
        ## get the amenities info
        try:
            amenities = []
            amenities_list = pizzeria.find('div', class_ = 'amenities-info').find_all('span')
            # lop through each amenitity for a pizzeria
            for topic in amenities_list:
                amenities.append(topic.text.strip())
        except Exception as e:
            amenities = None

        # print the results to screen
        print("------")
        print(f"Rank: {rank}")
        print(f"Name: {name}")
        print(f"Link: {link}")
        print(f"YP Star Rating: {yp_rating}")
        print(f"YP Review Count: {yp_review_count}")
        print(f"TA Rating: {ta_rating}")
        print(f"TA Review Count: {ta_review_count}")
        print(f"Price Range: {price_range}")
        print(f"Year in Business: {YIB}")
        print(f"Review: {review}")
        print(f"Amenities: {amenities}")

#######################################################################
#### MongoDB (Question 6) #############################################
#######################################################################

def Question6():
    client = MongoClient("localhost", 27017)
    db = client["pizzerias"]
    collection = db["sf_pizzerias"]

    """
    line 219-306 copied code from Question 5 below
    line 308 starts the modified code
    """

    # read the file
    with open("sf_pizzeria_search_page.htm", 'r', encoding = 'utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    # pinpoint 30 pizzeria listings under the div class named 'search-results organic'
    main_content = soup.find('div', class_ = 'search-results organic').find_all('div', class_ = 'result')

    # iterate through rank and each listing to extract info
    for rank, pizzeria in enumerate(main_content, start = 1):
        ## get name and link
        name = pizzeria.find('a', class_ = 'business-name').get_text().strip()
        sublink = pizzeria.find('a', class_ = 'business-name').get('href')
        link = "https://yellowpages.com" + sublink

        # trying for cases when a pizzeria doesn't have certain pieces of info
        ## get YP Star rating
        try:
            # the rating is the second part of the class attribute value
            rating = pizzeria.find('div', class_ = 'result-rating').get('class')
            yp_rating = rating[1]
            # for cases when the rating class has another word, "half"
            if "half" in rating:
                yp_rating += " " + rating[2]
            
            mappings = {"one": 1, "one half": 1.5, "two": 2, "two half": 2.5, "three": 3, "three half": 3.5, "four": 4, "four half": 4.5, "five": 5}
            yp_rating = mappings.get(yp_rating.lower())

        except Exception as e:
            yp_rating = None

        ## get YP review count
        try:
            # find the next span element after the result-rating div
            # strip the parenthesis around the number
            yp_review_count = pizzeria.find('div', class_ = 'result-rating').find_next('span', class_='count').get_text().strip()[1:-1]
        
        except Exception as e:
            yp_review_count = None

        ## get TA rating and TA review count
        try:
            # extract from the json dictionary that contains the trip advisor info
            ta_info = pizzeria.find('div', class_ = 'ratings').get("data-tripadvisor")
            ta_info = json.loads(ta_info)
            ta_rating = ta_info.get("rating")
            ta_review_count =ta_info.get("count")

        except Exception as e:
            ta_rating = None
            ta_review_count = None
        
        ## get the price range
        try:
            # logc is the same as extracting yp_review_count
            price_range = pizzeria.find('div', class_ = 'price-range').get_text().strip()
            # returns None for pizzerias with 'price-range' div but no value in it 
            if price_range:
                price_range
            else:
                price_range = None

        except Exception as e:
            price_range = None
        
        ## get the year in business (YIB)
        try:
            YIB = pizzeria.find('div', class_ = 'number').get_text().strip()
        
        except Exception as e:
            YIB = None

        ## get the review 
        try:
            review = pizzeria.find('p', class_ = 'body with-avatar').text.strip()

        except Exception as e:
            review = None
        
        ## get the amenities info
        try:
            amenities = []
            amenities_list = pizzeria.find('div', class_ = 'amenities-info').find_all('span')
            # lop through each amenitity for a pizzeria
            for topic in amenities_list:
                amenities.append(topic.text.strip())
            
        except Exception as e:
            amenities = None

        """
        new modification to insert into MongdoDB
        """

        document = {
            'Rank': rank,
            'Name': name,
            'Link': link,
            'YP Star Rating': yp_rating,
            'YP Review Count': yp_review_count,
            'TA Rating': ta_rating,
            'TA Review Count': ta_review_count,
            'Price Range': price_range,
            'Year in Business': YIB,
            'Review': review,
            'Amenities': amenities
        }
        
        collection.insert_one(document)

#######################################################################
#### Parsing (Question 7 and Question 8) ##############################
#######################################################################

### Question 7

def Question7():

    db = client["pizzerias"]
    collection = db["sf_pizzerias"]

    # locate the iterate through each pizzeria
    for pizzeria in collection.find():
        link = pizzeria['Link']
        rank = pizzeria['Rank']
        filename = f"sf_pizzerias_{rank}.htm"
        
        # set a long pause to bypass the time-out issue
        time.sleep(15)
        response = requests.get(link, headers = user_agent)
        time.sleep(15)

        with open(filename, 'w', encoding = 'utf-8') as f:
            f.write(response.text)

### Question 8

def Question8():

    for rank in range(1,31):
        
        filename = f"sf_pizzerias_{rank}.htm"
        
        # read each pizzeria html page
        with open(filename, 'r', encoding = 'utf-8') as f:
            html = f.read()

        soup = BeautifulSoup(html, 'html.parser')

        # find the p element with phone as class attribute, extract just the number
        try: 
            phone = soup.find('p', class_ = 'phone').get_text().replace('Phone:  ', '')
        except Exception as e:
            phone = None
            
        # find the p element that contains a specific span element, extract just the address info
        try:
            address = soup.find('span', text = 'Address: ').parent.text.replace('Address: ', '')
        except Exception as e:
            address = None

        # find the a element that comes after the p element with class named website, extract website text
        try:
            website = soup.find('p', class_ = 'website').find('a').text
        except Exception as e:
            website = None
        
        # print the results
        print("------")
        print(f"Phone: {phone}")
        print(f"Address: {address}")
        print(f"Website: {website}")

#######################################################################
##### API (Question 9) ################################################
#######################################################################

### Question 9

def Question9():

    conn = http.client.HTTPConnection('api.positionstack.com')

    phone_list = []
    address_list = []
    website_list = []

    # fill in the empty lists above with info
    for rank in range(1,31):
            
        filename = f"sf_pizzerias_{rank}.htm"
        
        # read each pizzeria html page
        with open(filename, 'r', encoding = 'utf-8') as f:
            html = f.read()

        soup = BeautifulSoup(html, 'html.parser')

        # find the p element with phone as class attribute, extract just the number
        try: 
            phone = soup.find('p', class_ = 'phone').get_text().replace('Phone:  ', '')
        except Exception as e:
            phone = None
            
        # find the p element that contains a specific span element, extract just the address info
        try:
            address = soup.find('span', text = 'Address: ').parent.text.replace('Address: ', '')
        except Exception as e:
            address = None

        # find the a element that comes after the p element with class named website, extract website text
        try:
            website = soup.find('p', class_ = 'website').find('a').text
        except Exception as e:
            website = None
        
        phone_list.append(phone)
        address_list.append(address)
        website_list.append(website)

    geoloc_list = []

    # fill in the geolocation list with info
    for address in address_list[0:30]:
        # positionstack.com API query
        params = urllib.parse.urlencode({
            'access_key': '992f286a8e78f3ec28636d430f579bc8',
            'query': address
        })

        # send GET request 
        conn.request('GET', '/v1/forward?{}'.format(params))
        time.sleep(10)

        # load the data into a json object
        response = conn.getresponse().read()
        data = json.loads(response)

        long = data['data'][0]['longitude']
        lat = data['data'][0]['latitude']
        geoloc = {"Latitude": lat, "Longitude": long}

        geoloc_list.append(geoloc)

    # save the geolocation list locally to avoid requestings multiple times
    with open('geoloc_list.txt', 'w') as f:
        json.dump(geoloc_list, f)
    
    # read the local geolocation list
    with open('geoloc_list.txt', 'r') as f:
        geoloc_list_read = f.read()

    # convert to a proper list
    geoloc_list = list(ast.literal_eval(geoloc_list_read))

    db = client['pizzerias']
    collection = db['sf_pizzerias']

    for pizzeria in collection.find():
        # uniquely identify the document
        id = pizzeria['_id']
        rank = pizzeria['Rank']

        # set up the new fields
        new_fields = {
            "Phone_Number": phone_list[rank-1],
            "Address": address_list[rank-1],
            "Website": website_list[rank-1],
            "Geolocation": geoloc_list[rank-1]
        }
        
        # update the documents
        collection.update_one({"_id": id}, {"$set": new_fields})

##### Function Calls
Question2(bayc_url, driver_path)
Question3()
Question4()
Question5()
Question6()
Question7()
Question8()
Question9()
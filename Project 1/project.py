"""
452 - Individual Project 1 - Coding Part
Shaolong (Fred) Xue
""" 

from bs4 import BeautifulSoup
import requests
import time
import re

user_agent = {'User-agent': 'Mozilla/5.0'}

"""
~~~~~~~~~~Note for Jörn or Rishabh~~~~~~~~~~~

I defined answers to each question in a function. The call for each function is currently commented out. 
Hopefully this is easier to run/check the whole file. 
"""

######## Part 1.1 ##########

#### Question (a) - Saving a file
def question_1a(url):
    page = requests.get(url, headers = user_agent)
    soup = BeautifulSoup(page.content, 'html.parser')

    # save the soup
    file = open("amazon_gift_card_01.htm", "w")
    file.write(str(soup.prettify()))
    file.close()

url = "https://www.ebay.com/sch/i.html?_from=R40&_nkw=amazon+gift+card&_sacat=0&rt=nc&LH_Sold=1&_fsrp=1&_pgn=1"

### Function Call
#question_1a(url)

#### Question (b) - Downloading 10 files w/ loop
def question_1b():
    for page_num in range(1, 11):
        
        # pause in between saves
        time.sleep(10)

        # load the page
        url = f"https://www.ebay.com/sch/i.html?_from=R40&_nkw=amazon+gift+card&_sacat=0&rt=nc&LH_Sold=1&_fsrp=1&_pgn={page_num}"
        page = requests.get(url, headers = user_agent)

        # parse the page with BeautifulSoup
        soup = BeautifulSoup(page.text, "html.parser")

        # save the page to a file
        with open(f"amazon_gift_card_{page_num:02}.htm", "w") as file:
            file.write(str(soup))

### Function Call
#question_1b()

#### Question (c) - Parsing through files w/ loop
def question_1c():
    # loop through each file
    for file_number in range(1, 11):
        file_path = f'amazon_gift_card_{file_number:02d}.htm'

        with open(file_path, 'r') as f:
            soup = BeautifulSoup(f, 'html.parser')
            #print(soup.prettify())

### Function Call
#question_1c()

#### Question (d) - Extracting all info
def extract_face_value(title):
    match = re.search(r'\d+', title)
    if match:
        return float(match.group(0))
    else:
        return None

def question_1d():
    # loop through each file
    for file_number in range(1, 11):
        file_path = f'amazon_gift_card_{file_number:02d}.htm'

        with open(file_path, 'r') as f:
            soup = BeautifulSoup(f, 'html.parser')
            items = soup.find_all('div', class_='s-item__info clearfix') ## find item info

        # loop through each item
        for item in items[1:]:

            # extracting title info
            title_element = item.find("span", {"role": "heading"})

            if title_element:
                title = title_element.text
            else:
                title = "Title not found"

            # extracting face value info
            face_value = extract_face_value(title)

            # extracting price info
            price_element = item.find("span", {"class": "s-item__price"}).text
            price = float(re.search(r"\$(\d+(?:\.\d+)?)", price_element)[1])

            # extracting shipping info
            shipping_element = item.find("span", {"class": "s-item__shipping"})

            ## assign 0 to missing shipping info
            if shipping_element is None:
                shipping = 0

            ## assign 0 for free shipping 
            elif "Free shipping" in shipping_element.get_text():
                shipping = 0

            ## extract actual shipping fee
            else:
                shipping = float(re.search(r"\$(\d+(?:\.\d+)?)", shipping_element.get_text())[1])

            cost = price + shipping

            # print item details
            print(f"Title: {title}")
            print(f"Price: ${price:.2f}")
            print(f"Shipping: ${shipping:.2f}")
            print(f"Cost: ${cost:.2f}")
            if face_value is None:
                print("Face Value: Missing")
            else:
                print(f"Face Value: ${face_value:.2f}")
            print()

### Function Call
#question_1d()

#### Question (e) - Comparing using regex
def question_1e():
    n = 0
    # loop through each file
    for file_number in range(1, 11):
        file_path = f'amazon_gift_card_{file_number:02d}.htm'

        with open(file_path, 'r') as f:
            soup = BeautifulSoup(f, 'html.parser')

            items = soup.find_all('div', class_='s-item__info clearfix')

        # loop through each item
        for item in items[1:]:

            # extracting title info
            title_element = item.find("span", {"role": "heading"})

            if title_element:
                title = title_element.text
            else:
                title = "Title not found"

            # extracting face value info
            face_value = extract_face_value(title)

            # extracting price info
            price_element = item.find("span", {"class": "s-item__price"}).text
            price = float(re.search(r"\$(\d+(?:\.\d+)?)", price_element)[1])

            # extracting shipping info
            shipping_element = item.find("span", {"class": "s-item__shipping"})

            ## assign 0 to missing shipping info
            if shipping_element is None:
                shipping = 0

            ## assign 0 to free shipping 
            elif "Free shipping" in shipping_element.get_text():
                shipping = 0

            ## extract actual shipping fee
            else:
                shipping = float(re.search(r"\$(\d+(?:\.\d+)?)", shipping_element.get_text())[1])

            cost = price + shipping
                        
            # print out only items with cost greater than face value
            if face_value is not None and cost > face_value:
            # print item details
                print(f"Title: {title}")
                print(f"Price: ${price:.2f}")
                print(f"Shipping: ${shipping:.2f}")
                print(f"Cost: ${cost:.2f}")
                print(f"Face Value: ${face_value:.2f}")
                n += 1
                fraction = "{:.4f}".format(n/(10*60))
                print("Fraction of Over Valued: " + str(fraction))
                print()

### Function Call
#question_1e()

#### Question (f) - Summarizing

"""
Question 1(f) Answer:

Out of 600 Amazon gift cards recently sold on eBay, about 41% were sold above face value! That's really surprising. 
My guess initially was that a few people might have purchased it my mistake. But it couldn't have been that prevalent. 

After some Google searching, I found out that most of these situations are due to fraud. 
People who used stolen credit cards or other accounts to buy gift cards listed by themselves, 
essentially milking money from the stolen credientials. This made more sense. 
But at almost half of the gift card transitions, this is still quite alarming. 
"""

######## Part 2 ##########

## setting up values
username = "HalaMadrid"
password = "ynadamas!"
login_url = "https://www.fctables.com/user/login/"
get_url = "https://www.fctables.com/tipster/my_bets/"

def question_2ab():
    page = requests.get(login_url)
    doc = BeautifulSoup(page.content, 'html.parser')

    ## getting the required elements for login
    input1 = doc.select('form.form input[name=login_action]')[0]
    input2 = doc.select('form.form input[name=user_remeber]')[0]
    login_action = input1.get('value')
    user_remeber = input2.get('value')

    ## storing required login values
    payload = {"login_username" : "HalaMadrid",
                "login_password" : "ynadamas!",
                "user_remeber" : user_remeber,
                "login_action": login_action}

    ## pausing in between requests
    time.sleep(5)

    ## starting a session
    session = requests.Session()

    ## sending POST request
    response = session.post(login_url, data = payload,
                            timeout = 15)

    ## storing cookies
    cookies = session.cookies.get_dict()

    ## going to My Bets page
    page2 = session.get(get_url, cookies = cookies)

    ## parsing My Bets page
    doc2 = BeautifulSoup(page2.content, 'html.parser')

    ## verifying login status
    if "Wolfsburg" in doc2.get_text():
        print("Login Successful.")
    else:
        print("Login Failed")

### Function Call
#question_2ab()
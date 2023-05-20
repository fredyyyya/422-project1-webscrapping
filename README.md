# msba-422-project1-webscrapping

### Summary

This is the first individual project I completed in the 422-Data Design & Representation course in the MSBA program at UC Davis. 

In this project, I webscrapped ebay.com and automated login process using BeautifulSoup package in Python.

#### Below are the instructions and requirements of the project

All code needs to be written in a SINGLE Python or Java file.  Please use functions to divide up the different sections in this project.  In the end, there should be a one file called “project.py” or “project.java” file.  Jupyter notebooks are not accepted.  (I want to be able to run your entire code in full at once…)
All text answers need to be written in a single .txt file called “answers.txt”.
All screen output needs to be copied into a single .txt file called “screen.txt”.
Please compress your code file, answers.txt, and screen.txt along with all downloaded HTML files into a single zip file and submit that.
 
[50%]
(1.1)  Do the following IN YOUR BROWSER, no programming required.  Please write down your answers (concise answers please).
Use your browsers development tools.  Open the network tab and analyze the network for the following:
a) go to https://www.ebay.com and search for "amazon gift card"
b) what type of search request is eBay using, GET or POST?
c) which URL variable represents the search term?
d) on the left-hand side of the page, find “Show only” and select “Sold Items” (you may have to scroll down a little bit). Which URL variable represents display sold items only?
e) can you come up with a shorter URL that produces the same search result page?
f) click on the next search result page and observe how the URL changes. What variable in the URL identifies the page number?
g) what is the feature common to each item in the search results page? I.e., what item do I need to select to obtain each item among the search results?
 
(1.2)  Let's program!
a) use the URL identified above and write code that loads eBay's search result page containing sold "amazon gift card". Save the result to file. Give the file the filename "amazon_gift_card_01.htm".
b) take your code in (a) and write a loop that will download the first 10 pages of search results. Save each of these pages to "amazon_gift_card_XX.htm" (XX = page number). IMPORTANT: each page request needs to be followed by a 10 second pause.  Please remember, you want your program to mimic your behavior as a human and help you make good purchasing decisions.
c) write code that loops through the pages you downloaded in (b), opens and parses them to a Python or Java xxxxsoup-object.
d) using your code in (c) and your answer to 1 (g), identify and print to screen the title, price, and shipping price of each item.
e) using RegEx, identify and print to screen gift cards that sold above face value. e., use RegEx to extract the value of a gift card from its title when possible (doesn’t need to work on all titles, > 90% success rate if sufficient). Next compare a gift card’s value to its price + shipping (free shipping should be treated as 0).  If value < price + shipping, then a gift card sells above face value.
f) What fraction of Amazon gift cards sells above face value? Why do you think this is the case?
 
[50%]
Let’s engage in some sport betting!
(2.1)  Do the following IN YOUR BROWSER, no programming required.  Please write down your answers (concise answers please).
a) go to fctables.comLinks to an external site. and create an account. Please choose a username + password combination that you are comfortable sharing with us.
b) log into your account.
c) search for “Bayern Munich”. (While I do not support any particular football team, I am always happy to see this team lose.)  Bayern Munich is playing Wolfsburg on February 5.  Let’s select that game.
d) let’s place a virtual bet against Bayern. To do this, click on “1” inside of “1X2” and then “Place bet”.  (This mean that you think the home team, Wolfsburg, will win.  Unfortunately, the odds are not in their favor.)
e) now go to https://www.fctables.com/tipster/my_bets/Links to an external site. and confirm that your virtual bet on the match “Wolfsburg vs Bayern Munich” appears there.
 
(2.2)  Let’s program!
a) Following the steps we discussed in class and write code that automatically logs into the website fctables.comLinks to an external site..
b) Verify that you have successfully logged in:  use the cookies you received during log in and write code to access https://www.fctables.com/tipster/my_bets/Links to an external site..  Check whether the word “Wolfsburg” appears on the page.  Don’t look for your username to confirm that you are logged in (it won’t work) and use this page’s content instead.
![image](https://github.com/fredyyyya/msba-422-project1-webscrapping/assets/123432022/89b9fcd9-f3a8-4d56-8d84-9b60bc2c1007)

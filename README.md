The objective of this project was to create a Python script to analyze the overall credibility of a given product by scraping the reviews. 
Then, get the URL of each reviewer and determine whether or not they are biased and give an adjusted rating. To do this, the selenium 
framework was used which provided several helpful functions, such as the find_element() function. When used in conjunction with the “By” 
import (from the selenium webdriver common library), it enabled the search for specific HTML elements on the webpage given different identifiers, 
such as By.CSS_SELECTER, By.XPATH, or By.CLASS_NAME, for example. Using these in our first search_amazon() function, the “reviews” section was 
loaded from the product. Once there, a for loop was used to iteratively scrape each review from the page and obtain necessary information, such as 
client name, rating, and URL to their profile, which was then appended to a list. This was inside of a while loop that was used to navigate through 
each page until the “next page” button was not present on the screen. After all information about the reviewers was obtained, it was written to an 
output text file. Then, the second function, eliminate_bias(), was called. This function opens the output file and loads the URL to each user profile.
Once there, the program checks the users “heart value”, which is the total number of likes that the user's reviews have generated. To determine if 
a user is biased, we selected an arbitrary number “40” and set that to be the benchmark for whether someone has been an active amazon reviewer. 
Those with heart values less than 40 have not created enough quality reviews, so they are rejected. Otherwise, they are added to a hashMap. 
Once biased users are eliminated, we compute the average using only the ratings of the unbiased users.

In all 3 tests, the new, adjusted score without bias was lower than the original score. This indicates that biased reviewers are in fact inflating 
scores rather than lowering them. Interested customers should take this into consideration before purchasing products.

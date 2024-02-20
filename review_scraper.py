from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait #added
from selenium.webdriver.support import expected_conditions as EC #added
import sys
import time

def search_amazon(item):
    #HashMap containing reviewers and their ratings; biased reviewers will be removed
    reviewer_info = []

    #load chrome webdriver and go to desired product's amazon webpage
    driver = webdriver.Chrome()
    driver.get(item)

    old_value = float(driver.find_element(By.CSS_SELECTOR, 'span[data-hook="rating-out-of-text"]').text.split()[0])    

    #load the reviews of said item
    try:
        reviews = driver.find_element(By.XPATH, "//a[contains(@data-hook, 'see-all-reviews-link-foot')]")
        reviews.click()

    except NoSuchElementException:
        print("Element not found. Exiting the script.")
        sys.exit()
    
    driver.implicitly_wait(3)

    #for each page of reviews, obtain the urls of each reviewer
    page = 1
    while True:
        #get the parent element containing all of the reviews on the page
        review_container = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'cm_cr-review_list')))

        #get a list of all child elements within the parent element
        reviews = review_container.find_elements(By.XPATH, './/div[@data-hook="review"]')

        #iterate through each review
        for review in reviews:
            try:
                driver.implicitly_wait(3)

                #extract url of reviewer
                url = review.find_element(By.XPATH, './/div[@data-hook="genome-widget"]/a').get_attribute('href')

                #extract name of reviewer
                name = review.find_element(By.CSS_SELECTOR, 'span.a-profile-name').text

                #extract review rating
                rating_element = review.find_element(By.CSS_SELECTOR, 'span.a-icon-alt')
                rating_innerHTML = rating_element.get_attribute('innerHTML')
                rating = int(float(rating_innerHTML.split()[0]))

                #write information to reviewer_info list
                reviewer_info.append([name,rating,url])

            except (Exception) as e:
                print("Error with reading user")
                continue

        #if there is a button for next page, navigate there, otherwise break
        try:
            print("PAGE " + str(page) + " DONE")
            page += 1

            next_page = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'li.a-last a')))
            next_page.click()
            time.sleep(1)
        except Exception as e:
            break

    #write information to output file
    with open("output.txt", 'w') as output_file:
        for info in reviewer_info:
            output_file.write(info[0] + ", " + str(info[1]) + ", " + info[2] + "\n")

    return old_value

def eliminate_bias(old_rating):
    unbiased_list = {}
    biased_user_count = 0

    #load chrome webdriver and go to desired product's amazon webpage
    driver = webdriver.Chrome()
    driver.get("https://www.amazon.com/")
    driver.implicitly_wait(3)

    #open input_file containing reviewer urls
    with open("output.txt", 'r') as input_file:
        for line in input_file:
            name, rating, url = line.strip().split(', ')

            #go to reviewer's page
            driver.get(url)
            time.sleep(1)
            
            try:
                #obtain heart_value
                heart_value = driver.find_element(By.CLASS_NAME, "impact-text").text

                #those with a heart value greater than 40 are trusted amazon reviewers 
                if int(heart_value.replace(',', "")) > 40:
                    unbiased_list[name] = rating #therefore we add them to the unbiased_list
                else:
                    biased_user_count += 1 #increment biased user count

            except NoSuchElementException:
                print("Error with processing user: " + name)

    #calculate the new rating based on the average of unbaised reviewer ratings
    new_rating = 0
    for rating in unbiased_list.values():
        new_rating += int(rating)

    new_rating = new_rating / len(unbiased_list)
    new_rating = round(new_rating, 1)

    #print the new rating compared to the old rating
    print("Original rating: " + str(old_rating) + " out of 5")
    print("Adjusted rating (no bias): " + str(new_rating) + " out of 5")
    print("Total number of biased reviewers: " + str(biased_user_count))

#different urls for different amazon products, uncomment the one to test
#item_url = "https://www.amazon.com/MARVELS-SPIDER-MAN-2-Launch-PlayStation-5/dp/B0C7WNMCSC/ref=cm_cr_arp_d_product_top?ie=UTF8"
#item_url = "https://www.amazon.com/Franklin-Sports-Official-Size-Football/dp/B0000ASZXN/ref=sr_1_4?keywords=football&qid=1699997937&sr=8-4"
item_url = "https://www.amazon.com/2022-Apple-MacBook-Laptop-chip/dp/B0B3C76P69/ref=sr_1_6?crid=279ZVD26K01KV&keywords=macbook%2Bpro&qid=1699998452&sprefix=macbook%2Bpro%2Caps%2C97&sr=8-6&th=1"

old_rating = search_amazon(item_url)
eliminate_bias(old_rating)
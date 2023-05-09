#!/usr/bin/env python
# coding: utf-8

# In[11]:


##Libraries to be imported
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup 
import pymongo
import requests
import time
import json
import re
from datetime import date
import random


# In[3]:


##Question A

##Using Selenium to access vivino, [click] Wines, [Deselect] White.

##I assume that rose is a type of red wine and further red wine can be sparkling.

##Launching the browser
driver = webdriver.Chrome(executable_path = '/Users/anirudhmenon/Desktop/UC Davis MSBA 2023/Winter Semester/Data Design and Representation/HW4/chromedriver')
driver.get("https://www.vivino.com/US-CA/en");
# driver.implicitly_wait(1)
##Selecting and Clicking the "wines" 
driver.implicitly_wait(10)
driver.set_script_timeout(120)
driver.set_page_load_timeout(10)
driver.get("https://www.vivino.com/");         

##Selecting 'Wines'
wine = "span[title='Wines']"  
wines = driver.find_element("css selector", wine);
wines.click()
time.sleep(2)

## Deselecting 'White'
wht = "//span[text()='White']"
white = driver.find_element("xpath", wht);
white.click()
time.sleep(2)

##Selecting Any Rating
any_rating=driver.find_element(By.XPATH,'//*[@id="1"]')
any_rating.click()


time.sleep(7)

driver.quit()



# In[25]:


##Question C

driver = webdriver.Chrome()
for i in [1,11,128]:
    url="https://www.vivino.com/US-CA/en/w/"+str(i)
    driver.get(url)
    time.sleep(2)
    new_url=driver.current_url
    response=requests.get(new_url,headers ={"user-agent": "Mozilla/5.0"})
    content=response.content
    soup=BeautifulSoup(content,'html.parser')
    new_id=new_url.split('/')[-1]
    print(f"Input ID - {i}")
    url_result_error=soup.find('h1', { "class" : "error-page-header" })
    if url_result_error:
        print("404 error")
    else:
        print("no 404 error")
            
    
    if i == int(new_id):
        print("Not forwarded\n")
    else:
        print(f"forwarded to {new_id}\n")
        
time.sleep(7)

driver.quit()


# In[5]:


##Question D

##Wine 1695288
url_1695288="https://www.vivino.com/US-CA/en/w/1695288"
driver = webdriver.Chrome()
driver.get(url_1695288)
time.sleep(5)


##Scrolling through the url
body = driver.find_element("css selector",'body')
for i in range(10):
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(5)

time.sleep(20)

##Question E
more_reviews = driver.find_element("xpath","//*[contains(text(), 'Show more reviews')]")
more_reviews.click()

time.sleep(20)

##Question F

scroll_selection = driver.find_element("class name","anchor_anchor__m8Qi-.reviewAnchor__anchor--2NKFw.communityReview__reviewContent--3xA5s")

k = 10
j = 0
while True:
    review_body = driver.find_elements("class name","communityReviewItem__reviewCard--1RupJ")
    
    for i in range(k):
        scroll_selection.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.5)
        
    updated_review_body = driver.find_elements("class name","communityReviewItem__reviewCard--1RupJ")
    
    if len(review_body) == len(updated_review_body):
        break
    
    review_body = updated_review_body
    print(f"No. of Reviews available in iteration {j+1} is {len(updated_review_body)}")
    k = k + 3
    j = j +1

print("\nTotal No. of reviews pulled : ",len(updated_review_body),"\n\n")

##Question G
new_page_source = f"<!--ID:1695288-->\n<!--URL:{driver.current_url}-->\n" + driver.page_source

page_content = new_page_source

with open("vivino_id_1695288.html", "w", encoding='utf-8') as f:
    f.write(new_page_source)


# In[9]:


##Question H

##Creating MongoDB connection
myclient=pymongo.MongoClient("mongodb://localhost:27017/")

##Declaring the database and collection
db = myclient["vivino"]
wines = db["wines"]
reviews= db["reviews"]
links=db["links"]
taste=db["taste"]

##Question I

##I was able to find all the reviews in Question F and G. The resulting file is throwing an error when read in jupyter.
##Hence using the new_page_source variable from above to find all elements
                
#with open("vivino_id_1695288.html", encoding='utf-8') as f:
#    soup = BeautifulSoup(f,"html.parser")
#     print(soup.prettify())

soup = BeautifulSoup(page_content,'html.parser')

for k in range(1):
    badges=[]
    goes_well_with=[]
    
    ##Wines
    #for winery, grapes, region, wine_style, allergens
    elements=soup.find_all(("td",{"class":"wineFacts__fact--3BAsiz-"}))
    
    wine_id="1695288"
    winery=elements[0].text.strip()
    name=soup.find("span",{"class":"vintage"}).text.strip()
    grapes=elements[1].text.strip()
    badge_list=soup.find_all("div",{"class":"mobile-column-4 tablet-column-8 desktop-column-6 highlights"})
    for i in badge_list:
        badges.append(i.text.strip().replace("\n\n\n"," ").replace("\n\n"," "))
    region=elements[2].text.strip()
    wine_style=elements[3].text.strip()
    allergens=elements[4].text.strip()
    date_of_download=str(date.today())
    avg_rating=soup.find("div",{"class":"vivinoRating_averageValue__uDdPM"}).text.strip()
    num_rating=soup.find("div",{"class":"vivinoRating_caption__xL84P"}).text.strip()
    avg_price=soup.find("div",{"class":"purchaseAvailability__row--S-DoM purchaseAvailability__prices--1WNrU"}).text.strip()
    pairings=soup.find_all("a",{"class":"anchor_anchor__m8Qi- foodPairing__imageContainer--2CtYR"})
    for i in pairings:
        goes_well_with.append(i.text.strip())
    print(wine_id)
    print(winery)
    print(name)
    print(grapes)
    print(badges)
    print(region)
    print(wine_style)
    print(allergens)
    print(date_of_download)
    print(avg_rating)
    print(num_rating)
    print(avg_price)
    print(goes_well_with,"\n\n")
    #Defining the data to be pushed to the collection
    data = {"Wine ID":wine_id,
            "Winery":winery,
            "Name":name,
            "Grapes":grapes,
            "Badges":badges,
            "Region":region,
            "Wine Style":wine_style,
            "Allergens":allergens,
            "Date of Download":date_of_download,
            "Average Rating":avg_rating,
            "Number of Rating":num_rating,
            "Average Price":avg_price,
            "Goes Well With":goes_well_with
           }
    wines.insert_one(data)
        
    
    ##Reviews
    
    review_no=1
    reviews_list=soup.find_all("div",{"class":"communityReviewItem__reviewCard--1RupJ"})
    for review in reviews_list:

        user_id=review.find("a",{"class":"anchor_anchor__m8Qi- userAlias_userAlias__ztmrT undefined communityReview__userAlias--1wUOM anchor_baseLink__O8bvu"})['href']
        user_id=re.search(r"/([^/]+)$", user_id).group(1)
        user_name_num_reviews=review.find("a",{"class":"anchor_anchor__m8Qi- userAlias_userAlias__ztmrT undefined communityReview__userAlias--1wUOM anchor_baseLink__O8bvu"}).text.strip()
        user_name=re.sub(r'\s*\([^)]*\)', '', user_name_num_reviews)
        num_user_reviews=re.search(r"\((\d+) ratings\)", user_name_num_reviews)
        num_user_reviews=num_user_reviews.group(1) if num_user_reviews else "NA"
        vintage=review.find("span",{"class":"reviewedVintageYear__vintageText--3TZOW communityReview__vintageText--vW6OI"})
        vintage= vintage.text.strip() if vintage else "NA"
        star_rating=review.find("span",{"class":"userRating_userRating__1X0Ps communityReview__userRating--1436U"}).text.strip()
        text=review.find("span",{"class":"communityReview__reviewText--2bfLj"}).text.strip().replace("\n\n\n"," ").replace("\n\n"," ")
        num_likes=review.find("div",{"class":"likeButton__likeCount--1stJS"}).text.strip()
        num_comments=review.find("div",{"class":"commentsButton__commentsCount--3CoCn"}).text.strip()

        print(f"Review Number : {review_no}")
        print(f"User ID : {user_id}")
        print(f"User Name : {user_name}")
        print(f"Number of Reviews by User: {num_user_reviews}")
        print(f"Vintage : {vintage}")
        print(f"Star Rating : {star_rating}")
        print(f"Comments : {text}")
        print(f"Number of likes : {num_likes}")
        print(f"Number of Comments : {num_comments} \n")
        review_no=review_no+1
        
    data = {"Wine ID":wine_id,
            "Review Number":review_no,
            "User ID":user_id,
            "User Name":user_name,
            "Number of Reviews by User":num_user_reviews,
            "Vintage":vintage,
            "Star Rating":star_rating,
            "Comments":text,
            "Number of Likes":num_likes,
            "Number of Comments":num_comments
           }
        
    reviews.insert_one(data)

    ##Links
    
    links_final=[]
    link_list=soup.find_all("a",{"class":"anchor_anchor__m8Qi- wineCard__cardLink--3F_uB"})
    for item in link_list:
        link=item['href']
        link=re.search(r'w/([^?]+)', link)
        link=link.group(1) if link else "NA"
        links_final.append(link)
    #print(links_final)
    data = {"Original Wine ID":wine_id,
            "Links":links_final
           }
        
    links.insert_one(data)    
    
    ##Taste
    
    taste_badges=[]
    wine_id=wine_id
    
    wine_features=soup.find_all("span",{"class":"indicatorBar__progress--3aXLX"})
    
    light_bold_scale=wine_features[0]['style']
    light_bold_scale=float(re.search(r'left:\s*(\d+(?:\.\d+)?)%',light_bold_scale).group(1))
    light_bold_scale=round(light_bold_scale/100,2)
    
    smooth_tannic_scale=wine_features[1]['style']
    smooth_tannic_scale=float(re.search(r'left:\s*(\d+(?:\.\d+)?)%',smooth_tannic_scale).group(1))
    smooth_tannic_scale=round(smooth_tannic_scale/100,2)
    
    dry_sweet_scale=wine_features[2]['style']
    dry_sweet_scale=float(re.search(r'left:\s*(\d+(?:\.\d+)?)%',dry_sweet_scale).group(1))
    dry_sweet_scale=round(dry_sweet_scale/100,2)
    
    soft_acidic_scale=wine_features[3]['style']
    soft_acidic_scale=float(re.search(r'left:\s*(\d+(?:\.\d+)?)%',soft_acidic_scale).group(1))
    soft_acidic_scale=round(soft_acidic_scale/100,2)
    
    taste_badge_list=soup.find_all("div",{"class":"tasteNote__mentions--1T_d5"})
    for item in taste_badge_list:
        taste_badge=item.text.strip().replace("\n\n\n"," ").replace("\n\n"," ")
        taste_badges.append(taste_badge)
    
    print(wine_id)
    print(light_bold_scale)
    print(smooth_tannic_scale)
    print(dry_sweet_scale)
    print(soft_acidic_scale)
    print(taste_badges)
    data = {"Wine ID":wine_id,
            "Light - Bold Scale":light_bold_scale,
            "Smooth - Tannic Scale":smooth_tannic_scale,
            "Dry - Sweet Scale":dry_sweet_scale,
            "Soft - Acidic Scale":soft_acidic_scale,
            "Taste badges":taste_badges
           }
        
    taste.insert_one(data)   


# In[22]:


#Question J

##Creating MongoDB connection
myclient=pymongo.MongoClient("mongodb://localhost:27017/")
##Declaring the database and collection
db = myclient["vivino"]
wines = db["wines"]
reviews= db["reviews"]
links=db["links"]
taste=db["taste"]
for i in range(1000):
    original_wine_id = str(random.randint(1, 999999))
    url=f"https://www.vivino.com/US-CA/en/w/{original_wine_id}"
    driver = webdriver.Chrome()
    driver.get(url)
    soup=BeautifulSoup(driver.page_source,"html.parser")
    url_result_error=soup.find('h1', { "class" : "error-page-header" })
    if url_result_error:
        print(f"404 Error for Wine ID : {original_wine_id}")
        new_page_source = f"<!--ID:{wine_id}-->\n<!--URL:{driver.current_url}-->\n" + driver.page_source
        with open(f"vivino_id_{original_wine_id}.html", "w", encoding='utf-8') as f:
            f.write(new_page_source)
        data = {"Wine ID":original_wine_id,
                "Winery":"NA",
                "Name":"NA",
                "Grapes":"NA",
                "Badges":"NA",
                "Region":"NA",
                "Wine Style":"NA",
                "Allergens":"NA",
                "Date of Download":"NA",
                "Average Rating":"NA",
                "Number of Rating":"NA",
                "Average Price":"NA",
                "Goes Well With":"NA"}
        wines.insert_one(data)        
        data = {"Wine ID":original_wine_id,
                "Review Number":"NA",
                "User ID":"NA",
                "User Name":"NA",
                "Number of Reviews by User":"NA",
                "Vintage":"NA",
                "Star Rating":"NA",
                "Comments":"NA",
                "Number of Likes":"NA",
                "Number of Comments":"NA"}
        reviews.insert_one(data)
        data = {"Original Wine ID":original_wine_id,
                "Links":"NA"}
        links.insert_one(data)           
        data = {"Wine ID":original_wine_id,
                "Light - Bold Scale":"NA",
                "Smooth - Tannic Scale":"NA",
                "Dry - Sweet Scale":"NA",
                "Soft - Acidic Scale":"NA",
                "Taste badges":"NA"}
        taste.insert_one(data)        
        continue
    else:    
        forwarded_url=driver.current_url
        new_id=forwarded_url.split('/')[-1]
        if original_wine_id != new_id:
            wine_id = new_id
        else:
            wine_id = original_wine_id
        time.sleep(5)
        ##Scrolling through the url
        body = driver.find_element("css selector",'body')
        for i in range(11):
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(5)
        time.sleep(15)
        more_reviews = driver.find_element("xpath","//*[contains(text(), 'Show more reviews')]")
        more_reviews.click()
        time.sleep(10)
        scroll_selection = driver.find_element("class name","anchor_anchor__m8Qi-.reviewAnchor__anchor--2NKFw.communityReview__reviewContent--3xA5s")
        k = 10
        j = 0
        while True:
            review_body = driver.find_elements("class name","communityReviewItem__reviewCard--1RupJ")
            for i in range(k):
                scroll_selection.send_keys(Keys.PAGE_DOWN)
                time.sleep(0.5)
            updated_review_body = driver.find_elements("class name","communityReviewItem__reviewCard--1RupJ")
            if len(review_body) == len(updated_review_body):
                break
            review_body = updated_review_body
            #print(f"No. of Reviews available in iteration {j+1} is {len(updated_review_body)}")
            k = k + 3
            j = j +1
        print(f"Total No. of reviews pulled for {original_wine_id} forwarded to {wine_id} : ",len(updated_review_body),"\n")
        new_page_source = f"<!--ID:{wine_id}-->\n<!--URL:{driver.current_url}-->\n" + driver.page_source
        page_content = new_page_source
        with open(f"vivino_id_{wine_id}.html", "w", encoding='utf-8') as f:
            f.write(new_page_source)
        ##I was able to find all the reviews in Question F and G. The resulting files are throwing an error when read in jupyter.
        ##Hence using the new_page_source variable from above to find all elements
        #with open(f"vivino_id_{wine_id}.html", encoding='utf-8') as f:
        #    soup = BeautifulSoup(f,"html.parser")
        soup = BeautifulSoup(page_content,'html.parser')
        badges=[]
        goes_well_with=[]
        
        ##Wines
        #for winery, grapes, region, wine_style, allergens
        elements=soup.find_all(("td",{"class":"wineFacts__fact--3BAsiz-"}))
        winery=elements[0]
        winery=winery.text.strip() if winery else "NA"
        name=soup.find("span",{"class":"vintage"})
        name=name.text.strip() if name else "NA"
        grapes=elements[1]
        grapes=grapes.text.strip() if grapes else "NA"
        badge_list=soup.find_all("div",{"class":"mobile-column-4 tablet-column-8 desktop-column-6 highlights"})
        if badge_list:
            for i in badge_list:
                i=i.text.strip().replace("\n\n\n"," ").replace("\n\n"," ") if i else "NA"
                badges.append(i)
        else:
            badges=["NA"]
        region=elements[2]
        region=region.text.strip() if region else "NA"
        wine_style=elements[3]
        wine_style=wine_style.text.strip() if wine_style else "NA"
        allergens=elements[4]
        allergens=allergens.text.strip() if allergens else "NA"
        date_of_download=str(date.today())
        avg_rating=soup.find("div",{"class":"vivinoRating_averageValue__uDdPM"})
        avg_rating=avg_rating.text.strip() if avg_rating else "NA"
        num_rating=soup.find("div",{"class":"vivinoRating_caption__xL84P"})
        num_rating=num_rating.text.strip() if num_rating else "NA"
        avg_price=soup.find("div",{"class":"purchaseAvailability__row--S-DoM purchaseAvailability__prices--1WNrU"})
        avg_user_price=soup.find("span",{"class":"purchaseAvailabilityPPC__amount--2_4GT"})
        avg_price=avg_price.text.strip() if avg_price else avg_user_price.text.strip()
        pairings=soup.find_all("a",{"class":"anchor_anchor__m8Qi- foodPairing__imageContainer--2CtYR"})
        if pairings:
            for i in pairings:
                goes_well_with.append(i.text.strip())
        else:
            goes_well_with=["NA"]

        data = {"Wine ID":wine_id,
                "Winery":winery,
                "Name":name,
                "Grapes":grapes,
                "Badges":badges,
                "Region":region,
                "Wine Style":wine_style,
                "Allergens":allergens,
                "Date of Download":date_of_download,
                "Average Rating":avg_rating,
                "Number of Rating":num_rating,
                "Average Price":avg_price,
                "Goes Well With":goes_well_with}
        wines.insert_one(data)
        
        ##Reviews
        review_no=1
        reviews_list=soup.find_all("div",{"class":"communityReviewItem__reviewCard--1RupJ"})
        if reviews_list:
            for review in reviews_list:
                user_id=review.find("a",{"class":"anchor_anchor__m8Qi- userAlias_userAlias__ztmrT undefined communityReview__userAlias--1wUOM anchor_baseLink__O8bvu"})['href']
                user_id=re.search(r"/([^/]+)$", user_id).group(1)
                user_name_num_reviews=review.find("a",{"class":"anchor_anchor__m8Qi- userAlias_userAlias__ztmrT undefined communityReview__userAlias--1wUOM anchor_baseLink__O8bvu"})
                user_name_num_reviews=user_name_num_reviews.text.strip() if user_name_num_reviews else "NA"
                user_name=re.sub(r'\s*\([^)]*\)', '', user_name_num_reviews)
                num_user_reviews=re.search(r"\((\d+) ratings\)", user_name_num_reviews)
                num_user_reviews=num_user_reviews.group(1) if num_user_reviews else "NA"
                vintage=review.find("span",{"class":"reviewedVintageYear__vintageText--3TZOW communityReview__vintageText--vW6OI"})
                vintage= vintage.text.strip() if vintage else "NA"
                star_rating=review.find("span",{"class":"userRating_userRating__1X0Ps communityReview__userRating--1436U"})
                star_rating=star_rating.text.strip() if star_rating else "NA"
                body=review.find("span",{"class":"communityReview__reviewText--2bfLj"})
                text=body.text.strip().replace("\n\n\n"," ").replace("\n\n"," ") if body else "NA"
                num_likes=review.find("div",{"class":"likeButton__likeCount--1stJS"})
                num_likes=num_likes.text.strip() if num_likes else "NA"
                num_comments=review.find("div",{"class":"commentsButton__commentsCount--3CoCn"})
                num_comments=num_comments.text.strip() if num_comments else "NA"
                review_no=review_no+1
                data = {"Wine ID":wine_id,
                        "Review Number":review_no,
                        "User ID":user_id,
                        "User Name":user_name,
                        "Number of Reviews by User":num_user_reviews,
                        "Vintage":vintage,
                        "Star Rating":star_rating,
                        "Comments":text,
                        "Number of Likes":num_likes,
                        "Number of Comments":num_comments}
                reviews.insert_one(data)
        else:
            data = {"Wine ID":wine_id,
                    "Review Number":"NA",
                    "User ID":"NA",
                    "User Name":"NA",
                    "Number of Reviews by User":"NA",
                    "Vintage":"NA",
                    "Star Rating":"NA",
                    "Comments":"NA",
                    "Number of Likes":"NA",
                    "Number of Comments":"NA"}
            reviews.insert_one(data)            
        
        ##Links
        links_final=[]
        link_list=soup.find_all("a",{"class":"anchor_anchor__m8Qi- wineCard__cardLink--3F_uB"})
        if link_list:
            for item in link_list:
                link=item['href']
                link=re.search(r'w/([^?]+)', link)
                link=link.group(1) if link else "NA"
                links_final.append(link)
            #print(links_final)
            data = {"Original Wine ID":wine_id,
                    "Links":links_final}
            links.insert_one(data)    
        else:
            data = {"Original Wine ID":wine_id,
                    "Links":"NA"}
            links.insert_one(data)            
        ##Taste
        taste_badges=[]
        wine_features=soup.find_all("span",{"class":"indicatorBar__progress--3aXLX"})
        if wine_features:
            light_bold_scale=wine_features[0]['style']
            light_bold_scale=re.search(r'left:\s*(\d+(?:\.\d+)?)%',light_bold_scale)
            light_bold_scale=float(light_bold_scale.group(1)) if light_bold_scale else "NA"
            light_bold_scale=round(light_bold_scale/100,2)
            smooth_tannic_scale=wine_features[1]['style']
            smooth_tannic_scale=re.search(r'left:\s*(\d+(?:\.\d+)?)%',smooth_tannic_scale)
            smooth_tannic_scale=float(smooth_tannic_scale.group(1)) if smooth_tannic_scale else "NA"
            smooth_tannic_scale=round(smooth_tannic_scale/100,2)
            dry_sweet_scale=wine_features[2]['style']
            dry_sweet_scale=re.search(r'left:\s*(\d+(?:\.\d+)?)%',dry_sweet_scale)
            dry_sweet_scale=float(dry_sweet_scale.group(1)) if dry_sweet_scale else "NA"
            dry_sweet_scale=round(dry_sweet_scale/100,2)
            soft_acidic_scale=wine_features[3]['style']
            soft_acidic_scale=re.search(r'left:\s*(\d+(?:\.\d+)?)%',soft_acidic_scale)
            soft_acidic_scale=float(soft_acidic_scale.group(1)) if soft_acidic_scale else "NA"
            soft_acidic_scale=round(soft_acidic_scale/100,2)
        taste_badge_list=soup.find_all("div",{"class":"tasteNote__mentions--1T_d5"})
        if taste_badge_list:
            for item in taste_badge_list:
                taste_badge=item.text.strip().replace("\n\n\n"," ").replace("\n\n"," ") if item else "NA"
                taste_badges.append(taste_badge)
        if taste_badge_list and wine_features:
            data = {"Wine ID":wine_id,
                    "Light - Bold Scale":light_bold_scale,
                    "Smooth - Tannic Scale":smooth_tannic_scale,
                    "Dry - Sweet Scale":dry_sweet_scale,
                    "Soft - Acidic Scale":soft_acidic_scale,
                    "Taste badges":taste_badges}
            taste.insert_one(data)
        else:
            if taste_badge_list:
                data = {"Wine ID":wine_id,
                        "Light - Bold Scale":"NA",
                        "Smooth - Tannic Scale":"NA",
                        "Dry - Sweet Scale":"NA",
                        "Soft - Acidic Scale":"NA",
                        "Taste badges":taste_badges}
                taste.insert_one(data)
            elif wine_features:
                data = {"Wine ID":wine_id,
                        "Light - Bold Scale":light_bold_scale,
                        "Smooth - Tannic Scale":smooth_tannic_scale,
                        "Dry - Sweet Scale":dry_sweet_scale,
                        "Soft - Acidic Scale":soft_acidic_scale,
                        "Taste badges":taste_badges}
                taste.insert_one(data)  
            else:
                data = {"Wine ID":wine_id,
                        "Light - Bold Scale":"NA",
                        "Smooth - Tannic Scale":"NA",
                        "Dry - Sweet Scale":"NA",
                        "Soft - Acidic Scale":"NA",
                        "Taste badges":"NA"}
                taste.insert_one(data)                              
        print(f"Data parsed and inserted for {original_wine_id} forwarded to {wine_id}")


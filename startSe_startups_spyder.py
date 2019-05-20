import json
import pymongo
from pymongo import MongoClient
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time



# Working

# source env/bin/activate 
# brew services start mongodb

client = MongoClient('mongodb://localhost:27017/')
db = client.startupsDB
startse = db.startse

driver = webdriver.Chrome()

driver.get('https://comunidade.startse.com/startups')
time.sleep(3)
driver.maximize_window()
time.sleep(3)

i=0

while len(driver.find_elements_by_class_name('infinite-more-link')) > 0: #pay attention: find_element*s*
  driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
  time.sleep(random.randint(3,6))

  i+=1
  if i > 0:
    break


start = time.time()
"the code you want to test stays here"

names = driver.find_elements_by_xpath("//h5[@class='fb m-0 p-lines h5-lines-2']")
links = driver.find_elements_by_css_selector('.infinite-item')
types = driver.find_elements_by_xpath("//p[@class='small text-link p-lines p-lines-1 mt-5 mb-0']")
locations = driver.find_elements_by_xpath("//p[@class='small text-muted p-lines p-lines-1 m-0']")
images = driver.find_elements_by_class_name("mb-10")

if len(names) > 0:
  for i in range(len(names)):
    print(i)
    print(names[i].text)
    print(links[i].find_element_by_tag_name('a').get_attribute('href'))
    print(types[i].text)
    print(locations[i].text)
    print(images[i].get_attribute("src"))
else:
  print('something went wrong :(')


end = time.time()
print(end - start)

driver.close()

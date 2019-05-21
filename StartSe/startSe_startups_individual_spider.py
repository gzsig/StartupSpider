import pymongo
from pymongo import MongoClient
import random
from selenium import webdriver
import time

# source env/bin/activate 
# brew services start mongodb

client = MongoClient('mongodb://localhost:27017/')
db = client.startupsDB
startse = db.startse

driver = webdriver.Chrome()

cont = 0

for startup in startse.find():
  # if cont > 3:
  #   break

  cont+=1
  link = startup['startSe link']
  name = startup['name']
  # old_website = startup['website']

  driver.get(link)
  time.sleep(random.randint(1,3))
  website = driver.find_elements_by_xpath("//a[@class='fn mr-15 text-link small']")

  if len(website) > 0:
    website = website[0].get_attribute('href')
    time.sleep(random.randint(1,2))
    startse.update_one({'name':name}, {'$set' : {'website': website}})
    print(str(cont) + '- {} website saved!'.format(name))

driver.close()
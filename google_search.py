import pymongo
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random

# DB variables
client = MongoClient('mongodb://localhost:27017/')
db = client.startupsDB
angellist = db.angellist

# # Open Chrome
driver = webdriver.Chrome()

def search(word):
  driver.get('https://www.google.com/')
  assert 'Google' in driver.title

  elem = driver.find_element_by_name('q')  # Find the search box
  elem.send_keys(word + Keys.RETURN)
  startup_card = driver.find_elements_by_xpath("//div[@class='SALvLe farUxc mJ2Mod']")


  if len(startup_card) > 0:
    for info in startup_card:
      print(info.text)
  # print(startup_card)

  # first_link = first_link.get_attribute('href')
  # website(first_link)
  time.sleep(random.randint(2,4))

def website(url):
  print(url)






cont = 0
for startup in angellist.find():
  name = startup['name']
  name = name.splitlines()
  names = []
  names.append(name[0])
  for name in names:
    if cont > 5:
      break    
    elif cont > 0:
      search(name)
      print(str(cont) + '- ' + name)
    cont+=1

# Close Chrome
driver.close()
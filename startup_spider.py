import json
import pymongo
from pymongo import MongoClient
from selenium import webdriver
import time

# brew services start mongodb

client = MongoClient('mongodb://localhost:27017/')
db = client.startupsDB
startups = db.startups

driver = webdriver.Chrome()
driver.get("https://angel.co/brazil")

time.sleep(5)

driver.find_element_by_xpath('//*[@id="root"]/div[4]/div[2]/div[2]/div/div[1]/div/div[2]').click()

time.sleep(1)

def get_startups():
  for i in range(2):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="root"]/div[4]/div[2]/div[2]/div/div[3]').click()
    time.sleep(1)
  time.sleep(3)

  results = driver.find_elements_by_class_name('startup-link')
  for element in results:
    if startups.find_one({'name' : str(element.text)}) == None and str(element.text) != '':
      name = {'name' : str(element.text)}
      startups.insert_one(name)
      print('{} saved'.format(element.text))
    elif startups.find_one({'name' : str(element.text)}) != None:
      print('{} already exists in database'.format(element.text))
    else:
      print('Empty String')

get_startups()


driver.close()


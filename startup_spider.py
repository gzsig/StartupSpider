import json
import pymongo
from pymongo import MongoClient
from selenium import webdriver
import unidecode
import time

# source env/bin/activate 
# brew services start mongodb

client = MongoClient('mongodb://localhost:27017/')
db = client.startupsDB
startups = db.startups

driver = webdriver.Chrome()

def get_data():
  driver.get("https://angel.co/companies?locations[]=1622-Brazil")
  time.sleep(8)
  driver.find_element_by_xpath('//*[@id="root"]/div[4]/div[2]/div/div[2]/div[2]/div[2]/div[1]/div/div[3]').click()
  time.sleep(2)

  for i in range(0):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="root"]/div[4]/div[2]/div/div[2]/div[2]/div[2]/div[22]').click()
    time.sleep(1)
  time.sleep(3)

  results = driver.find_elements_by_class_name('startup-link')
  for element in results:
    name = unidecode.unidecode(element.text)
    angel = element.get_attribute('href')
    if startups.find_one({'name' : str(name)}) == None and str(name) != '':
      data = {
        'name' : str(name),
        'link' : str(angel)
      }
      startups.insert_one(data)
      print('{} saved'.format(name))
      print('link: {}'.format(angel))
    elif startups.find_one({'name' : str(name)}) != None:
      print('{} already exists in database'.format(name))
    else:
      print('Empty String')


def individual_scrape():
  i=0
  for startup in startups.find():

    if i > 3:
      break

    link = startup['link']
    name = startup['name']
    driver.get(link)

    website = driver.find_element_by_class_name('company_url')
    startups.update_one({'name':name}, {'$set' : {'website': website.text}})
    print(website.text)

    locations = driver.find_element_by_class_name('js-location_tags')
    print(locations.text)

    fundings = driver.find_elements_by_class_name('raised')
    for amount in fundings:
      print(amount.text)

    employee = driver.find_element_by_class_name('js-company_size')
    print(employee.text)
    
    print(i + '\n')
    i+=1
    time.sleep(10)

# get_tada()
# individual_scrape()

driver.close()



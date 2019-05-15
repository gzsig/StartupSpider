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

def get_startups():
  driver = webdriver.Chrome()
  driver.get("https://angel.co/brazil")
  time.sleep(5)
  driver.find_element_by_xpath('//*[@id="root"]/div[4]/div[2]/div[2]/div/div[1]/div/div[2]').click()
  time.sleep(1)

  for i in range(0):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="root"]/div[4]/div[2]/div[2]/div/div[3]').click()
    time.sleep(1)
  time.sleep(3)

  results = driver.find_elements_by_class_name('startup-link')
  for element in results:
    name = unidecode.unidecode(element.text)
    angel = element.get_attribute('href')
    if startups.find_one({'name' : str(name)}) == None and str(name) != '':
      name = {
        'name' : str(name),
        'link' : str(angel)
      }
      startups.insert_one(name)
      print('{} saved'.format(name))
      print('link: {}'.format(angel))
    elif startups.find_one({'name' : str(name)}) != None:
      print('{} already exists in database'.format(name))
    else:
      print('Empty String')
  driver.close()

def individual_scrape():
  driver = webdriver.Chrome()
  driver.get("https://angel.co/company/neighborly")

  websites = driver.find_elements_by_class_name('company_url')
  for website in websites:
    print(website.text)

  about = driver.find_element_by_xpath('//*[@id="root"]/div[4]/div/div[2]/div/div[2]/div[1]/div/div[1]/div/div[3]/div/div')
  # for about in info:
  print(about.text)

  locations = driver.find_elements_by_class_name('js-location_tags')
  for location in locations:
    print(location.text)

  # investors = driver.find_elements_by_class_name('g-lockup')
  # for investor in investors:
  #   print(investor.text)

  fundings = driver.find_elements_by_class_name('raised')
  for amount in fundings:
    print(amount.text)

  employees = driver.find_elements_by_class_name('js-company_size')
  for employee in employees:
    print(employee.text)

  driver.close()


# get_startups()
individual_scrape()


# stup = startups.find()
# for i in stup:
#   print(i.name)



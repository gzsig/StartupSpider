import json
import pymongo
from pymongo import MongoClient
from selenium import webdriver
import unidecode
import time

# Not working 

# source env/bin/activate 
# brew services start mongodb

client = MongoClient('mongodb://localhost:27017/')
db = client.startupsDB
startups = db.startups

driver = webdriver.Chrome()

def get_data(xpath):
  driver.get("https://angel.co/companies?locations[]=1622-Brazil")
  time.sleep(5)
  driver.find_element_by_xpath(xpath).click()
  time.sleep(2)

  for i in range(19):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    time.sleep(1)
    driver.find_element_by_class_name('more').click()
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

    link = startup['link']
    name = startup['name']
    driver.get(link)
    
    time.sleep(5)

    website = driver.find_element_by_class_name('company_url')
    startups.update_one({'name':name}, {'$set' : {'website': website.text}})
    print('website: ' + website.text)

    markets = driver.find_element_by_class_name('js-market_tags')
    startups.update_one({'name':name}, {'$set' : {'markets': markets.text}})
    print('markets: ' + markets.text)

    locations = driver.find_element_by_class_name('js-location_tags')
    startups.update_one({'name':name}, {'$set' : {'location': locations.text}})
    print('location: ' + locations.text)

    fundings = []
    fundings = driver.find_elements_by_class_name('raised')
    if fundings == []:
      print('amount raised: -')
      startups.update_one({'name':name}, {'$set' : {'amount raised': '-'}})
    else:
      round = len(fundings)
      for amount in fundings:
        startups.update_one({'name':name}, {'$set' : {"amount raised in round {}".format(round): amount.text}})
        print('amount raised in round ' + str(round) +': ' + amount.text)
        round-=1

    employee = driver.find_element_by_class_name('js-company_size')
    if employee.text == (None or ''):
      startups.update_one({'name':name}, {'$set' : {'number of employees': '-'}})
      print('number of employees: -')
    else:
      startups.update_one({'name':name}, {'$set' : {'number of employees': employee.text}})
      print('number of employees: ' + employee.text)
    
    print(i)
    print('\n')
    i+=1
    time.sleep(15)

# get_data('//*[@id="root"]/div[4]/div[2]/div/div[2]/div[2]/div[2]/div[1]/div/div[2]')
# get_data('//*[@id="root"]/div[4]/div[2]/div/div[2]/div[2]/div[2]/div[1]/div/div[3]')
# get_data('//*[@id="root"]/div[4]/div[2]/div/div[2]/div[2]/div[2]/div[1]/div/div[9]')
individual_scrape()

driver.close()



import json
import pymongo
from pymongo import MongoClient
import dns # required for connecting with SRV
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


# Working

# source env/bin/activate 
# brew services start mongodb

client = pymongo.MongoClient("mongodb+srv://gabriel:Gz%40db3611@cluster0-ozy7g.mongodb.net/test?retryWrites=true")
db = client.startupsDB
angelList = db.angelList

driver = webdriver.Chrome()

def search(xpath):
  driver.get('https://angel.co/companies?locations[]=1622-Brazil&company_types[]=Startup')
  time.sleep(8)
  driver.find_element_by_xpath(xpath).click()
  time.sleep(2)
  driver.maximize_window()
  time.sleep(3)

  for i in range(20):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    time.sleep(3)
    if len(driver.find_elements_by_class_name('more')) > 0: #pay attention: find_element*s*
      driver.find_element_by_class_name('more').click() #pay attention: find_element
    time.sleep(2)
  time.sleep(5)


  startups = driver.find_elements_by_css_selector(".base.startup")
  for i in range(len(startups)):
    if len(startups[i].find_elements_by_css_selector('.startup-link')) > 0:
      internal_link = startups[i].find_element_by_css_selector('.startup-link').get_attribute('href')
    else:
      internal_link = '-'

    if len(startups[i].find_elements_by_tag_name('img')) > 0:
      logo = startups[i].find_element_by_tag_name('img').get_attribute('src')
    else:
      logo = '-'

    if len(startups[i].find_elements_by_css_selector(".pitch")) > 0:
      pitch = startups[i].find_element_by_css_selector(".pitch").text
    else:
      pitch = '-'

    if len(startups[i].find_elements_by_css_selector('.name')) > 0:
      name = startups[i].find_element_by_css_selector('.name').text
    else:
      name = '-'

    if len(startups[i].find_elements_by_css_selector('.joined')) > 0:
      date = startups[i].find_element_by_css_selector('.joined').text
    else:
      date = '-'

    if len(startups[i].find_elements_by_css_selector('.location')) > 0:
      location = startups[i].find_element_by_css_selector('.location').text
    else:
      location = '-'

    if len(startups[i].find_elements_by_css_selector('.market')) > 0:
      market = startups[i].find_element_by_css_selector('.market').text
    else:
      market = '-'

    if len(startups[i].find_elements_by_css_selector('.website')) > 0:
      website = startups[i].find_element_by_css_selector('.website').text
    else:
      website = '-'

    if len(startups[i].find_elements_by_css_selector('.company_size')) > 0:
      company_size = startups[i].find_element_by_css_selector('.company_size').text
    else:
      company_size = '-'

    if len(startups[i].find_elements_by_css_selector('.stage')) > 0:
      stage = startups[i].find_element_by_css_selector('.stage').text
    else:
      stage = '-'

    if len(startups[i].find_elements_by_css_selector('.raised')) > 0:
      raised = startups[i].find_element_by_css_selector('.raised').text
    else:
      raised = '-'



    if angelList.find_one({'name' : str(name)}) == None and str(name) != '':
      data = {
        'name' : str(name),
        'location' : str(location),
        'logo' : str(logo),
        'pitch' : str(pitch),
        'internal link' : str(internal_link),
        'founded' : str(date),
        'market' : str(market),
        'website' : str(website),
        'number of employees' : str(company_size),
        'stage' : str(stage),
        'amount raised' : str(raised)
      }
      angelList.insert_one(data)
      print('{} saved!'.format(name))
      print('\n')
    else:
      print('{} already!'.format(name))
    

search('//*[@id="root"]/div[4]/div[2]/div/div[2]/div[2]/div[2]/div[1]/div/div[3]')

driver.close()

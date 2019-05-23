import json
import pymongo
from pymongo import MongoClient
import dns # required for connecting with SRV
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


# source env/bin/activate 
# brew services start mongodb

client = pymongo.MongoClient("mongodb+srv://gabriel:Gz%40db3611@cluster0-ozy7g.mongodb.net/test?retryWrites=true")
db = client.startupsDB
startupBase = db.startupBase

driver = webdriver.Chrome()

start = time.time()

def search(url):
  driver.get(url)
  time.sleep(2)
  driver.maximize_window()
  time.sleep(3)
  for i in range(2):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    time.sleep(1)
  time.sleep(2)

  page = driver.find_element_by_class_name('ais-InfiniteHits')
  startups = page.find_elements_by_class_name('search-body__item')
  for startup in startups:
    if len(startup.find_elements_by_tag_name('a')) > 0:
      internal_link = startup.find_element_by_tag_name('a').get_attribute('href')
      # print(startup.find_element_by_tag_name('a').get_attribute('href'))
    
    if len(startup.find_elements_by_tag_name('img')) > 0:
      logo = startup.find_element_by_tag_name('img').get_attribute('src')
      # print(startup.find_element_by_tag_name('img').get_attribute('src'))
    
    if len(startup.find_elements_by_css_selector('.organization__title.sb-size-6')) > 0:
      name = startup.find_element_by_css_selector('.organization__title.sb-size-6').text
      # print(startup.find_element_by_css_selector('.organization__title.sb-size-6').text)
    
    if len(startup.find_elements_by_css_selector('.organization__label')) > 0:
      organization_label = startup.find_element_by_css_selector('.organization__label')
      check = organization_label.find_elements_by_tag_name('span')
      location_check = organization_label.find_elements_by_class_name('fa-map-marker-alt')
      if len(check) > 1 and len(location_check) > 0:
        location = check[0].text
        market = check[1].text
      elif len(check) > 0 and len(location_check) > 0:
        market = '-' 
        location = check[0].text
      elif len(check) > 0:
        market = check[0].text
        location = '-'
      else:
        location = '-'
        market = '-'        
      # print(startup.find_element_by_css_selector('.organization__label').text)
    
    if len(startup.find_elements_by_css_selector('.organization__description.sb-size-10')) > 0:
      info = startup.find_element_by_css_selector('.organization__description.sb-size-10').text
      # print(startup.find_element_by_css_selector('.organization__description.sb-size-10').text)
  # print('\n')
    if startupBase.find_one({'name' : str(name)}) == None and str(name) != '':
      data = {
        'name' : str(name),
        'market' : str(market),
        'location' :str(location),
        'logo' : str(logo),
        'internal link' : str(internal_link),
        'info' : str(info)
      }
      startupBase.insert_one(data)
      print('{} saved!'.format(data))
      print('\n')
    else:
      print('{} already in DB!'.format(name))
    time.sleep(1)

search('https://startupbase.com.br/startups?q=&states=all&cities=all&groups=all&targets=all&phases=all&models=all&badges=all')
end = time.time()
print(end - start)

driver.close()
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
db = client.test
test_one = db.test_one

driver = webdriver.Chrome()

def search(url):
  driver.get(url)
  time.sleep(2)
  driver.maximize_window()
  time.sleep(3)
  for n in range(1):
    startups = driver.find_elements_by_tag_name('card-startup')
    for i in range(len(startups)):
      if startups[i].find_element_by_css_selector(".mb-0") != None:
        name = startups[i].find_element_by_css_selector(".mb-0").text
      else:
        name = '-'
      if startups[i].find_element_by_css_selector(".col-4.sb-card__verified") != None:
        logo = startups[i].find_element_by_css_selector(".col-4.sb-card__verified").find_element_by_tag_name('img').get_attribute('src')
      else:
        logo = '-'
      if startups[i].find_element_by_tag_name('small') != None:
        location = startups[i].find_element_by_tag_name('small').text
      else:
        location = '-'
      if len(startups[i].find_elements_by_class_name('text-center')) > 0:
        info = startups[i].find_element_by_class_name('text-center').text
      else:
        info = '-'
      if startups[i].find_element_by_tag_name('a') != None:
        internal_link = startups[i].find_element_by_tag_name('a').get_attribute('href')
      else:
        internal_link = '-'



      if test_one.find_one({'name' : str(name)}) == None and str(name) != '':
        data = {
          'name' : str(name),
          'location' : str(location),
          'logo' : str(logo),
          'info' : str(info),
          'internal link' : str(internal_link)
        }
        print('{} saved!'.format(name))
        print('{} saved!'.format(logo))
        print('{} saved!'.format(location))
        print('{} saved!'.format(info))
        print('{} saved!'.format(internal_link))
        print('\n')
        test_one.insert_one(data)
      else:
        print('{} already!'.format(name))
      time.sleep(random.randint(1,3))

    driver.find_element_by_xpath('/html/body/app-root/app-list/div[2]/div/div/div[2]/div[1]/pagination/ul/li[8]/a').click()


search('https://startupbase.abstartups.com.br/startups?refinementList%5Bbusiness_target%5D%5B0%5D=B2B')

driver.close()

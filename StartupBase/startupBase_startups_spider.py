import json
import pymongo
from pymongo import MongoClient
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


# source env/bin/activate 
# brew services start mongodb

client = MongoClient('mongodb://localhost:27017/')
db = client.startupsDB
startupbase = db.startupbase

driver = webdriver.Chrome()

def search(url):
  driver.get(url)
  time.sleep(2)
  driver.maximize_window()
  time.sleep(3)

  # names = driver.find_elements_by_xpath("//h6[@class='mb-0']")
  # logo_links = driver.find_elements_by_css_selector(".col-4.sb-card__verified") 
  # locations = driver.find_elements_by_xpath("//p[@class='text-muted']")
  # infos = driver.find_elements_by_xpath("//small[@class='text-muted']")

  names = driver.find_elements_by_tag_name('card-startup')
  for i in range(len(names)):
    # print(logo_links[i].find_element_by_tag_name('img').get_attribute('src'))
    if names[i].find_element_by_css_selector(".mb-0") != None:
      print('name')
      print(names[i].find_element_by_css_selector(".mb-0").text)

    if names[i].find_element_by_css_selector(".col-4.sb-card__verified") != None:
      print('logo')
      print(names[i].find_element_by_css_selector(".col-4.sb-card__verified").find_element_by_tag_name('img').get_attribute('src'))

    if names[i].find_element_by_tag_name('small') != None:
      print('location')
      print(names[i].find_element_by_tag_name('small').text)

    if len(names[i].find_elements_by_class_name('text-center')) > 0:
      print('info')
      print(names[i].find_element_by_class_name('text-center').text)
    
    print('\n')
    # print(locations[i].text)
    # print(infos[i].text)


search('https://startupbase.abstartups.com.br/startups?refinementList%5Bbusiness_target%5D%5B0%5D=B2B')

driver.close()

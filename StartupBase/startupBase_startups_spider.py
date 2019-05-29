import json
import pymongo
from pymongo import MongoClient
import dns # required for connecting with SRV
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


# source env/bin/activate 

# Getting access to database
password = ""
with open("password.txt", "r") as password_file:
  password = password_file.readline()

client = pymongo.MongoClient(password)
db = client.startupsDB
# saving collections in variables
startupBase = db.startupBase

driver = webdriver.Chrome()

# starting to count time to get full duration of run time
start = time.time()



def search(letter, url):
  cont = 0
  # open driver and get specif url
  driver.get(url)
  time.sleep(2)
  driver.maximize_window()
  time.sleep(2)
  # find search box and seach for all letters and numbers
  elem = driver.find_elements_by_class_name('ais-SearchBox-input')  # Find the search box
  elem[1].send_keys(letter + Keys.RETURN)
  time.sleep(3)
  # scroll to bottom of page 10 times to load the largest number of startups possible
  for i in range(10):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    time.sleep(1)
  time.sleep(2)

  page = driver.find_element_by_class_name('ais-InfiniteHits')
  # finds all startup cards
  startups = page.find_elements_by_class_name('search-body__item')
  for startup in startups:
    cont += 1
    # gets internal startupBase link to get more info
    if len(startup.find_elements_by_tag_name('a')) > 0:
      internal_link = startup.find_element_by_tag_name('a').get_attribute('href')
    # gets logo
    if len(startup.find_elements_by_tag_name('img')) > 0:
      logo = startup.find_element_by_tag_name('img').get_attribute('src')
    # gets name of startup
    if len(startup.find_elements_by_css_selector('.organization__title.sb-size-6')) > 0:
      name = startup.find_element_by_css_selector('.organization__title.sb-size-6').text
    # check for location and market. save accordingly
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
    # get description if avaible
    if len(startup.find_elements_by_css_selector('.organization__description.sb-size-10')) > 0:
      info = startup.find_element_by_css_selector('.organization__description.sb-size-10').text
    # if startup not already in DB save
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
      print(str(cont) + '- {} saved!'.format(data))
      print('\n')
    else:
      print(str(cont) + '- {} already in DB!'.format(name))

letters = [
  'a',
  'b',
  'c',
  'd',
  'e',
  'f',
  'g',
  'h',
  'i',
  'j',
  'k',
  'l',
  'm',
  'n',
  'o',
  'p',
  'q',
  'r',
  's',
  't',
  'u',
  'v',
  'w',
  'x',
  'y',
  'z',
  '0',
  '1',
  '2',
  '3',
  '4',
  '5',
  '6',
  '7',
  '8',
  '9'
]
# calls function with all letters
for letter in letters:
  search(letter, 'https://startupbase.com.br/startups')
  time.sleep(random.randint(1,2))
  
end = time.time()
print(end - start)

driver.close()
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

password = ""
with open("password.txt", "r") as password_file:
  password = password_file.readline()

client = pymongo.MongoClient(password)
db = client.startupsDB
dealBook = db.dealBook

driver = webdriver.Chrome()

start = time.time()

driver.get('https://dealbook.co/companies')
time.sleep(1)
driver.maximize_window()
time.sleep(2)

for i in range(111):

  table = driver.find_element_by_tag_name('tbody')
  rows = table.find_elements_by_tag_name('tr')

  for startup in rows:
    name = startup.find_element_by_tag_name('a').text
    internal_link = startup.find_element_by_tag_name('a').get_attribute('href')

    if dealBook.find_one({'name' : str(name)}) == None and str(name) != '':
      data = {
        'name' : str(name),
        'internal link' : str(internal_link)
      }
      dealBook.insert_one(data)
      print('{} saved!'.format(name))
    else:
      print('{} Already in DB!'.format(name))
  time.sleep(1)
  next_page = driver.find_element_by_class_name('next_page')
  next_page.find_element_by_tag_name('a').click()

end = time.time()
print(end - start)

driver.close()
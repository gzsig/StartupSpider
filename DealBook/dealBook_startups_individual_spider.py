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

cont = 0

for startup in dealBook.find():
  if cont > 3:
    break
  cont += 1
  link = startup['internal link']
  name = startup['name']
  driver.get(link)
  
  table = driver.find_element_by_tag_name('tbody')
  rows = table.find_elements_by_tag_name('tr')

  for row in rows:
    

  

end = time.time()
print(end - start)
driver.close()
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

# starting to count time to get full duration of run time
start = time.time()

cont = 0
for startup in startupBase.find({'info' : ''}):
  name = startup['name']
  while cont < 1:
    cont += 1
    print(startup)
    # startup.update({}, {'$unset' : {'info': 1 }})
    startupBase.update_one({'name' : name}, {'$unset' : {'info': 1}})
    print(cont)
    print(startup)



# gets the end time and print the duration
end = time.time()
dutration = ((end - start) / 60)
print('duration was {} min'.format(dutration))
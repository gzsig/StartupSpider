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
angelList = db.angelList

# starting to count time to get full duration of run time
start = time.time()

# update stage
cont = 0
for startup in angelList.find({'stage' : ''}):
  name = startup['name']
  cont += 1
  angelList.update_one({'name' : name}, {'$unset' : {'stage': 1}})
print('updated {} stage!'.format(cont))
print('\n')

# update stage
cont = 0
for startup in angelList.find({'stage' : '-'}):
  name = startup['name']
  cont += 1
  angelList.update_one({'name' : name}, {'$unset' : {'stage': 1}})
print('updated {} stage!'.format(cont))
print('\n')

# update amount raised
cont = 0
for startup in angelList.find({'amount raised' : ''}):
  name = startup['name']
  cont += 1
  angelList.update_one({'name' : name}, {'$unset' : {'amount raised': 1}})
print('updated {} amount raised!'.format(cont))
print('\n')

# update amount raised
cont = 0
for startup in angelList.find({'amount raised' : '-'}):
  name = startup['name']
  cont += 1
  angelList.update_one({'name' : name}, {'$unset' : {'amount raised': 1}})
print('updated {} amount raised!'.format(cont))
print('\n')

# update number of employees
cont = 0
for startup in angelList.find({'number of employees' : ''}):
  name = startup['name']
  cont += 1
  angelList.update_one({'name' : name}, {'$unset' : {'number of employees': 1}})
print('updated {} number of employees!'.format(cont))
print('\n')

# update number of employees
cont = 0
for startup in angelList.find({'number of employees' : '-'}):
  name = startup['name']
  cont += 1
  angelList.update_one({'name' : name}, {'$unset' : {'number of employees': 1}})
print('updated {} number of employees!'.format(cont))
print('\n')

# update location
cont = 0
for startup in angelList.find({'location' : ''}):
  name = startup['name']
  cont += 1
  angelList.update_one({'name' : name}, {'$unset' : {'location': 1}})
print('updated {} location!'.format(cont))
print('\n')

# update location
cont = 0
for startup in angelList.find({'location' : '-'}):
  name = startup['name']
  cont += 1
  angelList.update_one({'name' : name}, {'$unset' : {'location': 1}})
print('updated {} location!'.format(cont))
print('\n')

# update pitch
cont = 0
for startup in angelList.find({'pitch' : ''}):
  name = startup['name']
  cont += 1
  angelList.update_one({'name' : name}, {'$unset' : {'pitch': 1}})
print('updated {} pitch!'.format(cont))
print('\n')

# update pitch
cont = 0
for startup in angelList.find({'pitch' : '-'}):
  name = startup['name']
  cont += 1
  angelList.update_one({'name' : name}, {'$unset' : {'pitch': 1}})
print('updated {} pitch!'.format(cont))
print('\n')

# update founded
cont = 0
for startup in angelList.find({'founded' : ''}):
  name = startup['name']
  cont += 1
  angelList.update_one({'name' : name}, {'$unset' : {'founded': 1}})
print('updated {} founded!'.format(cont))
print('\n')

# update founded
cont = 0
for startup in angelList.find({'founded' : '-'}):
  name = startup['name']
  cont += 1
  angelList.update_one({'name' : name}, {'$unset' : {'founded': 1}})
print('updated {} founded!'.format(cont))
print('\n')

# update market
cont = 0
for startup in angelList.find({'market' : ''}):
  name = startup['name']
  cont += 1
  angelList.update_one({'name' : name}, {'$unset' : {'market': 1}})
print('updated {} market!'.format(cont))
print('\n')

# update market
cont = 0
for startup in angelList.find({'market' : '-'}):
  name = startup['name']
  cont += 1
  angelList.update_one({'name' : name}, {'$unset' : {'market': 1}})
print('updated {} market!'.format(cont))
print('\n')

# update website
cont = 0
for startup in angelList.find({'website' : ''}):
  name = startup['name']
  cont += 1
  angelList.update_one({'name' : name}, {'$unset' : {'website': 1}})
print('updated {} website!'.format(cont))
print('\n')

# update website
cont = 0
for startup in angelList.find({'website' : '-'}):
  name = startup['name']
  cont += 1
  angelList.update_one({'name' : name}, {'$unset' : {'website': 1}})
print('updated {} website!'.format(cont))
print('\n')

# gets the end time and print the duration
end = time.time()
dutration = ((end - start) / 60)
print('duration was {} min'.format(dutration))



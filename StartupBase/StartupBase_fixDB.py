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

# update infos
cont = 0
for startup in startupBase.find({'info' : ''}):
  name = startup['name']
  cont += 1
  startupBase.update_one({'name' : name}, {'$unset' : {'info': 1}})
print('updated {} infos!'.format(cont))
print('\n')

# update locations
cont = 0
for startup in startupBase.find({'location' : '-'}):
  name = startup['name']
  cont += 1
  startupBase.update_one({'name' : name}, {'$unset' : {'location': 1}})
print('updated {} locations!'.format(cont))
print('\n')

# update markets
cont = 0
for startup in startupBase.find({'market' : '-'}):
  name = startup['name']
  cont += 1
  startupBase.update_one({'name' : name}, {'$unset' : {'market' : '-'}})
print('updated {} markets!'.format(cont))
print('\n')

# update foundations
cont = 0
for startup in startupBase.find({'foundation' : '(Não informado)'}):
  name = startup['name']
  cont += 1
  startupBase.update_one({'name' : name}, {'$unset' : {'foundation' : '(Não informado)'}})
print('updated {} foundations!'.format(cont))
print('\n')

# update target audience
cont = 0
for startup in startupBase.find({'target audience' : 'S/N'}):
  name = startup['name']
  cont += 1
  startupBase.update_one({'name' : name}, {'$unset' : {'target audience' : 'S/N'}})
print('updated {} target audience!'.format(cont))
print('\n')

# update moment
cont = 0
for startup in startupBase.find({'moment' : 'S/N'}):
  name = startup['name']
  cont += 1
  startupBase.update_one({'name' : name}, {'$unset' : {'moment' : 'S/N'}})
print('updated {} moment!'.format(cont))
print('\n')

# update revenue model
cont = 0
for startup in startupBase.find({'revenue model' : 'S/N'}):
  name = startup['name']
  cont += 1
  startupBase.update_one({'name' : name}, {'$unset' : {'revenue model' : 'S/N'}})
print('updated {} revenue model!'.format(cont))
print('\n')

# update employees
cont = 0
for startup in startupBase.find({'employees' : '(não informado)'}):
  name = startup['name']
  cont += 1
  startupBase.update_one({'name' : name}, {'$unset' : {'employees' : '(não informado)'}})
print('updated {} employees!'.format(cont))
print('\n')

# gets the end time and print the duration
end = time.time()
dutration = ((end - start) / 60)
print('duration was {} min'.format(dutration))
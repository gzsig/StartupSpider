import pymongo
from pymongo import MongoClient
import dns
import time

from collections import OrderedDict
from operator import itemgetter   

# Getting acces to database
password = ""
with open("password.txt", "r") as password_file:
  password = password_file.readline()


client = pymongo.MongoClient(password)
db = client.startupsDB

# saving collections in variables
allStartups = db.allStartups
angelList = db.angelList
dealBook = db.dealBook
startSe = db.startSe
startupBase = db.startupBase
cont = 0


for startup in startupBase.find():
  name = startup['name']
  for startse in startSe.find({'name' : name}):
    startup.update(startse)
  for angellist in angelList.find({'name' : name}):
    startup.update(angellist)

  if allStartups.find_one({'name' : str(name)}) == None and str(name) != '':
    allStartups.insert_one(startup)
    cont += 1
    print(cont)
    print('{} saved!'.format(name))
    print('\n')
  else:
    cont += 1
    print(cont)
    print('{} already exists!'.format(name))
    print('\n')

for startup in startSe.find():
  name = startup['name']
  for startupbase in startupBase.find({'name' : name}):
    startup.update(startupbase)
  for angellist in angelList.find({'name' : name}):
    startup.update(angellist)
  if allStartups.find_one({'name' : str(name)}) == None and str(name) != '':
    allStartups.insert_one(startup)
    cont += 1
    print(cont)
    print('{} saved!'.format(name))
    print('\n')
  else:
    cont += 1
    print(cont)
    print('{} already exists!'.format(name))
    print('\n')

for startup in angelList.find():
  name = startup['name']
  for startupbase in startupBase.find({'name' : name}):
    startup.update(startupbase)
  for startse in startSe.find({'name' : name}):
    startup.update(startse)
  if allStartups.find_one({'name' : str(name)}) == None and str(name) != '':
    allStartups.insert_one(startup)
    cont += 1
    print(cont)
    print('{} saved!'.format(name))
    print('\n')
  else:
    cont += 1
    print(cont)
    print('{} already exists!'.format(name))
    print('\n')
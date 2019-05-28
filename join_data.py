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

  cont += 1
  print(cont)
  print(startup)
  print('\n')


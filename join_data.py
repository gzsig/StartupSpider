import pymongo
from pymongo import MongoClient
import dns
import time

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


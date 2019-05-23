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

client = pymongo.MongoClient("mongodb+srv://gabriel:Gz%40db3611@cluster0-ozy7g.mongodb.net/test?retryWrites=true")
db = client.startupsDB
startupBase = db.startupBase

driver = webdriver.Chrome()

start = time.time()
# MY FUTER CODE

end = time.time()
print(end - start)

driver.close()
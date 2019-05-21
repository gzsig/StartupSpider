import pymongo
from pymongo import MongoClient
import random
from selenium import webdriver
import time

# source env/bin/activate 
# brew services start mongodb

client = MongoClient('mongodb://localhost:27017/')
db = client.startupsDB
startse = db.startse

start = time.time()

driver = webdriver.Chrome()

cont = 0

startups = startse.find({}, no_cursor_timeout=True)

for startup in startups:
#   if cont > 3:
#     break

  cont+=1
  link = startup['startSe link']
  name = startup['name']

  driver.get(link)
  time.sleep(random.randint(1,3))
  website = driver.find_elements_by_xpath("//a[@class='fn mr-15 text-link small']")
  social_media = driver.find_elements_by_xpath("//a[@class='fn pr-15 text-link small']")

  if len(website) > 0:
    website = website[0].get_attribute('href')
    time.sleep(random.randint(1,2))
    startse.update_one({'name':name}, {'$set' : {'website': website}})
    print(str(cont) + '- {} website saved!'.format(name))
  if len(social_media) > 0:
    for link in social_media:
      link = link.get_attribute('href')
      if "facebook" in link:
        startse.update_one({'name':name}, {'$set' : {'facebook': link}})
        print('facebook: {} SAVED!'.format(link))
      elif "linkedin" in link:
        print('linkedin: {} SAVED!'.format(link))
        startse.update_one({'name':name}, {'$set' : {'linkedin': link}})
      elif "youtube" in link:
        print('youtube: {} SAVED!'.format(link))     
        startse.update_one({'name':name}, {'$set' : {'youtubre': link}})
      elif "instagram" in link:
        print('instagram: {} SAVED!'.format(link))       
        startse.update_one({'name':name}, {'$set' : {'instagram': link}})
      elif "twitter" in link:
        print('twitter: {} SAVED!'.format(link))       
        startse.update_one({'name':name}, {'$set' : {'twitter': link}})

end = time.time()
startups.close()
print(end - start)
driver.close()
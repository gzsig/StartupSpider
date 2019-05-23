import pymongo
from pymongo import MongoClient
import random
from selenium import webdriver
import time

# source env/bin/activate 
# brew services start mongodb

client = pymongo.MongoClient("mongodb+srv://gabriel:Gz%40db3611@cluster0-ozy7g.mongodb.net/test?retryWrites=true")
db = client.startupsDB
startse = db.startSe

start = time.time()

driver = webdriver.Chrome()
driver.maximize_window()

cont = 0

startups = startse.find({}, no_cursor_timeout=True)

for startup in startups:
  # if cont > 7:
  #   break

  cont+=1
  link = startup['internal link']
  name = startup['name']

#   if "facebook" in startup.keys():
#     print(startup["name"],startup["facebook"])
#   else:
#     print((startup["name"]))

  driver.get(link)
  time.sleep(random.randint(1,3))
  website = driver.find_elements_by_xpath("//a[@class='fn mr-15 text-link small']")
  social_media = driver.find_elements_by_xpath("//a[@class='fn pr-15 text-link small']")
  content = driver.find_element_by_class_name('col-md-8')

  info = content.find_elements_by_tag_name('p')
  if len(info) > 1:
    main_info = info[0].text
    extra_info = info[1].text
    startse.update_one({'name':name}, {'$set' : {'info': main_info}})
    startse.update_one({'name':name}, {'$set' : {'extra info': extra_info}})
    print('TWO infos saved!')
  elif len(info) > 0:
    main_info = info[0].text
    startse.update_one({'name':name}, {'$set' : {'info': main_info}})
    print('ONE info saved!')
  else:
    main_info = 'no info available'
    startse.update_one({'name':name}, {'$set' : {'info': main_info}})
    print('NO info given')

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
        startse.update_one({'name':name}, {'$set' : {'youtube': link}})
      elif "instagram" in link:
        print('instagram: {} SAVED!'.format(link))       
        startse.update_one({'name':name}, {'$set' : {'instagram': link}})
      elif "twitter" in link:
        print('twitter: {} SAVED!'.format(link))       
        startse.update_one({'name':name}, {'$set' : {'twitter': link}})
  time.sleep(random.randint(1,3))

end = time.time()
startups.close()
print(end - start)
driver.close()
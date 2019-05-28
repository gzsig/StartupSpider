import pymongo
from pymongo import MongoClient
import random
from selenium import webdriver
import time

# source env/bin/activate 

# Getting access to database
password = ""
with open("password.txt", "r") as password_file:
  password = password_file.readline()

client = pymongo.MongoClient(password)
db = client.startupsDB
# saving collections in variables
startse = db.startSe
# starting to count time to get full duration of run time
start = time.time()
# open broweser
driver = webdriver.Chrome()
driver.maximize_window()

cont = 1

# allow query to run for longer than 10minutes
startups = startse.find({}, no_cursor_timeout=True)

for startup in startups:
  # if cont > 7:
  #   break

  cont+=1
  link = startup['internal link']
  name = startup['name']
  # check if startup hasn't already been individually scraped
  if 'info' not in startup.keys():
    if "comunidade.startse.com" in link:
      # gets open browser and goes to internal link
      driver.get(link)
      # lets driver finish loading link
      time.sleep(random.randint(1,3))
      # gets website link
      website = driver.find_elements_by_xpath("//a[@class='fn mr-15 text-link small']")
      # gets social media links
      social_media = driver.find_elements_by_xpath("//a[@class='fn pr-15 text-link small']")
      content = driver.find_element_by_class_name('col-md-8')

      info = content.find_elements_by_tag_name('p')
      # checks who many descriptions are given and saves
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
      # if website exists then save
      if len(website) > 0:
        website = website[0].get_attribute('href')
        time.sleep(random.randint(1,2))
        startse.update_one({'name':name}, {'$set' : {'website': website}})
        print(str(cont) + '- {} website saved!'.format(name))
      if len(social_media) > 0:
        # saves each social media link
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
# gets the end time and print the duration
end = time.time()
# close query
startups.close()
print(end - start)
# close chrome
driver.close()
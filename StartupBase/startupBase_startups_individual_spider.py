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

driver = webdriver.Chrome()
driver.maximize_window()

# starting to count time to get full duration of run time
start = time.time()

cont = 0

for startup in startupBase.find():
  cont += 1
  link = startup['internal link']
  name = startup['name']
  # check if startup hasn't already been individually scraped
  if 'moment' not in startup.keys():
    # gets open browser and goes to internal link
    driver.get(link)
    # checks if link is not broken
    if len(driver.find_elements_by_css_selector('.startup-timely__data.has-text-weight-semibold.sb-size-6')) > 0:
      specific_info = []
      # pauses while selenium saves class into variable
      while specific_info == []:
        specific_info = driver.find_elements_by_css_selector('.startup-timely__data.has-text-weight-semibold.sb-size-6')


      publico_alvo = specific_info[1].text
      modelo_de_receita = specific_info[2].text
      momento = specific_info[3].text

      # saves target audience, revenue model and moment to DB
      startupBase.update_one({'name':name}, {'$set' : {'target audience': publico_alvo}})
      startupBase.update_one({'name':name}, {'$set' : {'revenue model': modelo_de_receita}})
      startupBase.update_one({'name':name}, {'$set' : {'moment': momento}})

      # check if startup has badges
      if len(driver.find_elements_by_css_selector('.column.is-half-mobile.is-one-third-tablet.is-one-quarter-desktop')) > 0:
        cards = driver.find_elements_by_css_selector('.column.is-half-mobile.is-one-third-tablet.is-one-quarter-desktop')
        badges = []
        for card in cards:

          badge = {
            'type' : card.find_element_by_css_selector('.badge__tagline.sb-size-11').text,
            'accomplishment name' : card.find_element_by_css_selector('.badge__name.sb-size-10.has-text-weight-bold').text,
            'date' : card.find_element_by_css_selector('.badge__data.sb-size-11').text
          }
        
        badges.append(badge)
        # saves badges to DB
        startupBase.update_one({'name':name}, {'$set' : {'badges' : badges}})

      # checks for extra info and saves to DB
      if len(driver.find_elements_by_css_selector('.mold-text.mold-about__text.sb-size-9')) > 0:
        about = driver.find_element_by_css_selector('.mold-text.mold-about__text.sb-size-9').text
        startupBase.update_one({'name':name},{'$set' : {'about' : about}})

      # check for specific people related to this startup and saves to DB
      if len(driver.find_elements_by_css_selector('.member__body')) > 0:
        people = driver.find_elements_by_css_selector('.member__body')
        members = []
        for person in people:
          if len(person.find_elements_by_css_selector('.member__link')) > 0:
            member = {
              'name' : person.find_element_by_css_selector('.member__name').text,
              'position' : person.find_element_by_css_selector('.member__title').text,
              'linkedin' : person.find_element_by_css_selector('.member__link').get_attribute('href')
            }
          else:
            member = {
              'name' : person.find_element_by_css_selector('.member__name').text,
              'position' : person.find_element_by_css_selector('.member__title').text,
            }

          members.append(member)
      startupBase.update_one({'name':name}, {'$set' : {'members': members}})

      # gets foundation date, number of employees and when it was last updated and saves to DB
      info_card = driver.find_element_by_css_selector('.mold-aside.has-background-white')
      foundation = info_card.find_elements_by_css_selector('.mold-text.sb-size-10')[0].text
      employees = info_card.find_elements_by_css_selector('.mold-text.sb-size-10')[1].text
      last_update = info_card.find_elements_by_css_selector('.mold-text.sb-size-10')[2].text

      startupBase.update_one({'name':name}, {'$set' : {'foundation': foundation}})
      startupBase.update_one({'name':name}, {'$set' : {'employees': employees}})
      startupBase.update_one({'name':name}, {'$set' : {'last updated': last_update}})

      # checks for social media links and website, if avaiable saves to DB
      social_media = info_card.find_elements_by_css_selector('.out-social__link.has-text-centered')
      if len(social_media) > 0:
        for link in social_media:
          link = link.get_attribute('href')
          if "facebook" in link:
            startupBase.update_one({'name':name}, {'$set' : {'facebook': link}})
          elif "linkedin" in link:
            startupBase.update_one({'name':name}, {'$set' : {'linkedin': link}})
          elif "twitter" in link:
            startupBase.update_one({'name':name}, {'$set' : {'twitter': link}})

      website = info_card.find_elements_by_css_selector('.out-channel.is-radius3.is-unselectable')
      if len(website) > 0:
        website = info_card.find_element_by_css_selector('.out-channel.is-radius3.is-unselectable')
        website = website.get_attribute('href')
        startupBase.update_one({'name':name}, {'$set' : {'website': website}})
      # after all possible data is saved prints success msg
      print(str(cont) + '- {} saved extra info'.format(name))
      print('\n')
      time.sleep(random.randint(1,2))
  else:
    # if startup already has this extra data print warning msg
    print(str(cont) + '- {} already has extra info'.format(name))

# gets the end time and print the duration
end = time.time()
dutration = ((end - start) / 60)
print('duration was {} min'.format(dutration))
# close chrome
driver.close()
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

password = ""
with open("password.txt", "r") as password_file:
  password = password_file.readline()

client = pymongo.MongoClient(password)
db = client.startupsDB
startupBase = db.startupBase

driver = webdriver.Chrome()

start = time.time()

cont = 0

for startup in startupBase.find():
  if cont > 5:
    break
  cont += 1
  link = startup['internal link']
  name = startup['name']
  driver.get(link)

  if 'momento' not in startup.keys():

    specific_info = []
    while specific_info == []:
      specific_info = driver.find_elements_by_css_selector('.startup-timely__data.has-text-weight-semibold.sb-size-6')

    # print('PÚBLICO-ALVO: {}'.format(specific_info[1].text))
    # print('MODELO DE RECEITA: {}'.format(specific_info[2].text))
    # print('MOMENTO: {}'.format(specific_info[3].text))

    publico_alvo = specific_info[1].text
    modelo_de_receita = specific_info[2].text
    momento = specific_info[3].text

    startupBase.update_one({'name':name}, {'$set' : {'publico alvo': publico_alvo}})
    startupBase.update_one({'name':name}, {'$set' : {'modelo de receita': modelo_de_receita}})
    startupBase.update_one({'name':name}, {'$set' : {'momento': momento}})

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
      startupBase.update_one({'name':name}, {'$set' : {'badges' : badges}})

        # print('type: {}'.format(card.find_element_by_css_selector('.badge__tagline.sb-size-11').text))
        # print('accomplishment name: {}'.format(card.find_element_by_css_selector('.badge__name.sb-size-10.has-text-weight-bold').text))
        # print('date: {}'.format(card.find_element_by_css_selector('.badge__data.sb-size-11').text))

    if len(driver.find_elements_by_css_selector('.mold-text.mold-about__text.sb-size-9')) > 0:
      # print('about: {}'.format(driver.find_element_by_css_selector('.mold-text.mold-about__text.sb-size-9').text))

      about = driver.find_element_by_css_selector('.mold-text.mold-about__text.sb-size-9').text
      startupBase.update_one({'name':name},{'$set' : {'about' : about}})


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

    info_card = driver.find_element_by_css_selector('.mold-aside.has-background-white')
    foundation = info_card.find_elements_by_css_selector('.mold-text.sb-size-10')[0].text
    employees = info_card.find_elements_by_css_selector('.mold-text.sb-size-10')[1].text
    last_update = info_card.find_elements_by_css_selector('.mold-text.sb-size-10')[2].text

    startupBase.update_one({'name':name}, {'$set' : {'members': members}})
    startupBase.update_one({'name':name}, {'$set' : {'foundation': foundation}})
    startupBase.update_one({'name':name}, {'$set' : {'employees': employees}})
    startupBase.update_one({'name':name}, {'$set' : {'last updated': last_update}})

    # print(members)
    # print(foundation)
    # print(employees)
    # print(last_update)

    social_media = info_card.find_elements_by_css_selector('.out-social__link.has-text-centered')
    if len(social_media) > 0:
      for link in social_media:
        link = link.get_attribute('href')
        if "facebook" in link:
          startupBase.update_one({'name':name}, {'$set' : {'facebook': link}})
          # print('facebook: {} SAVED!'.format(link))
        elif "linkedin" in link:
          # print('linkedin: {} SAVED!'.format(link))
          startupBase.update_one({'name':name}, {'$set' : {'linkedin': link}})
        elif "twitter" in link:
          # print('twitter: {} SAVED!'.format(link))       
          startupBase.update_one({'name':name}, {'$set' : {'twitter': link}})

    website = info_card.find_elements_by_css_selector('.out-channel.is-radius3.is-unselectable')
    if len(website) > 0:
      website = info_card.find_element_by_css_selector('.out-channel.is-radius3.is-unselectable')
      website = website.get_attribute('href')
      # print(website)
      startupBase.update_one({'name':name}, {'$set' : {'website': website}})
    print(str(cont) + '- {} saved extra info'.format(name))
    print('\n')
    time.sleep(random.randint(1,3))
  else:
    print(str(cont) + '- {} already has extra info'.format(name))


end = time.time()
dutration = ((end - start) / 60)
print('duration was {} min'.format(dutration))
driver.close()
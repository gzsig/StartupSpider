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

def search(url):
  driver.get(url)
  time.sleep(2)
  driver.maximize_window()
  time.sleep(3)
  for n in range(4):
    if len(driver.find_elements_by_tag_name('card-startup')) > 0:
      startups = driver.find_elements_by_tag_name('card-startup')
      for i in range(len(startups)):
        if startups[i].find_element_by_css_selector(".mb-0") != None:
          name = startups[i].find_element_by_css_selector(".mb-0").text
        else:
          name = '-'
        if startups[i].find_element_by_css_selector(".col-4.sb-card__verified") != None:
          logo = startups[i].find_element_by_css_selector(".col-4.sb-card__verified").find_element_by_tag_name('img').get_attribute('src')
        else:
          logo = '-'
        if startups[i].find_element_by_tag_name('small') != None:
          location = startups[i].find_element_by_tag_name('small').text
        else:
          location = '-'
        if len(startups[i].find_elements_by_class_name('text-center')) > 0:
          info = startups[i].find_element_by_class_name('text-center').text
        else:
          info = '-'
        if startups[i].find_element_by_tag_name('a') != None:
          internal_link = startups[i].find_element_by_tag_name('a').get_attribute('href')
        else:
          internal_link = '-'

        if startupBase.find_one({'name' : str(name)}) == None and str(name) != '':
          data = {
            'name' : str(name),
            'location' : str(location),
            'logo' : str(logo),
            'info' : str(info),
            'internal link' : str(internal_link)
          }
          startupBase.insert_one(data)
          print('{} saved!'.format(data))
          # print('{} saved!'.format(logo))
          # print('{} saved!'.format(location))
          # print('{} saved!'.format(info))
          # print('{} saved!'.format(internal_link))
          print('\n')
        else:
          print('{} already in DB!'.format(name))
        time.sleep(random.randint(1,3))

    if len(driver.find_elements_by_css_selector('.pagination-next.page-item')) > 0:
      driver.find_element_by_xpath('/html/body/app-root/app-list/div[2]/div/div/div[2]/div[1]/pagination/ul/li[8]/a').click()
    else:
      break


# links = [
#   'https://startupbase.abstartups.com.br/startups?hitsPerPage=80&refinementList%5Bbusiness_target%5D%5B0%5D=B2B',
#   'https://startupbase.abstartups.com.br/startups?hitsPerPage=80&refinementList%5Bbusiness_phase%5D%5B0%5D=Idea%C3%A7%C3%A3o&refinementList%5Bbusiness_phase%5D%5B1%5D=Opera%C3%A7%C3%A3o&refinementList%5Bbusiness_target%5D%5B0%5D=B2B',
#   'https://startupbase.abstartups.com.br/startups?hitsPerPage=80&refinementList%5Bbusiness_phase%5D%5B0%5D=Scaleup&refinementList%5Bbusiness_phase%5D%5B1%5D=Tra%C3%A7%C3%A3o&refinementList%5Bbusiness_target%5D%5B0%5D=B2B',
#   'https://startupbase.abstartups.com.br/startups?hitsPerPage=80&refinementList%5Bbusiness_model%5D%5B0%5D=API&refinementList%5Bbusiness_model%5D%5B1%5D=Consumer&refinementList%5Bbusiness_model%5D%5B2%5D=E-commerce&refinementList%5Bbusiness_model%5D%5B3%5D=Hardware&refinementList%5Bbusiness_model%5D%5B4%5D=Licenciamento&refinementList%5Bbusiness_model%5D%5B5%5D=Marketplace&refinementList%5Bbusiness_model%5D%5B6%5D=Outros&refinementList%5Bbusiness_model%5D%5B7%5D=Venda%20de%20dados&refinementList%5Bbusiness_target%5D%5B0%5D=B2B',
#   'https://startupbase.abstartups.com.br/startups?hitsPerPage=80&refinementList%5Bbusiness_model%5D%5B0%5D=SaaS&refinementList%5Bbusiness_target%5D%5B0%5D=B2B',
# ''
# ]
search('https://startupbase.abstartups.com.br/startups?hitsPerPage=80&refinementList%5Bbusiness_model%5D%5B0%5D=API&refinementList%5Bbusiness_target%5D%5B0%5D=B2B')

driver.close()

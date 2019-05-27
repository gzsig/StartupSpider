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
startSe = db.startSe

driver = webdriver.Chrome()

start = time.time()

def search(url):
  driver.get(url)
  time.sleep(1)
  driver.maximize_window()
  time.sleep(3)
  i=0
  while len(driver.find_elements_by_class_name('infinite-more-link')) > 0: #pay attention: find_element*s*
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    time.sleep(1)
    i+=1
    if i > 2:
      break

  startups = driver.find_elements_by_xpath("//div[@class='infinite-item mix col-md-2 col-sm-3 col-xs-6 search']")
  for i in range(len(startups)):
    # print(startups[i].find_element_by_tag_name('a').get_attribute('href'))
    # print(startups[i].find_element_by_tag_name('img').get_attribute('src'))
    # print(startups[i].find_element_by_css_selector(".fb.m-0.p-lines.h5-lines-2").text)
    # print(startups[i].find_element_by_css_selector('.small.text-muted.p-lines.p-lines-1.m-0').text)
    # print('\n')

    if len(startups[i].find_elements_by_tag_name('a')) > 0:
      internal_link = startups[i].find_element_by_tag_name('a').get_attribute('href')
    else:
      internal_link = '-'
    if len(startups[i].find_elements_by_tag_name('img')) > 0:
      logo = startups[i].find_element_by_tag_name('img').get_attribute('src')
    else:
      logo = '-'
    if len(startups[i].find_elements_by_css_selector(".fb.m-0.p-lines.h5-lines-2")) > 0:
      name = startups[i].find_element_by_css_selector(".fb.m-0.p-lines.h5-lines-2").text
    else:
      name = '-'
    if len(startups[i].find_elements_by_css_selector('.small.text-muted.p-lines.p-lines-1.m-0')) > 0:
      location = startups[i].find_element_by_css_selector('.small.text-muted.p-lines.p-lines-1.m-0').text
    else:
      location = '-'
    
    if startSe.find_one({'name' : str(name)}) == None and str(name) != '':
      data = {
        'name' : str(name),
        'location' : str(location),
        'logo' : str(logo),
        'internal link' : str(internal_link)
      }
      startSe.insert_one(data)
      print('{} saved!'.format(name))
      print('\n')
    else:
      print('{} already exists in DB!'.format(name))
      
search('https://comunidade.startse.com/startups')

end = time.time()
print(end - start)

driver.close()

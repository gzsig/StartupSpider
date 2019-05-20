import json
import pymongo
from pymongo import MongoClient
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unidecode


# Working

# source env/bin/activate 
# brew services start mongodb

client = MongoClient('mongodb://localhost:27017/')
db = client.startupsDB
startups = db.startups

driver = webdriver.Chrome()


def get_data(xpath, link):

  a = []
  b = []
  c = []
  d = []
  e = []
  f = []
  g = []
  h =[]
  i = []

  driver.get(link)
  time.sleep(5)
  driver.maximize_window()
  driver.find_element_by_xpath(xpath).click()
  time.sleep(10)

  for i in range(0):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    time.sleep(3)
    if len(driver.find_elements_by_class_name('more')) > 0: #pay attention: find_element*s*
      driver.find_element_by_class_name('more').click() #pay attention: find_element
    time.sleep(2)
  time.sleep(5)

  names = driver.find_elements_by_class_name('company')
  for element in names:
    result_list = unidecode.unidecode(element.text)
    a.append(result_list)
  print(a)


  stages = driver.find_elements_by_class_name('stage')
  for element in stages:
    if element.text == '':
      result_list = '-'
    else:
      result_list = element.text
    b.append(result_list)
  print(b)

  joins = driver.find_elements_by_class_name('joined')
  for element in joins:
    if element.text == '':
      result_list = '-'
    else:
      result_list = element.text
    c.append(result_list)
  print(c)

  locations = driver.find_elements_by_class_name('location')
  for element in locations:
    if element.text == '':
      result_list = '-'
    else:
      result_list = element.text
    d.append(result_list)
  print(d)

  markets = driver.find_elements_by_class_name('market')
  for element in markets:
    if element.text == '':
      result_list = '-'
    else:
      result_list = element.text
    e.append(result_list)
  print(e)

  websites = driver.find_elements_by_xpath("//div[@class='column website']")
  for element in websites:
    if element.text == '':
      result_list = '-'
    else:
      result_list = element.text
    f.append(result_list)
  print(f)

  sizes = driver.find_elements_by_class_name('company_size')
  for element in sizes:
    if element.text == '':
      result_list = '-'
    else:
      result_list = element.text
    g.append(result_list)
  print(g)

  raises = driver.find_elements_by_class_name('raised')
  for element in raises:
    if element.text == '':
      result_list = '-'
    else:
      result_list = element.text
    h.append(result_list)
  print(h)

  angel_links = driver.find_elements_by_class_name('startup-link')
  print(len(angel_links))
  for element in angel_links:
    result_list = str(element.get_attribute('href'))
    i.append(result_list)
  print(i)

  print(len(a))
  print(len(b))
  print(len(c))
  print(len(d))
  print(len(e))
  print(len(f))
  print(len(g))
  print(len(h))
  print(len(i))

#   cont = 0

#   while cont < len(a):
#     name = a[cont]
#     created = c[cont]
#     location = d[cont]
#     market = e[cont]
#     website = f[cont]
#     employees = g[cont]
#     stage = b[cont]
#     raised = h[cont]
#     if startups.find_one({'name' : str(name)}) == None and str(name) != '':
#       data = {
#         'name' : str(name),
#         'foundation' : str(created),
#         'location' : str(location),
#         'market' : str(market),
#         'website' : str(website),
#         'number of employees' : str(employees),
#         'stage' : str(stage),
#         'total amount raised' : str(raised),
#       }
#       print('{} saved!'.format(name))
#       cont+=1
#       startups.insert_one(data)
#     else:
#       cont+=1


# urls = [
# 'https://angel.co/companies?locations[]=1622-Brazil',
# 'https://angel.co/companies?locations[]=1622-Brazil&company_types[]=Startup',
# 'https://angel.co/companies?locations[]=1622-Brazil&company_types[]=VC+Firm',
# 'https://angel.co/companies?locations[]=1622-Brazil&company_types[]=Private+Company',
# 'https://angel.co/companies?locations[]=1622-Brazil&company_types[]=SaaS',
# 'https://angel.co/companies?locations[]=1622-Brazil&company_types[]=Incubator',
# 'https://angel.co/companies?locations[]=1622-Brazil&company_types[]=Mobile+App',
# 'https://angel.co/companies?locations[]=1622-Brazil&stage=Seed',
# 'https://angel.co/companies?locations[]=1622-Brazil&stage=Series+A',
# 'https://angel.co/companies?locations[]=1622-Brazil&stage=Series+B',
# 'https://angel.co/companies?locations[]=1622-Brazil&stage=Series+C',
# 'https://angel.co/companies?locations[]=1622-Brazil&stage[]=Acquired',
# 'https://angel.co/companies?locations[]=1622-Brazil&markets[]=E-Commerce',
# 'https://angel.co/companies?locations[]=1622-Brazil&markets[]=Education',
# 'https://angel.co/companies?locations[]=1622-Brazil&markets[]=Enterprise+Software',
# 'https://angel.co/companies?locations[]=1622-Brazil&markets[]=Games',
# 'https://angel.co/companies?locations[]=1622-Brazil&markets[]=Healthcare',
# 'https://angel.co/companies?locations[]=1622-Brazil&markets[]=Mobile'
# ]

# for url in urls:
#   get_data('//*[@id="root"]/div[4]/div[2]/div/div[2]/div[2]/div[2]/div[1]/div/div[2]', url)
#   time.sleep(random.randint(6,12))
#   get_data('//*[@id="root"]/div[4]/div[2]/div/div[2]/div[2]/div[2]/div[1]/div/div[3]', url)
#   time.sleep(random.randint(6,12))
#   get_data('//*[@id="root"]/div[4]/div[2]/div/div[2]/div[2]/div[2]/div[1]/div/div[9]', url)
#   time.sleep(random.randint(10,15))

get_data('//*[@id="root"]/div[4]/div[2]/div/div[2]/div[2]/div[2]/div[1]/div/div[2]', 'https://angel.co/companies?locations[]=1622-Brazil')

driver.close()

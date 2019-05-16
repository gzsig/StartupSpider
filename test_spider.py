import json
import pymongo
from pymongo import MongoClient
from selenium import webdriver
import unidecode
import time

# source env/bin/activate 
# brew services start mongodb

client = MongoClient('mongodb://localhost:27017/')
db = client.startupsDB
startups = db.startups

driver = webdriver.Chrome()

a = []
b = []
c = []
d = []
e = []
f = []
g = []
h =[]

def get_data(xpath):
  driver.get("https://angel.co/companies?locations[]=1622-Brazil")
  time.sleep(5)
  driver.find_element_by_xpath(xpath).click()
  time.sleep(10)

  for i in range(20):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    time.sleep(1)
    driver.find_element_by_class_name('more').click()
    time.sleep(2)
  time.sleep(5)

  names = driver.find_elements_by_class_name('company')
  for element in names:
    result_list = unidecode.unidecode(element.text)
    a.append(result_list)
  # print(a)


  stages = driver.find_elements_by_class_name('stage')
  for element in stages:
    if element.text == '':
      result_list = '-'
    else:
      result_list = element.text
    b.append(result_list)
  # print(b)

  joins = driver.find_elements_by_class_name('joined')
  for element in joins:
    if element.text == '':
      result_list = '-'
    else:
      result_list = element.text
    c.append(result_list)
  # print(c)

  locations = driver.find_elements_by_class_name('location')
  for element in locations:
    if element.text == '':
      result_list = '-'
    else:
      result_list = element.text
    d.append(result_list)
  # print(d)

  markets = driver.find_elements_by_class_name('market')
  for element in markets:
    if element.text == '':
      result_list = '-'
    else:
      result_list = element.text
    e.append(result_list)
  # print(e)

  websites = driver.find_elements_by_xpath("//div[@class='column website']")
  for element in websites:
    if element.text == '':
      result_list = '-'
      # f.append(result_list)
    else:
      result_list = element.text
      # if element.text not in f:
    f.append(result_list)
  # print(f)

  sizes = driver.find_elements_by_class_name('company_size')
  for element in sizes:
    if element.text == '':
      result_list = '-'
    else:
      result_list = element.text
    g.append(result_list)
  # print(g)

  raises = driver.find_elements_by_class_name('raised')
  for element in raises:
    if element.text == '':
      result_list = '-'
    else:
      result_list = element.text
    h.append(result_list)
  # print(h)

  print(len(a))
  print(len(b))
  print(len(c))
  print(len(d))
  print(len(e))
  print(len(f))
  print(len(g))
  print(len(h))

  # cont = 0
  # loopmax = len(a)

  # while cont < loopmax-1:
  #   name = a[cont]
  #   created = c[cont]
  #   location = d[cont]
  #   market = e[cont]
  #   website = f[cont]
  #   employees = g[cont]
  #   stage = b[cont]
  #   raised = h[cont]
  #   if startups.find_one({'name' : str(name)}) == None and str(name) != '':
  #     data = {
  #       'name' : str(name),
  #       'foundation' : str(created),
  #       'location' : str(location),
  #       'market' : str(market),
  #       'website' : str(website),
  #       'number of employees' : str(employees),
  #       'stage' : str(stage),
  #       'total amount raised' : str(raised),
  #     }
  #     print('{} saved!'.format(name))
  #     print(cont)
  #     cont+=1
  #     startups.insert_one(data)
  #   else:
  #     print(cont)
  #     cont+=1


# get_data('//*[@id="root"]/div[4]/div[2]/div/div[2]/div[2]/div[2]/div[1]/div/div[2]')
# get_data('//*[@id="root"]/div[4]/div[2]/div/div[2]/div[2]/div[2]/div[1]/div/div[3]')
get_data('//*[@id="root"]/div[4]/div[2]/div/div[2]/div[2]/div[2]/div[1]/div/div[9]')

driver.close()

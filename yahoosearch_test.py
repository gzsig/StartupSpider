from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random

browser = webdriver.Chrome()

def testing(word, wordone):
  browser.get('http://www.yahoo.com')
  assert 'Yahoo' in browser.title

  elem = browser.find_element_by_name('p')  # Find the search box
  elem.send_keys(word + wordone + Keys.RETURN)

myList = ["The", "earth", "revolves", "around", "sun"]

for text in myList:
  testing("one", text)
  time.sleep(random.randint(6,12))
  testing("tow", text)
  time.sleep(random.randint(6,12))
  testing("three", text)
  time.sleep(random.randint(6,12))

browser.close()
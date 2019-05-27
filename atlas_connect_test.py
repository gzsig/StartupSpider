import pymongo
import dns # required for connecting with SRV


password = ""
with open("password.txt", "r") as password_file:
  password = password_file.readline()

client = pymongo.MongoClient(password)
db = client.test
test_one = db.test_one

data = {
  'name' : 'Matheus',
}

test_one.insert_one(data)
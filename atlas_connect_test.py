import pymongo
import dns # required for connecting with SRV


client = pymongo.MongoClient("mongodb+srv://gabriel:Gz%40db3611@cluster0-ozy7g.mongodb.net/test?retryWrites=true")
db = client.test
test_one = db.test_one

data = {
  'name' : 'Matheus',
}

test_one.insert_one(data)
import pymongo
import certifi

connection_string =  "mongodb+srv://alexisaldrete:Beagle98@cluster0.nryiv7p.mongodb.net/?retryWrites=true&w=majority"

client = pymongo.MongoClient(connection_string, tlsCAFile=certifi.where())

db = client.get_database("FoodStoreDb")
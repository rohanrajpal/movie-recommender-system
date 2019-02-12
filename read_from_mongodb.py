from pymongo import MongoClient
import pandas as pd

# pprint library is used to make the output look more pretty
from pprint import pprint
# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
client = MongoClient('mongodb://localhost:27017/')
db=client.admin

pprint(db.movies.find_one({'Year': 1996}))
pprint(db.list_collection_names())
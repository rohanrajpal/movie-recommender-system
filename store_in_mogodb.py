from pymongo import MongoClient
import pandas as pd

def solve():
  # pprint library is used to make the output look more pretty
  from pprint import pprint
  # connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
  client = MongoClient('mongodb://localhost:27017/')
  # client.drop_database('movies')
  db = client['movies']
  mycol = db['movie_data']

  # # Issue the serverStatus command and print the results
  # # serverStatusResult=db.command("serverStatus")
  # # pprint(serverStatusResult)

  # movies = db.movies
  # # print(record)
  # df = pd.read_csv("data/smaller_data/movie_data.csv") #csv file which you want to import
  # records_ = df.to_dict(orient = 'records')
  # result = mycol.insert_many(records_ )
  # for x in mycol.find():
  #   print(x)
  print(mycol.find_one({'MovieID': 29}))
  dblist = client.list_database_names()
  print(dblist)
  if "movies" in dblist:
    print("The database exists.")


if __name__ == '__main__':
  solve()
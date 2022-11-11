## Create a MongoDB client, open a connection to Amazon DocumentDB as a replica set and specify the read preference as secondary preferred 
                    
import pymongo
import sys

#mongodb://pragma:pragma123@copapragmadb.cluster-cpoxrljke2qk.us-east-1.docdb.amazonaws.com:27017/?retryWrites=false


client = pymongo.MongoClient('mongodb://pragma:pragma123@copapragmadb.cluster-cpoxrljke2qk.us-east-1.docdb.amazonaws.com:27017/?retryWrites=false')

##Specify the database to be used
#db = client.mapa_crecimiento

db = client['mapa_crecimiento']



##Specify the collection to be used
col = db['chapter']

print(col)

##Find the document that was previously written
x = col.find_one({'id_chapter':'14'})

col.find()

##Print the result to the screen
print(x)

##Close the connection
client.close()
                    
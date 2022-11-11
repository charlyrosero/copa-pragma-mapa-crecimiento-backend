from pymongo import MongoClient
import sys
import logging
import sshtunnel
from sshtunnel import SSHTunnelForwarder
import pandas as pd


#mongodb://pragma:<insertYourPassword>@mapadb.cpoxrljke2qk.us-east-1.docdb.amazonaws.com:27017/?retryWrites=false

# ssh variables
host = '3.93.168.214'
localhost = 'mapadb.cpoxrljke2qk.us-east-1.docdb.amazonaws.com'
ssh_username = 'ec2-user'
ssh_private_key = 'keys/tunnel-ssh.pem'

sshtunnel.DEFAULT_LOGLEVEL = 1


# VM IP/DNS - Will depend on your VM
EC2_URL = 'ec2-3-93-168-214.compute-1.amazonaws.com'

# Mongo URI Will depende on your DocDB instances
DB_URI = 'mapadb.cpoxrljke2qk.us-east-1.docdb.amazonaws.com'

# DB user and password
DB_USER = 'pragma'
DB_PASS = 'pragma123'

# Create the tunnel
server = SSHTunnelForwarder(
    (EC2_URL, 22),
    ssh_username='ec2-user',                # I used an Ubuntu VM, it will be ec2-user for you
    #ssh_pkey='',   # I had to give the full path of the keyfile here    
    ssh_private_key='/Users/charly.rosero/Apps/copa-pragma/tunnel-ssh.pem',    
    remote_bind_address=(DB_URI, 27017),
    local_bind_address=('127.0.0.1', 27017)
)
# Start the tunnel
server.start()

# Connect to Database
client = MongoClient(
    host='127.0.0.1',
    port=27017,
    username='pragma',
    password='pragma123',
    directConnection=True,
    
)


# Close the tunnel once you are done
server.stop()
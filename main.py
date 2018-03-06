#! /usr/bin/env python3
# coding: utf-8

import sys
import json
from ClassDatabase import Database

# I get the config file with categories and login info for the database
with open("../config/config.json") as f:
    config = json.load(f)

# New instance of the databse
pur_beurre = Database(config["user"],config["password"],config["server"])

# If i can connect to the database it means it has been created and filled previously
try :
    pur_beurre.connect()
    print("Cnnexion réussie")
# If it doesn't connect then i create the database
except:
    print("la base n'existe pas")
    # Creates the database
    pur_beurre.create_base()
    # Creates the tables
    pur_beurre.create_tables()
    # Connects to the database and use it
    pur_beurre.connect()
    # Fill the all database
    for category in config["categories"]:
        pur_beurre.fill_in('a',category)
        pur_beurre.fill_in('e',category)

# In case of update
try :
    if sys.argv[1] == '-update':
        print("mise à jour")

except:
    pass
    

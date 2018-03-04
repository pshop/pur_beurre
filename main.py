#! /usr/bin/env python3
# coding: utf-8

import sys
from ClassDatabase import Database

pur_beurre = Database()

try :
    pur_beurre.connect()
    print("Cnnexion réussie")
except:
    print("la base n'existe pas")
    pur_beurre.create_base()
    pur_beurre.create_tables()
    pur_beurre.connect()

try :
    if sys.argv[1] == '-update':
        print("mise à jour")
        pur_beurre.update_data()
except:
    pass

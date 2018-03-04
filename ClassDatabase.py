#! /usr/bin/env python3
# coding: utf-8
import records
from ClassTables import Tables
from ClassImportFromAPI import ImportFromApi
from ClassExtractJson import ExtractFromJson
from ClassUpdateDatabase import UpdateDatabase

class Database:

    def __init__(self):
        self.category_list = ['produits-laitiers','boissons']

    def connect(self):
        self.db = records.Database('mysql+pymysql://root:kcokopv6@localhost')
        self.db.query('USE pur_beurre')
    
    def create_base(self):
        self.db.query('CREATE DATABASE IF NOT EXISTS pur_beurre')
    
    def create_tables(self):
        self.table = Tables()
        self.table.store_create()
        self.table.product_create()
        self.table.category_create()
        self.table.product_category_create()
        self.table.save_create()
        self.table.product_store_create()

    def update_data(self):
        self.import_api = []
        self.json = []
        self.product_list = []

        for cat in self.category_list:
            print(cat)
            self.import_api.append(ImportFromApi('a', cat)) 
            self.import_api.append(ImportFromApi('e', cat))

        for api in self.import_api:
            self.json.append(api.get_json())

        for product in self.json:
            self.product_list.append(ExtractFromJson(product))

        for my_list in self.product_list:
            self.update_db = UpdateDatabase(my_list.extract_json())
            self.update_db.table_store_update()
            self.update_db.table_product_update()
            self.update_db.table_category_update()
            self.update_db.table_product_category_update()

        
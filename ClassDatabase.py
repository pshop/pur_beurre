#! /usr/bin/env python3
# coding: utf-8
import records
import sys

from ClassTablesCreator import TablesCreator
from ClassImportFromAPI import ImportFromApi
from ClassExtractJson import ExtractFromJson
from ClassDatabaseCreator import DatabaseCreator


class Database:

    def __init__(self, usr, pswd, server):
        self.db = None
        self.usr = usr
        self.pswd = pswd
        self.server = server

    def connect(self):
        """ Create a connection to the database """
        self.db = records.Database(
            'mysql+pymysql://{}:{}@{}'.format(self.usr, self.pswd, self.server))
        self.db.query('USE pur_beurre')

    def create_base(self):
        """ Creates the database if it doesn't exist """
        self.db.query('CREATE DATABASE IF NOT EXISTS pur_beurre')

    def create_tables(self):
        """ Create all the tables needed """
        self.table = TablesCreator(self.db)
        self.table.store_create()
        self.table.product_create()
        self.table.category_create()
        self.table.product_category_create()
        self.table.save_create()
        self.table.product_store_create()

    def fill_in(self, grade, category):
        """ fills in the all database with products of the given category and grade """
        api_json = ImportFromApi(grade, category)
        extracted_data = ExtractFromJson(api_json.get_json())
        self.fill_in_db = DatabaseCreator(
            extracted_data.extract_json(), self.db)
        self.fill_in_db.table_store_update()
        self.fill_in_db.table_product_update()
        self.fill_in_db.table_category_update()
        self.fill_in_db.table_product_category_update()
        self.fill_in_db.table_product_store_update()

    def clean_product_category(self):
        """ Deletes relations product_category and product_store witch are not
        linked to saved products. Then delete all the non-saved products """
        try:
            self.db.query("DELETE FROM product_category\
                WHERE PC_PROD_id NOT IN (\
                SELECT SAU_PROD_id FROM save);")
            print("product_category cleaned")
        except:
            print("un problème est survenur lors du nettoyage de product_category")
            print("Erreur :", sys.exc_info()[0])

    def clean_product_store(self):
        try:    
            self.db.query("DELETE FROM product_store\
                WHERE PS_PROD_id NOT IN \
                SELECT SAU_PROD_id FROM save);")
            print("product_store cleaned")
        except:
            print("un problème est survenur lors du nettoyage de product_store")
            print("Erreur :", sys.exc_info()[0])

    def clean_product(self):
        try:    
            self.db.query("DELETE FROM product\
                WHERE PROD_id NOT IN (SELECT SAU_PROD_id FROM save);")
            print("product cleaned")
        except:
            print("un problème est survenur lors du nettoyage de product")
            print("Erreur :", sys.exc_info()[0])

    def save(self, id):
        """ Gets a PROD_id and add it to the save table """
        try:
            self.db.query("INSERT INTO save VALUES (:id)", id=id)
        except:
            prod_name = self.db.query(
                "SELECT PROD_name FROM product WHERE PROD_id = :id", id=id)
            print("{} est déjà dans la base".format(prod_name.export('json')))

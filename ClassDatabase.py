#! /usr/bin/env python3
# coding: utf-8
import records
import sys
import json

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
        self.db.query(
            'CREATE DATABASE IF NOT EXISTS pur_beurre CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')

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
                SELECT SAU_PROD_id FROM save)")
            print("product_category cleaned")
        except:
            print("un problème est survenur lors du nettoyage de product_category")
            print("Erreur :", sys.exc_info()[0])

    def clean_product_store(self):
        try:
            self.db.query("DELETE FROM product_store\
                WHERE PS_PROD_id NOT IN \
                (SELECT SAU_PROD_id FROM save)")
            print("product_store cleaned")
        except:
            print("un problème est survenur lors du nettoyage de product_store")
            print("Erreur :", sys.exc_info()[0])

    def clean_product(self):
        try:
            self.db.query("DELETE FROM product\
                WHERE PROD_id NOT IN (SELECT SAU_PROD_id FROM save)")
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

    def get_grade_e_products(self, category):
        """ Takes a category and return 10 random products of this category with a nutrition grade E """
        rows = self.db.query("SELECT product.PROD_name, product.PROD_descr, product.PROD_id\
            FROM product\
            INNER JOIN product_category\
            ON product.PROD_id = product_category.PC_PROD_id\
            INNER JOIN category\
            ON product_category.PC_CAT_id = category.CAT_id\
            WHERE CAT_nom = :category AND PROD_grade = 'e'\
            ORDER BY RAND()\
            LIMIT 10;", category=category)

        return json.loads(rows.export('json'))
    
    def get_grade_a_products_id(self, category):
        """ returns all the garde A products from the given category """
        rows = self.db.query("SELECT product.PROD_id\
            FROM product\
            INNER JOIN product_category\
            ON product.PROD_id = product_category.PC_PROD_id\
            INNER JOIN category\
            ON product_category.PC_CAT_id = category.CAT_id\
            WHERE CAT_nom = :category AND PROD_grade = 'a'",
            category=category)
        return json.loads(rows.export('json'))

    def get_product_categories_id(self, product_id):
        """ Returns a list of categories of a product """
        rows = self.db.query("SELECT PC_CAT_id FROM product_category\
            WHERE PC_PROD_id = :prod_id",
            prod_id=product_id)
        return json.loads(rows.export('json'))

    def get_prod_id_by_name(self, name):
        """gets the name of a product, return the id"""
        rows = self.db.query("SELECT PROD_id FROM product\
            WHERE PROD_name = :name",
            name=name)
        return json.loads(rows.export('json'))

    def get_best_match(self, prod_id, cat_name):
        pass
        # Je crée une liste PROD_id
        # Le PROD_id 0 est celui sélectionné par l'utilisateur
        # Les PROD suivants sont les grade A de la même CAT
        # 
        # Je crée une liste_set
        # Chaque set() est la liste des CAT_id des PROD de la liste
        # Je compare les sets avec liste_set[0] ( set(a) & set(b) )
        # J'enregistre les index des PROD avec le nb d'occurences max
        # S'il y a plusieurs set pertinents j'en revoie un au hasard

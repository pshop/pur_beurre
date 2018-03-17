#! /usr/bin/env python3
# coding: utf-8

import records

class DatabaseUpdator():
    """ Has a method to update every table of the Base """
    def __init__(self, data, db_connection):
        self.data = data
        self.db = db_connection
        self.db.query('USE pur_beurre')

    def table_store_update(self):
        """ Inserts unique stores name in table store """
        for product in self.data:
            for store_tag in product['stores_tags']:
                try:
                    self.db.query('INSERT INTO store (MAG_nom) VALUES (:store)', store = store_tag.lower())
                except:
                    pass

    def table_product_update(self):
        """ Inserts products in product table """
        for product in self.data:
            try:
                self.db.query('INSERT INTO product (PROD_id, PROD_name, PROD_descr, PROD_grade, PROD_url)\
                    VALUES(:id, :name, :descr, :grade, :link)',
                    id = product['id'],
                    name = product['product_name'],
                    descr = product['generic_name'],
                    grade = product['nutrition_grades'],
                    link = product['url'],
                    )
            except:
                pass
    
    def table_category_update(self):
        """ Inserts categories in category table """
        for product in self.data: 
            categories_list = product['categories'].split(',')
            for categorie in categories_list:
                categorie = self.__clean_string(categorie)
                try:
                    self.db.query("INSERT INTO category (CAT_nom) VALUES (:cat)", cat = categorie)
                except:
                    pass

    def table_product_category_update(self):
        """ Inserts product / category links in product category table """
        for product in self.data: 
            categories_list = product['categories'].split(',')
            for categorie in categories_list:
                categorie = self.__clean_string(categorie)
                try:
                    self.db.query("INSERT INTO product_category (PC_PROD_id, PC_CAT_id)\
                        VALUES (:id,\
                        (SELECT CAT_id FROM category\
                        WHERE CAT_nom = :cat))", id = product['id'], cat = categorie )
                except:
                    pass

    def table_product_store_update(self):
        """ Inserts all the occurences of stores i got with the products """
        for product in self.data:
            for store in product['stores_tags']:
                try:
                    self.db.query("INSERT INTO product_store (PS_PROD_id, PS_MAG_id)\
                    VALUES (:id,\
                    (SELECT MAG_id FROM store\
                    WHERE MAG_nom = :store))", id = product['id'], store = store )
                except:
                    pass

    def __clean_string(self, str_to_clean):
        """ cleans the strings from the API by deleting things like country id """
        if str_to_clean[:1] == " ":
            str_to_clean = str_to_clean[1:]
        if str_to_clean[2] == ':':
            str_to_clean = str_to_clean[3:]
        return str_to_clean.lower()

#! /usr/bin/env python3
# coding: utf-8

import records

class UpdateDatabase():

    def __init__(self, data):
        self.data = data
        self.db = records.Database('mysql+pymysql://root:kcokopv6@localhost')
        self.db.query('USE pur_beurre')

    def table_store_update(self):
        for product in self.data:
            for store_tag in product['stores_tags']:
                try:
                    self.db.query('INSERT INTO store (MAG_nom) VALUES (:store)', store = store_tag)
                except:
                    pass

    def table_product_update(self):
        #self.db.query('TRUNCATE TABLE product')
        for product in self.data:
            self.db.query('INSERT INTO product (PROD_id, PROD_name, PROD_descr, PROD_grade, PROD_url, PROD_MAG_id)\
                VALUES(:id, :name, :descr, :grade, :link,\
                (SELECT MAG_id FROM store WHERE MAG_nom = :store))',
                id = product['id'],
                name = product['product_name'],
                descr = product['generic_name'],
                grade = product['nutrition_grades'],
                link = product['url'],
                # A modifier plus tard et faire une table product_store
                store = product['stores_tags'][0]
                )
    
    def table_category_update(self):
        for product in self.data: 
            categories_list = product['categories'].split(',')
            for categorie in categories_list:
                categorie = self.__clean_string(categorie)
                try:
                    self.db.query("INSERT INTO category (CAT_nom) VALUES (:cat)", cat = categorie)
                except:
                    pass

    def table_product_category_update(self):
        #self.db.query('TRUNCATE TABLE product_category')
        for product in self.data: 
            categories_list = product['categories'].split(',')
            for categorie in categories_list:
                categorie = self.__clean_string(categorie)
                self.db.query("INSERT INTO product_category (PC_PROD_id, PC_CAT_id)\
                    VALUES (:id,\
                    (SELECT CAT_id FROM category\
                    WHERE CAT_nom = :cat))", id = product['id'], cat = categorie )

    def __clean_string(self, str_to_clean):
        if str_to_clean[:1] == " ":
            str_to_clean = str_to_clean[1:]
        if str_to_clean[2] == ':':
            str_to_clean = str_to_clean[3:]
        return str_to_clean.lower()

#! /usr/bin/env python3
# coding: utf-8

import records
# CREATE DATABASE off CHARSET utf8mb4 COLLATE utf8mb4_unicode_ci

class UpdateDatabase :

    def __init__(self, data, table_name):
        self.data = data
        self.table_name = table_name
        self.db = records.Database('mysql+pymysql://root:kcokopv6@localhost/base_off?utf8md4')
    
    def table_product(self):
        self.db.query('DROP TABLE IF EXISTS product')
        self.db.query('CREATE TABLE IF NOT EXISTS product (PROD_id int PRIMARY KEY, PROD_name varchar(100), PROD_descr varchar(100), PROD_grade char(1)), PROD_link varchar(150), PROD_MAG_id int')

    def table_update(self):
        for product in self.data:
            self.db.query('INSERT INTO product (PROD_id, PROD_name, PROD_descr, PROD_grade, PROD_link, PROD_MAG_id) VALUES(:id, :name, :descr, :grade, :link, :mag_id)',\
                id = product['id'],\
                name = product['product_name'],\
                descr = product['generic_name'],\
                grade = product['nutrition_grades'],\
                link = product['url'],\
                mag_id = 0
                )    
        
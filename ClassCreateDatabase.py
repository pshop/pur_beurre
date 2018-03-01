#! /usr/bin/env python3
# coding: utf-8

import records

class CreateDatabase :

    def __init__(self):
        self.db = records.Database('mysql+pymysql://root:kcokopv6@localhost')
    
    def table_product_create(self):
        self.db.query('DROP TABLE IF EXISTS product')
        self.db.query('CREATE TABLE product(\
            PROD_id BIGINT PRIMARY KEY,\
            PROD_name VARCHAR(100) NOT NULL UNIQUE,\
            PROD_descr VARCHAR(150) NOT NULL,\
            PROD_grade CHAR(1) NOT NULL,\
            PROD_url VARCHAR(150) NOT NULL UNIQUE,\
            PROD_MAG_id int NOT NULL)')
        self.db.query('CREATE UNIQUE INDEX UI_PROD_name ON product(PROD_name)')
        self.db.query('ALTER TABLE product\
            ADD CONSTRAINT FK_PROD_MAG_id\
            FOREIGN KEY (PROD_MAG_id) REFERENCES store(MAG_id)')
    
    def table_category_create(self):
        self.db.query('DROP TABLE IF EXISTS category')
        self.db.query('CREATE TABLE category(\
            CAT_id int PRIMARY KEY AUTO_INCREMENT,\
            CAT_nom VARCHAR(50) UNIQUE)')

    def table_product_category_create(self):
        self.db.query('DROP TABLE IF EXISTS product_category')
        self.db.query('CREATE TABLE product_category(\
            PC_PROD_id BIGINT NOT NULL,\
            PC_CAT_id int NOT NULL)')
        self.db.query('ALTER TABLE product_category ADD CONSTRAINT PK_product_category PRIMARY KEY (PC_PROD_id, PC_CAT_id)')
        self.db.query('ALTER TABLE product_category\
            ADD CONSTRAINT FK_PC_PROD_id\
            FOREIGN KEY (PC_PROD_id) REFERENCES product(PROD_id);')
        self.db.query('ALTER TABLE product_category\
            ADD CONSTRAINT FK_PC_CAT_id\
            FOREIGN KEY (PC_CAT_id) REFERENCES category(CAT_id);')
    
    def table_store_create(self):
        self.db.query('DROP TABLE IF EXISTS store')
        self.db.query('CREATE TABLE store(\
            MAG_id int PRIMARY KEY AUTO_INCREMENT,\
            MAG_nom VARCHAR(50) UNIQUE)')

    def table_save_create(self):
        self.db.query('DROP TABLE IF EXISTS save')
        self.db.query('CREATE TABLE save(\
            SAU_PROD_id BIGINT PRIMARY KEY)')
        self.db.query('ALTER TABLE save\
            ADD CONSTRAINT FK_SAU_PROD_id\
            FOREIGN KEY (SAU_PROD_id) REFERENCES product(PROD_id)')

    def initiate_db(self):
        self.db.query('DROP DATABASE if EXISTS pur_beurre')
        self.db.query('CREATE DATABASE pur_beurre')
        self.db.query('USE pur_beurre')
        self.table_store_create()
        self.table_product_create()
        self.table_category_create()
        self.table_product_category_create()
        self.table_save_create()
        
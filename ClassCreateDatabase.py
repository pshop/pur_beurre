#! /usr/bin/env python3
# coding: utf-8

import records

class CreateDatabase :

    def __init__(self):
        self.db = records.Database('mysql+pymysql://root:kcokopv6@localhost')

    def table_product_create(self):
        self.db.query('CREATE TABLE IF NOT EXISTS product(\
            PROD_id BIGINT PRIMARY KEY,\
            PROD_name VARCHAR(100) NOT NULL,\
            PROD_descr VARCHAR(150) NOT NULL,\
            PROD_grade CHAR(1) NOT NULL,\
            PROD_url VARCHAR(150) NOT NULL UNIQUE,\
            PROD_MAG_id int NOT NULL)')
            self.db.query('CREATE UNIQUE INDEX UI_PROD_name ON product(PROD_name)')
            self.db.query('ALTER TABLE product\
                ADD CONSTRAINT FK_PROD_MAG_id\
                FOREIGN KEY (PROD_MAG_id) REFERENCES store(MAG_id) ON DELETE CASCADE')
    
    def table_category_create(self):
        self.db.query('CREATE TABLE IF NOT EXISTS category(\
            CAT_id int PRIMARY KEY AUTO_INCREMENT,\
            CAT_nom VARCHAR(50) UNIQUE)')

    def table_product_category_create(self):
        self.db.query('CREATE TABLE IF NOT EXISTS product_category(\
            PC_PROD_id BIGINT NOT NULL,\
            PC_CAT_id int NOT NULL)')
            self.db.query('ALTER TABLE product_category ADD CONSTRAINT PK_product_category PRIMARY KEY (PC_PROD_id, PC_CAT_id)')
            self.db.query('ALTER TABLE product_category\
                ADD CONSTRAINT FK_PC_PROD_id\
                FOREIGN KEY (PC_PROD_id) REFERENCES product(PROD_id) ON DELETE CASCADE')
            self.db.query('ALTER TABLE product_category\
                ADD CONSTRAINT FK_PC_CAT_id\
                FOREIGN KEY (PC_CAT_id) REFERENCES category(CAT_id) ON DELETE CASCADE')
    
    def table_product_store_create(self):
        self.db.query('CREATE TABLE IF NOT EXISTS product_store(\
            PS_PROD_id BIGINT,\
            PS_MAG_id INT)')
            self.db.query('ALTER TABLE product_store\
                ADD CONSTRAINT PK_product_store\
                PRIMARY KEY (PS_PROD_id, PS_MAG_id)')
            self.db.query('ALTER TABLE product_store\
                ADD CONSTRAINT FK_PS_PROD_id\
                FOREIGN KEY (PS_PROD_id) REFERENCES product(PROD_id)')
            self.db.query('ALTER TABLE product_store\
                ADD CONSTRAINT FK_PS_MAG_id\
                FOREIGN KEY (PS_MAG_id) REFERENCES store(MAG_id)')

    def table_store_create(self):
        self.db.query('CREATE TABLE IF NOT EXISTS store(\
            MAG_id int PRIMARY KEY AUTO_INCREMENT,\
            MAG_nom VARCHAR(50) UNIQUE)')

    def table_save_create(self):
        self.db.query('CREATE TABLE IF NOT EXISTS save(\
            SAU_PROD_id BIGINT PRIMARY KEY)')
        self.db.query('ALTER TABLE save\
            ADD CONSTRAINT FK_SAU_PROD_id\
            FOREIGN KEY (SAU_PROD_id) REFERENCES product(PROD_id) ON DELETE CASCADE')



    def initiate_db(self):
        self.db.query('CREATE DATABASE IF NOT EXISTS pur_beurre')
        self.db.query('USE pur_beurre')
        self.table_store_create()
        self.table_product_create()
        self.table_category_create()
        self.table_product_category_create()
        self.table_save_create()
        self.table_product_store_create()
        


        
        
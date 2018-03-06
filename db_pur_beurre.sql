-- GRANT ALL PRIVILEGES ON pur_beurre.* TO 'sdz'@'localhost' IDENTIFIED BY 'kcokopv6';

CREATE DATABASE IF NOT EXISTS pur_beurre CHARACTER SET 'utf8';

USE pur_beurre;

CREATE TABLE produit(
    PROD_id int PRIMARY KEY,
    PROD_name VARCHAR(100) NOT NULL,
    PROD_descr VARCHAR(150) NOT NULL,
    PROD_garde CHAR(1) NOT NULL,
    PROD_url VARCHAR(150) UNIQUE,
    PROD_MAG_id int NOT NULL
);

CREATE TABLE categorie(
    CAT_id int PRIMARY KEY AUTO_INCREMENT,
    CAT_nom VARCHAR(50) UNIQUE
);

CREATE TABLE produit_categorie(
    PC_PROD_id int,
    PC_CAT_id int,
    PRIMARY KEY (PC_PROD_id, PC_CAT_id)
);

CREATE TABLE magasin(
    MAG_id int PRIMARY KEY AUTO_INCREMENT,
    MAG_nom VARCHAR(50) UNIQUE
);

CREATE TABLE sauvegarde(
    SAU_PROD_id int PRIMARY KEY
);

-- Je crée un index unique sur le nom du produit
CREATE UNIQUE INDEX UI_PROD_name ON produit(PROD_name);

-- Je crée la cle etrangere de produit magasin
ALTER TABLE produit
ADD CONSTRAINT FK_PROD_MAG_id
FOREIGN KEY (PROD_MAG_id) REFERENCES magasin(MAG_id);

-- Je crée les clés etrangères de produit_categorie
ALTER TABLE produit_categorie
ADD CONSTRAINT FK_PC_PROD_id
FOREIGN KEY (PC_PROD_id) REFERENCES produit(PROD_id);

-- LA deuxièmne clé étrangère:
ALTER TABLE produit_categorie
ADD CONSTRAINT FK_PC_CAT_id
FOREIGN KEY (PC_CAT_id) REFERENCES categorie(CAT_id);

-- La clé étrangère de sauvegarde:
ALTER TABLE sauvegarde
ADD CONSTRAINT FK_SAU_PROD_id
FOREIGN KEY (SAU_PROD_id) REFERENCES produit(PROD_id)

-- Récupérer tous les noms de produits ayant boisson pour catégorie
SELECT product.PROD_name
FROM product
INNER JOIN product_category
    ON product.PROD_id = product_category.PC_PROD_id
INNER JOIN category
    ON product_category.PC_CAT_id = category.CAT_id
WHERE CAT_nom = 'boissons'

-- Récupérer toutes les catégories d'un produit
SELECT category.CAT_nom
FROM category
INNER JOIN product_category 
    ON category.CAT_id = product_category.PC_CAT_id
INNER JOIN product
    ON product_category.PC_PROD_id = product.PROD_id
WHERE PROD_id = 3045320517101

-- sélectionner 10 produits au hasard
SELECT PROD_id
FROM product
ORDER BY RAND()
LIMIT 10;

-- Ajouter 10 produits au hasard dans la table save
INSERT INTO save (SAU_PROD_id)
SELECT PROD_id
FROM product
ORDER BY RAND()
LIMIT 10;
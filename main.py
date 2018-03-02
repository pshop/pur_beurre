#! /usr/bin/env python3
# coding: utf-8
from ClassImportFromAPI import ImportFromApi
from ClassExtractJson import ExtractFromJson
from ClassUpdateDatabase import UpdateDatabase

    # I set my search parameters : nutrition grade and categories
api_import = ImportFromApi("e", "produit-laitier")
    # I get the informations i need for every products in order to put it in the database
to_extract = ExtractFromJson(api_import.get_json())
    # It all goes in a list of dictionaries, one dictionary per product
liste_de_produits = to_extract.extract_json()

database = UpdateDatabase(liste_de_produits)
    # Je crée la base si elle n'existe pas ainsi que toutes ses tables.
database.initiate_db()
    # Je rempli les tables
database.table_store_update()
    # PROBLEME de contrainte d'unicité
    # Pourtant j'essaie de vider toutes les tables avec un TRUNCATE TABLE avant de les mettre à jour
    # ET POUQUOI TRUNCATE TABLE ne fonctionne pas?
database.table_product_update()
database.table_category_update()
database.table_product_category_update()

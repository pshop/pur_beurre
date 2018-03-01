#! /usr/bin/env python3
# coding: utf-8
from ClassImportFromAPI import ImportFromApi
from ClassExtractJson import ExtractFromJson
from ClassDatabase import UpdateDatabase

# I set my search parameters : nutrition grade and categories
api_import = ImportFromApi("e", "produit-laitier")
# I get the informations i need for every products in order to put it in the database
to_extract = ExtractFromJson(api_import.get_json())
# It all goes in a list of dictionaries, one dictionary per product
liste_de_produits = to_extract.extract_json()

create_table = UpdateDatabase(liste_de_produits, "produit")
create_table.table_product()
create_table.table_update()


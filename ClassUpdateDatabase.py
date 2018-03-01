from ClassCreateDatabase import CreateDatabase
import requests

class UpdateDatabase(CreateDatabase):

    def __init__(self, *data):
        CreateDatabase.__init__(self)
        self.db.query('USE pur_beurre')

        if data:
            self.data = data[0]

    def table_store_update(self):
        """ cleans the table and update the stores """
        stores = []
        for product in self.data:
            for store_tag in product['stores_tags']:
                if store_tag not in stores:
                    self.db.query('INSERT INTO store (MAG_nom) VALUES (:store)', store = store_tag)
                    stores.append(store_tag)

    def table_product_update(self):
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
        categories = []
        for product in self.data:
            for cat_tag in product['categories']:
                if cat_tag not in categories:
                    self.db.query("INSERT INTO category (CAT_nom) VALUES (:cat)", cat = cat_tag)
                    categories.append(cat_tag)

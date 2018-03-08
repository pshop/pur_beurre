#! /usr/bin/env python3
# coding: utf-8

import sys
import os
import json
from ClassDatabase import Database


class AppPurBeurre:

    def __init__(self, arg):

        try:
            self.arg = arg[1]
        except:
            self.arg = None

        # I get the config file with categories and login info for the database
        with open("../config/config.json") as f:
            self.config = json.load(f)

        # New instance of the databse
        self.pur_beurre = Database(
            self.config["user"], self.config["password"], self.config["server"])

        # If i can connect to the database it means it has been created and filled previously
        try:
            self.pur_beurre.connect()
            print("Cnnexion réussie")
        # If it doesn't connect then i create the database
        except:
            print("la base n'existe pas")
            # Creates the database
            self.pur_beurre.create_base()
            # Creates the tables
            self.pur_beurre.create_tables()
            # Connects to the database and use it
            self.pur_beurre.connect()
            # Fill the all database
            for category in self.config["categories"]:
                self.pur_beurre.fill_in('a', category)
                self.pur_beurre.fill_in('e', category)

        # In case of update
        try:
            if self.arg == '-update':
                print("mise à jour")
                self.pur_beurre.clean_product_category()
                self.pur_beurre.clean_product_store()
                self.pur_beurre.clean_product()
                for category in self.config["categories"]:
                    self.pur_beurre.fill_in('a', category)
                    self.pur_beurre.fill_in('e', category)
        except:
            pass

    def show_category_menu(self):
        """ Shows to the user the available categories an get his choice """
        cat_num = 0
        user_input = None

        os.system('cls' if os.name == 'nt' else 'clear')

        print("Bienvenu sur l'app de Pur Beurre")
        print("Entrez un chiffre correspondant à la catégorie que vous souhaitez explorer")
        for category in self.config["categories"]:
            print("Pour la catégorie {} tapez {}".format(category, cat_num))
            cat_num += 1
        user_input = input(">")

        try:
            if int(user_input) >= 0 and int(user_input) <= cat_num:
                return int(user_input)
            else:
                self.show_category_menu()
        except:
            self.show_category_menu()

    def show_category_products(self, usr_input_category):
        """ Shows to user 10 grade E products of the given category """
        category = self.config["categories"][usr_input_category]
        prod_nb = 0
        user_input_product = None

        request_json = self.pur_beurre.get_grade_e_products(category)
        os.system('cls' if os.name == 'nt' else 'clear')

        print("Veuillez sélectionner un produit de la catégorie {}".format(category))
        print("Entrez le numéro associé et trouvez un aliement de substitution plus saint:")

        for product in request_json:
            print("{num} : {prod_name}".format(
                num=prod_nb, prod_name=product["PROD_name"]))
            print("    {descr}\n".format(descr=product["PROD_descr"]))
            prod_nb += 1

        user_input_product = input(">")

        try:
            if int(user_input_product) >= 0 and int(user_input_product) <= prod_nb:         
                return self.pur_beurre.get_prod_id_by_name(request_json[int(user_input_product)]["PROD_name"])
            else:
                self.show_category_products(usr_input_category)
        except:
            self.show_category_products(usr_input_category)

    def show_best_match(self, product_id, category_index):

        request_json = self.pur_beurre.get_best_match(product_id, self.config["categories"][category_index])

def main(argv):
    # Stars a new session setup the database / update it if asked
    new_session = AppPurBeurre(argv)
    # # Shows the category menu / returns the chosen category
    # category_index_input = new_session.show_category_menu()
    # # Shows grade E products from the selected category / returns the chosen product
    # product_id_input = new_session.show_category_products(category_index_input)
    # # Shows the matching grade A product
    # new_session.show_best_match(product_id_input[0]["PROD_id"], category_index_input)
    new_session.show_best_match(3551720003941, 1)

if __name__ == '__main__':
    main(sys.argv)
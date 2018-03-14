#! /usr/bin/env python3
# coding: utf-8

import sys
import os
import json
from ClassDatabase import Database


class AppPurBeurre:
    """ Manages the user interface and connection to the database """
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
        while True:
            cat_num = 0
            user_input = None

            os.system('cls' if os.name == 'nt' else 'clear')

            print("Bienvenu sur l'app de Pur Beurre")
            print("Entrez un chiffre correspondant à la catégorie que vous souhaitez explorer")
            for category in self.config["categories"]:
                print("Pour la catégorie {} tapez {}".format(category, cat_num))
                cat_num += 1
            print("Pour consulter votre liste de produits favorits tapez '5'")
            user_input = input(">")

            try :
                if int(user_input) >= 0 and int(user_input) <= cat_num:
                    return int(user_input)
            except:
                pass

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
        """ Will show the most pertinent product and all the informations about it stored in the database """

        os.system('cls' if os.name == 'nt' else 'clear')
        best_match_id = self.pur_beurre.get_best_match(product_id, self.config["categories"][category_index])

        grade_e_prod = self.pur_beurre.get_prod_by_id(product_id)
        match_prod = self.pur_beurre.get_prod_by_id(best_match_id)
        match_prod_store = self.pur_beurre.get_stores_by_prod_id(best_match_id)

        print("En replacement de \'{name}\' nous vous conseillons le produit suivant:\n".format(name = grade_e_prod[0]["PROD_name"]))
        print("{name} :\n{descr}\n".format(name = match_prod[0]["PROD_name"], descr=match_prod[0]["PROD_descr"]))
        print("Ce produit a une note nutritionelle {note}\n".format(note=match_prod[0]["PROD_grade"]))
        print("Vous pouvez vous le procurer dans les magasins suivants :")
        for mag in match_prod_store:
            print("\t{}".format(mag["MAG_nom"]))
        print("Lien vers la fiche du produit :\n{url}".format(url = match_prod[0]["PROD_url"]))

        self.show_save_product(match_prod[0]["PROD_id"])


    def show_save_product(self, product_id):
        """ Displays the list of saved products and allows the user to delete them """
        user_input = None

        print("Pour enregistrer ce produit dans vos favorits entrez 's'")
        print("pour revenir au menu appuyez sur n'importe quelle touche:")
        user_input = input(">")

        if user_input.lower() == 's':
            self.pur_beurre.save_product(product_id)
        # else:
        #     self.show_save_product(product_id)

    def show_fav(self):
        """ Prints all the fav products saved by the user
        he also can select a product an delete it """
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            user_input = None
            i = 0
            fav_prod_list = self.pur_beurre.get_fav()

            print("Pour supprimer un produit de vos favorits,")
            print("entrez le numéro correspondant au produit\n")
            for prod_id in fav_prod_list:
                prod = self.pur_beurre.get_prod_by_id(prod_id["SAU_PROD_id"])
                prod_store =  self.pur_beurre.get_stores_by_prod_id(prod_id["SAU_PROD_id"])
                print("{i} :\n{name}".format(i=i,name=prod[0]["PROD_name"]))
                print(prod[0]["PROD_descr"])
                print("{url}".format(url=prod[0]["PROD_url"]))
                print("Est vendu dans les enseignes suivantes :")
                for mag in prod_store:
                    print(mag["MAG_nom"], '')
                print()
                i+=1
            user_input = input("Entrez un numéro de produit\nou tapez sur n'importe quelle touche pour quitter >")
            try:
                if int(user_input) >=0 and int(user_input) <=i:
                    self.pur_beurre.delete_from_save(fav_prod_list[int(user_input)]["SAU_PROD_id"])
            except:
                break
        

    





def main(argv):
    # Starts a new session setup the database / update it if asked
    new_session = AppPurBeurre(argv)

    while True:
        # Shows the category menu / returns the chosen category
        # and asks the user to press f to consult his favorite products
        category_index_input = new_session.show_category_menu()
        if category_index_input == 5:
            new_session.show_fav()
        else:
        # Shows grade E products from the selected category / returns the chosen product
            product_id_input = new_session.show_category_products(category_index_input)
        # Shows the matching grade A product
            new_session.show_best_match(product_id_input[0]["PROD_id"], category_index_input)
            continue

if __name__ == '__main__':
    main(sys.argv)
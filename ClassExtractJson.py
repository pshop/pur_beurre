#! /usr/bin/env python3
# coding: utf-8

class ExtractFromJson:

    def __init__(self, json_data):
        """ For each product i'll get : id, product_name, categories, nutrition_grade, stores_tags, generic_name """
        self.keys = [
            "id",
            "product_name",
            "categories",
            "nutrition_grades",
            "stores_tags",
            "generic_name",
            "url"
            ]
        self.json_data = json_data

    def extract_json(self):
        # list of products, will be return
        products_list = []
        black_list = []
        # for each products i got
        for data in self.json_data["products"]:
            temp_dict = {}
            complete = True
            
            # I create a black list to avoid multiple entries of the same product
            # It's only based on the four first letters of the product
            if data["product_name"][:4].lower() not in black_list :
                black_list.append(data["product_name"][:4].lower())
                # I check if there's not empty fields
                for key in self.keys:
                    # If the field is not empty i add it to the dict
                    if key in data and data[key] != "" and data[key] != []:
                        temp_dict[key] = data[key]
                    # Otherwise I go to the next product
                    else:
                        complete = False
                        break
                # If the dict is full i add the product to the list
                if complete:        
                    products_list.append(temp_dict)

        return products_list

#! /usr/bin/env python3
# coding: utf-8
import json
import requests

class ImportFromApi:
    """ I give a nutrition grade and one or more categories and i get de 10 most popular products corresponding """

    def __init__(self, nutrition_grade, *category):
        """ Give the instance a grade between \'a\' and \'e\' or type 0 for no grades selection and one or more categories """

        self.nutrition_grade = nutrition_grade
        self.category = []
        for cat in category:
            self.category.append(cat)

    def get_json(self):
        """ This method generates the request,
        submits it with the library requests
        and returns a json with the returned values """

        baseurl = 'https://fr.openfoodfacts.org/cgi/search.pl'

        params = {"action" : "process"}

        i = 0
        for cat in self.category:
            params.update({
                "tagtype_{}".format(i) : "categories",
                "tag_contains_{}".format(i) : "contains",
                "tag_{}".format(i) : cat
                })
            i += 1
                
        params.update({
            "tagtype_{}".format(i) : "nutrition_grades",
            "tag_contains_{}".format(i) : "contains",
            "tag_{}".format(i) : self.nutrition_grade
            })

        params.update({"sort_by" : "unique_scans_n", "page_size" :  500, "json" : 1})

        r = requests.get(baseurl, params = params)
        return r.json()


#obj = ImportFromApi("a", "boisson", "produits-laitiers")
#print(obj.get_json())

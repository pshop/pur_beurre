# pur_beurre
Projet 5 OC

1. Make sure that python 3 and pip are properly installed on your computer.
    If you need help you should check this [Properly Installing Python](http://docs.python-guide.org/en/latest/starting/installation/)
    * Then install pipenv : `pip install --user pipenv`
    * Clone the [github repository](https://github.com/pshop/pur_beurre) on your computer
    * Then `cd pur_beurre`
    * Install the needed packages with: `pipenv install -r requirements.txt`
1. If not installed, [install mysql](https://openclassrooms.com/courses/administrez-vos-bases-de-donnees-avec-mysql/installation-de-mysql)
    * Create a new user to connect with the base : ```sql GRANT ALL PRIVILEGES ON pur_beurre.* TO 'USERNAME'@'localhost' IDENTIFIED BY 'PASSWORD'; ```
    * Modify the **config.json** file, it has to be like this:
        ```json
        {
            "categories": [
                "produits-laitiers",
                "boissons",
                "desserts",
                "plats-prepares",
                "snacks-sucres"
            ],
            "password" : "PASSWORD",
            "user": "USERNAME",
            "server": "localhost"
        }
        ```
1. Run the script with `python3 main.py`
    * If this is the fun time you run the app you might have to wait a little before the menu appears.
    It is because the database is updating for the first time.
    * It is possible to update the databse when you want by running `python3 main.py -update`
    This wont affect the products you saved and this cant be usefull if you want to change the categories from the **config.json** file
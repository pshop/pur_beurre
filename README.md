# pur_beurre
Projet 5 OC

1. Make sure that python 3 and pip are properly installed on your computer.
    * If you need help you should check this [Properly Installing Python](http://docs.python-guide.org/en/latest/starting/installation/)
1. Then install pipenv if not already installed `pip install --user pipenv`
    * If you need help : [Pipenv & Virtual Environments](http://docs.python-guide.org/en/latest/dev/virtualenvs/)
1. If not installed, [install mysql](https://openclassrooms.com/courses/administrez-vos-bases-de-donnees-avec-mysql/installation-de-mysql):
    * Connect to mysql and write : ```GRANT ALL PRIVILEGES ON pur_beurre.* TO 'USERNAME'@'localhost' IDENTIFIED BY 'PASSWORD';```

### Now you have all you need to run the script

* Clone the [github repository](https://github.com/pshop/pur_beurre) on your computer
* Then `cd pur_beurre`
* And init the pipenv `pipenv install`, note that it will install all the needed libraries and modules
* Modify the **config.json** file, it has to be like this:

    ```json
    {
        "categories": [
            "produits laitiers",
            "boissons",
            "desserts",
            "plats préparés",
            "snacks sucrés"
        ],
        "user": "USER",
        "password" : "PASSWORD",
        "server": "localhost"
    }
    ```
**Run the script** with `pipenv run python3 main.py`
* If this is the first time you run the app you might have to wait a little before the menu appears.
It is because the database is updating and making requests to Open Food Fact.
* It is possible to update the databse when you want by running `python3 main.py -update`
This wont affect the products you saved and this can be usefull if you want to change the categories from the **config.json** file
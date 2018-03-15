# pur_beurre
Projet 5 OC

1. Make sure that python 3 and pip are properly installed on your computer.
    If you need help you should check this [Properly Installing Python](http://docs.python-guide.org/en/latest/starting/installation/)
    1. Then install pipenv : `pip install --user pipenv`
    1. Clone the [github repository](https://github.com/pshop/pur_beurre) on your computer
    1. Then `cd pur_beurre``
    1. Install the needed packages with: `pipenv install -r requirements.txt`
1. If not installed, [install mysql](https://openclassrooms.com/courses/administrez-vos-bases-de-donnees-avec-mysql/installation-de-mysql)
    1. Create a new user to connect with the base : ```sql GRANT ALL PRIVILEGES ON pur_beurre.* TO '**USERNAME**'@'localhost' IDENTIFIED BY '**PASSWORD**'; ```

IMPORTANT AJOUTER UN DOSSIER config
dans le même répertoire ou est contenu le dossier pur_beurre,
créer un fichier config.json sous cette forme:
```json
{
    "categories": [
        "produits-laitiers",
        "boissons",
        "desserts",
        "plats-prepares",
        "snacks-sucres"
    ],
    "password" : "motdepasse",
    "user": "utilisateur",
    "server": "serveur"
}
```
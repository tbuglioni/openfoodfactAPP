# OPENFOODFACT APP

[![forthebadge](http://forthebadge.com/images/badges/built-with-love.svg)](http://forthebadge.com)  [![forthebadge](http://forthebadge.com/images/badges/powered-by-electricity.svg)](http://forthebadge.com)

Small app for finding food and compare quality from the API OPENFOODFACT (fr version)

### Require

- Python 3.x
- mysql-server & mysql-client
- modules from requirements.txt

## Installation and requirements.

### Install require.
- Python 3 *[Download Python](https://www.python.org/downloads/)*
- mysql-server and mysql-client version 8 *[Install MySQL](https://dev.mysql.com/doc/mysql-installation-excerpt/8.0/en/)*

### Install OPENFOODFACT APP.
Link to the GitHub repository : [OPENFOODFACT APP](https://github.com/tbuglioni/openfoodfactAPP.git)
- Fork the project : [Fork a project](https://guides.github.com/activities/forking/)
- Create a directory for the clone.<br>
- Clone : <br><br>`user@computer:~/_path_/$ git clone <repository_url>`<br><br>

### Install Python's modules.
- Install requirements in virtual env. : <br><br>`pipenv install -r requirements.txt`<br>

### Add your own configuration (database Mysql)
- create file ".env" in the root of the app
- open it with your text application
- add inside your Mysql information to manage database:

``USER_DB=root
PASSWORD_DB=yourpassword ``

- save it




## Start-up

### How it's work ?
The user is on the terminal. The terminal displays the following choices:

****************
***** MENU *****
****************
1 found product
2 get saved products
3 manage database

The user selects 1. The program asks the following questions to the user 
and the user selects the answers:
- Select the category. [Several propositions associated with a number. 
The user enters the corresponding number and presses enter]
- Select the food. [Several propositions associated with a number. 
The user enters the number corresponding to the food chosen and presses enter]
- The program offers a substitute, 
where to to buy it and a link to the Open Food Facts page 
for that food.
- The user then has the option of saving the result in the database.

## Made with

* [pycharm](https://www.jetbrains.com/fr-fr/pycharm/) - IDE python

## Versions
1.0

## Authors

* **Thomas Buglioni** [link](https://github.com/tbuglioni)

## License

his project is licensed under the ``MIT License`` - see the file [LICENSE.md](LICENSE.md) for further information


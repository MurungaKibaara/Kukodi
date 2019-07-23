# Kukodi

Kukodi is an app that allows a property owner to manage his/her rental properties with ease> A propert owner can register their properties,
houses on the properties and tenants, and tenants can recieve monthly bills & make payments through the app.

## Kukodi API Version 1

---

## What is required

    - Python3
    - Flask
    - Postman
    - Pytest
    - Git
    - Python3 pip
    - PostgreSQL database 

## How to get started

1. Clone the repo

    > `https://github.com/MurungaKibaara/Kukodi/`

2) Checkout develop branch

    > `git checkout develop`

## First install

1. python3

    > `sudo apt-get install python3`

2. install python3 pip

    > `sudo apt-get install python3-pip`

3. install vitual environment

    > `pip3 install virtualenv`

4. checkout develop branch

    > `git checkout develop`

5. create the virtual environment

    > `virtualenv venv`

6. Activate the vitualenv in the parent directory of your **"env"**

    > `source venv/bin/activate`

7. Install requirement

    > `pip install -r requirements.txt`

8. Run the app

    > `python3 run.py`
    
9. Testing 

    > `python3 -m pytest`


## Endpoints to use on postman

    | Endpoints                                        |               Functions                |
    | -------------------------------------------------| :------------------------------------: |
    | POST/api/landlord/registration                   |     create property owner account      |
    | POST/api/landlord/login                          |        login property owner            |
    | POST/api/landlord/logout                         |        logout proprty owner            |
    | POST/api/tenant/registration                     |          create tenant account         |
    | POST/api/tenant/login                            |           login tenant                 |
    | POST/api/tenant/logout                           |           logout tenant                |
    | POST/api/v1/property                             |        Add a new property              |
    | GET/api/v1/property                              |       View all properties              |
    | GET/api/v1/property/&lt;id&gt                    |       View a property by id            |
    | GET/api/v1/property/&lt;name&gt                  |       View a property by name          |
    | POST/api/v1/houses                               |      Add a new house                   |
    | GET/api/v1/houses                                |View all houses in a particular property|
    | GET/api/v1/houses/&lt;id&gt                      |            View a houses by id         |
    | GET/api/v1/houses/&lt;house_no&gt                |          View a houses by house number |
    | POST/api/v1/payments                             |      Process rent payment using mpesa  |
    | GET/api/v1/payments                              |        View all payment records        |
    | GET/api/v1/payments/&lt;id&gt                    |        View a payment record by id     |
    | POST/api/v1/bills                                |            Create bills                |
    | GET/api/v1/bills                                 |       View all existing bills          |
    | GET/api/v1/bills/&lt;id&gt                       |         View a bills by id             |
    | POST/api/v1/complaints                           |      Tenants can post complaints       |
    | GET/api/v1/complaints                            |  Property owner can view all complaints|
    | GET/api/v1/complains/&lt;id&gt                   | property owner can view one coomplaint |
    

## Authors

    Murunga Kibaara

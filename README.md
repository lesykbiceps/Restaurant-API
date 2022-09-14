![PyPI - Python Version](https://img.shields.io/pypi/pyversions/privat_exchange_rates?style=for-the-badge) 
![PyPI - Developer](https://img.shields.io/badge/Developer-LesDev-orange) [![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger) ![PyPI - License](https://img.shields.io/github/license/lesykbiceps/nbu-exchange-rates)

**Official Repo:** https://github.com/lesykbiceps

Welcome! I developed a program that helps employees to make a decision at the lunch place. Each restaurant will be uploading menus
using the system every day over API.
Employees will vote for the menu before leaving for lunch
So, in general, API has the following functionality:
- Authentication
- Creating restaurant(Only for admins)
- Uploading menu for restaurant (Each restaurant has its own responsible administrator)
- Creating employee(Only for admins)
- Getting current day menu
- Getting results for the current day(menu for today)

This app contains different levels of access.Here only authenticated admins can list, create, update or delete restaurants and users. 
The menu can be added by restaurant administrators
Authenticated non-admins(employees) can see menu, vote, change password etc

If you are the administrator (default (is_admin: false)), then you have access to all the functionality, including the creation of all entities, their update or removal.

## Pathes

If you are testing in Postman, the program contains the following paths:

| Path | Function |
| ------ | ------ |
| POST /auth/registration {"username": "test", "password": "testpass","email":"test", "name":"User", "is_admin":true}| Create admin and get tokens |
| POST /auth/login {"username": "test", "password": "testpass"}|Get tokens and your id|
| POST /auth/refresh Authorization: Bearer refresh-token-here|Get new access token |
| POST /auth/change-password {"email":"test", "password":"testpass", "new_password":"test"}|Change password |
| POST /auth/logout-access Authorization: Bearer access-token-here|Revoke access token |
| POST /auth/logout-refresh Authorization: Bearer refresh-token-here|Revoke refresh token |

| Path | Function |
| ------ | ------ |
| GET /restaurants| List restaurant |
| POST /restaurants{    "name":"ClodeMone","resp_username":"test"}| Create a restaurant |
| PATCH /restaurants/{id} {"name": "TheaterofEats"}| Update restaurants by id |
| DELETE /restaurants/{id}| Delete restaurants by id |


| Path | Function |
| ------ | ------ |
| GET /menus| List menu |
| GET /menus{your filter,for example:} ?sort= True | List sorted menus(as example) |
| GET /menu_today | See which menu received the most votes |
| POST /menus {    "restaurant_id":2, "resp_username":"test", "first":"borsch2", "drink":"apple juice2", "second":"turkey2", "date":"2022-09-18 14:00:00"}| Create a menu |
| DELETE /menus/{id}| Delete menu by id |

| Path | Function |
| ------ | ------ |
| GET /votes  | List votes
|POST /votes {    "menu_id":2, "employee_id":3}  | The main function of the program - voting for a certain menu, employee_id you get when login
Also admin get votes by menu id and view the history of votes

| Path | Function |
| ------ | ------ |
|GET /employees  | list employees
|POST /employees  | create an employee
|GET /employees/{id}  | get employee by id
|PATCH /employees/{id}  | update employee by id
|DELETE /employees/{id}  | delete employee by id

## Additional info(Example of usage)
To better organize the work on the project you can use postman and follow the steps below
For example:
- Open postman and perform registration to get access token(if need next time you can only refresh token )
- Create employees
- Create restaurants and create menus for them
- Employees should get their passwords and usernames
- Employees should login, check menu and vote for one of them
- Everyone from authenticated users can check what menu win in this moment
- Every 24 hours, data related to orders is cleared automatically


# Quick Install

```bash
pip install -r requirements.txt
python run.py
```

# All additional requirements to the project are observed:
- Documentation (docstring) to functions
- README
- Flake 8
- Covered with a few pytest tests
- It can be started as from the command:
    python run.py

## License
MIT
**Free Software, Hell Yeah!**



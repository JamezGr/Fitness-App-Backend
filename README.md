# Fitness-App-Backend
API Built with Python for Fitness-App-React. It is built on Flask and is used to handle all Server-Side Requests from Login and Registration of Users to Tracking Daily Workouts and Activities.

## Installation
Before Installing **Fitness-App-Backend**, virtualenv package is required to create virtual environments:
```
$ pip install virtualenv
```
**Fitness-App-Backend** can be installed with the following commands:
```
$ git clone https://github.com/JamezGr/Fitness-App-Backend.git
```
Create a virtualenv and activate it:
```
$ virtualenv fitness-app
$ source fitness-app/bin/activate
```
Install Required Packages:
```
$ pip install -r requirements.txt
```


## Run
Ensure virtualenv activated before running Fitness-App-Backend:
```
$ source fitness-app/bin/activate
```
Start API:
```
$ python app.py
```
See API Docs api/README for usage

## Test
Unit Tests are located in ./test in Project Root as test_*.py files.
To Run Individual Tests:
```
$ python login_*.py
```
To Run All Tests, go to ./scripts in Project Root.
```
$ chmod +x run_tests.sh
$ ./run_tests.sh
```


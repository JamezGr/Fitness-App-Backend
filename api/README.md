# Fitness-App-Backend - API Reference
## Create New User:
```
POST /api/users
```
### Parameters
|     Name              |      Type      |   Description   |
| --------------------- | -------------- | ----------------|
| email                 | ``` string ``` |  **Required** Email Address for User To Create. Will reject non valid email formats.          
| username              | ``` string ``` |  **Required** Username for User To Create. Must contain 3 - 30 Characters and must not contain the following characters: &=()<>+,
| password              | ``` string ``` |  **Required** Password for User To Create. Must contain 8 - 32 Characters and must contain at least 3 Character Types: Upper Case, Lower Case, Numbers and Symbols
| confirm_password      | ``` string ``` |  **Required** Confirm Password for User To Create. Must match Original Password and Password Policy (see above) 

### Input
```json
{
  "email": "test123@gmail.com",
  "username": "Test123",
  "password": "Testtest123",
  "confirm_password": "Testtest123"
}
```
### Response
```json
{
    "data": {
        "email": "test123@gmail.com",
        "username": "Test123"
    },
    "message": "Successfully Registered",
    "status": "201"
}
```

## User Login:
```
POST /api/login
```
### Parameters
|     Name              |      Type      |   Description   |
| --------------------- | -------------- | ----------------|
| username              | ``` string ``` |  **Required** Email Address for User To Login to.      
| password              | ``` string ``` |  **Required** Password for User To Login to.

### Input
```json
{
  "username": "Test123",
  "password": "Testtest123",
}
```
### Response
```json
{
    "data": {
        "auth_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE1OTkxNjY1NTEsInN1YiI6InRlc3RfYWNjb3VudCIsImV4cCI6MTU5OTE2NzQ1MX0.9920Du1VVx55Ic3JmvoFzO87HfLt1RXz7l6JlVE4VO4",
        "username": "Test123"
    },
    "message": "Successfully Logged In",
    "status": "200"
}
```
## Check Logged In Status:
```
GET /api/users
```
### Parameters
|     Name              |      Type      |   Description   |
| --------------------- | -------------- | ----------------|
| access_token          | ``` string ``` |  **Required** Access Token to Verify User Logged In      

### Input  
Authorization: 'Bearer {ACCESS_TOKEN}'
### Response
```json
{
    "logged_in_as": "TestUser"
}
```
## Create New Access Token:
```
POST /api/refresh
```
### Parameters
|     Name              |      Type      |   Description   |
| --------------------- | -------------- | ----------------|
| refresh_token         | ``` string ``` |  **Required** Refresh Token Provided on User Login     

### Input  
Authorization: 'Bearer {REFRESH_TOKEN}'
### Response
```json
{
    "access_token": {ACCESS_TOKEN}
}
```


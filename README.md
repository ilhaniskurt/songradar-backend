# SongRadar Backend

## Introduction

SongRadar is a song recommendation service that helps users discover music according to their tastes. This backend service is built using FastAPI and SQLite.

## Features

- **JWT Authorization**: Uses JSON Web Tokens (JWT) for secure authorization, included as a bearer token in the header.
- **Password Hashing**: All user passwords are securely hashed before being stored in the SQLite database.
- **Unique User Validation**: Denies the creation of users with existing usernames or emails.
- **Username Requirements**: Usernames must meet the following conditions:

  - Must be at least 6 characters long
  - Must not be more than 18 characters long
  - Must only contain alphanumeric characters (letters and numbers)
  - Must not begin with a number

- **Email Validation**: Checks for valid email format during the sign-up process.
- **Strong Password Policy**: Passwords must meet the following conditions:

  - Minimum length of 8 characters
  - At least one uppercase letter
  - At least one lowercase letter
  - At least one numeric digit
  - At least one special character
  - No whitespace allowed

## Technology Stack

- Python
- FastAPI
- SQLite
- Uvicorn

## Prerequisites

- Python 3.10+
- pip
- virtualenv

## Setup and Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/ilhaniskurt/songradar-backend.git
   ```

2. **Navigate to the project directory**

   ```bash
   cd songradar-backend
   ```

3. **Create a virtual environment**

   ```bash
   virtualenv venv
   ```

4. **Activate the virtual environment**

   On macOS and Linux:

   ```bash
   source venv/bin/activate
   ```

   On Windows:

   ```bash
   venv\\Scripts\\activate
   ```

5. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

6. **Run the application**

   ```bash
   uvicorn app.main:app --reload
   ```

## API Endpoints

### Register a new user

- **URL**: `/auth/sign_up`
- **Method**: `POST`
- **Headers**:
  ```json
  {
    "accept": "application/json",
    "Content-Type": "application/json"
  }
  ```
- **Body**:
  ```json
  {
    "username": "string",
    "email": "string",
    "password": "string"
  }
  ```
- **Response**:
  ```json
  {
    "username": "string",
    "email": "string",
    "id": 0
  }
  ```

### Sign in an user (Get auth token)

- **URL**: `/auth/sign_in`
- **Method**: `POST`
- **Headers**:
  ```json
  {
    "accept": "application/json"
  }
  ```
- **Body**:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **Response**:
  ```json
  {
    "access_token": "string",
    "token_type": "string"
  }
  ```
- **Instructions**: To use the returned access token, include it in the `Authorization` header with the `Bearer` keyword when making requests to endpoints that require authorization. For example:
  ```bash
  curl -X 'GET' \
    'http://127.0.0.1:8000/auth/me' \
    -H 'accept: application/json' \
    -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNjk4NjgyMjE0fQ.dNvWxR8BG21vAaCnHd5LNX1_NoKpcjamNB_SHf1Y1NM'
  ```

### Get the current user (Requires Bearer Token in Header)

- **URL**: `/auth/me`
- **Method**: `GET`
- **Headers**:
  ```json
  {
    "accept": "application/json"
    "Authorization": "Bearer {access_token}"
  }
  ```
- **Response**:
  ```json
  {
    "username": "string",
    "email": "string",
    "id": 1
  }
  ```

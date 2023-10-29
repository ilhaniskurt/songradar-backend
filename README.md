# SongRadar Backend

## Introduction

SongRadar is a song recommendation service that helps users discover music according to their tastes. This backend service is built using FastAPI and SQLite.

## Technology Stack

- Python
- FastAPI
- SQLite
- Uvicorn

## Prerequisites

- Python 3.8+
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

- **URL**: `/api/register`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "username": "username",
    "password": "password"
  }
  ```
- **Response**:
  ```json
  {
    "user_id": 1,
    "username": "username"
  }
  ```

### Recommend songs

- **URL**: `/api/recommend`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "user_id": 1,
    "song_ids": [1, 2, 3]
  }
  ```
- **Response**:
  ```json
  {
    "recommended_songs": [4, 5, 6]
  }
  ```

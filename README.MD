# 🔗 FastURL - URL Shortener API

A simple URL Shortener API built using **FastAPI** and **PostgreSQL**. The application allows users to shorten long URLs into unique short links and redirect users back to the original URL while tracking the number of clicks.

---

# Features

- Shorten long URLs
- Redirect to the original URL
- Stores data in PostgreSQL
- Tracks click count
- Automatic duplicate URL detection
- Interactive API documentation using Swagger UI

---

# Technologies Used

- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- Uvicorn

---

# Project Structure

```
URL-SHORTENER/
│
├── app.py              # Main FastAPI application
├── db.py               # Database configuration
├── models.py           # SQLAlchemy models
├── index.html          # Frontend UI
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
```

---

# How It Works

## 1. Shorten URL

The client sends a POST request containing a long URL.

Example Request

```
POST /shorten
```

```json
{
    "url":"https://www.google.com"
}
```

The application:

- Validates the URL
- Checks whether it already exists
- Generates a unique 8-character short code
- Saves it into PostgreSQL
- Returns the shortened URL

Example Response

```json
{
    "message":"URL shortened successfully.",
    "original_url":"https://www.google.com",
    "short_code":"Ab12Xyz9",
    "short_url":"http://127.0.0.1:8000/Ab12Xyz9"
}
```

---

## 2. Redirect

When a user visits

```
GET /Ab12Xyz9
```

the application:

- Searches the database
- Finds the original URL
- Increments the click counter
- Redirects the user to the original website

---

## 3. Statistics

The API also provides a statistics endpoint.

```
GET /stats/{short_code}
```

Example Response

```json
{
    "original_url":"https://www.google.com",
    "short_code":"Ab12Xyz9",
    "short_url":"http://127.0.0.1:8000/Ab12Xyz9",
    "clicks":5
}
```

---

# Database

Table Name

```
urls
```

Columns

| Column | Description |
|---------|-------------|
| id | Primary Key |
| original_url | Original long URL |
| short_code | Generated unique short code |
| clicks | Number of redirects |

---

# API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | / | Home Page |
| POST | /shorten | Create Short URL |
| GET | /{short_code} | Redirect to Original URL |
| GET | /stats/{short_code} | URL Statistics |
| GET | /health | Health Check |

---

# Installation

## Clone the repository

```bash
git clone https://github.com/rakshitbagait/URL_SHORTNER
```

or download the project as ZIP.

---

## Create Virtual Environment

Windows

```bash
python -m venv venv
```

Activate

```bash
venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## PostgreSQL Setup

1. Install PostgreSQL.
2. Create a database.

Example

```sql
CREATE DATABASE url_shortener_db;
```

3. Update the database credentials inside **db.py**.

Example

```python
DATABASE_URL = "postgresql://postgres:password@localhost/url_shortener_db"
```

---

## Run the Project

```bash
uvicorn app:app --reload
```

The API will start on

```
http://127.0.0.1:8000
```

Swagger Documentation

```
http://127.0.0.1:8000/docs
```

ReDoc

```
http://127.0.0.1:8000/redoc
```

---

# Example Workflow

1. Open Swagger UI.
2. Call **POST /shorten**.
3. Enter a long URL.
4. Receive a short URL.
5. Open the short URL.
6. The application redirects to the original URL.
7. Call **GET /stats/{short_code}** to view click statistics.

---

# Future Improvements

- User Authentication
- URL Expiration
- Custom Short Codes
- QR Code Generation
- Analytics Dashboard
- Docker Support
- Rate Limiting

---

# Author

Rakshit Bagait

Built as part of the internship assessment using FastAPI and PostgreSQL.
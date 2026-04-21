# 🎮 Game Space

Game Space is a web application for managing video games and user reviews.

Users can:

- Add, edit, and delete games  
- Add, edit, and delete reviews for games  
- Add, edit, and delete genres  
- Add, edit, and delete platforms  
- Rate games  
- View game details with platforms and genres  
- Safely delete games and reviews with confirmation  

---

## 👤 User Roles & Permissions

The application defines two user groups:

### User
- Can register and log in  
- Can create and manage their own reviews  
- Can view games, genres, and platforms  
- Can edit their own profile  

### Moderator
- All User permissions  
- Can edit and delete any user’s reviews  
- Can moderate content across the platform  

---

## ⚙️ Technologies Used

- Backend: Django 6  
- Database: PostgreSQL  
- Frontend: HTML, CSS, Bootstrap 5  
- Templates: Django Template Language (DTL)  
- Asynchronous Tasks: Celery + Redis  
- API: Django REST Framework (DRF)  

---

## 🚀 Features

### 🎮 Games Management

Users can:

- Create games with:
  - Name  
  - Description  
  - Release date  
  - Platforms (multi-select)  
  - Genres (multi-select)  

- Edit games  
- Delete games with a confirmation page  
- View full game details  

---

### ⭐ Reviews System

Users can:

- Add reviews to games  
- Reviews include:
  - Author  
  - Rating (1–5)  
  - Review text  

- Edit reviews  
- Delete reviews with a confirmation page  

---

### 🎮 Platforms System

Users can:

- Add platforms  
- Platforms include:
  - Name  
  - Image URL (optional)  

- Edit platforms  
- Delete platforms with a confirmation page  

---

### 🧩 Genres System

Users can:

- Add genres  
- Genres include:
  - Name  

- Edit genres  
- Delete genres with a confirmation page  

---

## 🔌 REST API

The application includes RESTful API endpoints:

- `/api/games/` → list of games  
- `/api/games/<id>/` → game details  
- `/api/reviews/` → reviews list  

Implemented using Django REST Framework with serializers and permissions.

---

## ⚡ Asynchronous Processing

Celery with Redis is used for background task processing.

### Features:
- Sends email notifications when a review is added to a game  
- Runs tasks asynchronously without blocking the main application  

---

## 🛡 Safe Deletion

- Dedicated delete pages for games  
- Disabled form fields for preview before deletion  
- Confirmation before permanent deletion  
- Review deletion requires confirmation  

---

## 📦 Project Setup

### Clone the Repository

git clone <repository-url>  
cd GameSpace  

---

### Create a Virtual Environment

python -m venv venv  

Activate it:

Windows:
venv\Scripts\activate  

Mac / Linux:
source venv/bin/activate  

---

### Install Dependencies

pip install -r requirements.txt  

---

## 🗄 Database Setup (PostgreSQL Required)

This project requires PostgreSQL.

If PostgreSQL is not installed, download and install it first.

---

### 1. Create a Database

Open PostgreSQL terminal or pgAdmin and create the database:

CREATE DATABASE game_space;

---

### 2. Create a Database User

Create a user with a password:

CREATE USER game_user WITH PASSWORD 'your_secure_password';

---

### 3. Grant Permissions

Grant the user access to the database:

GRANT ALL PRIVILEGES ON DATABASE game_space TO game_user;

\c game_space

GRANT ALL ON SCHEMA public TO game_user;
ALTER SCHEMA public OWNER TO game_user;

ALTER DATABASE game_space OWNER TO game_user;

---

### 4. Configure Environment Variables

Create a .env file in the project root (same level as manage.py):

DB_NAME=game_space  
DB_USER=game_user  
DB_PASSWORD=your_secure_password  
DB_HOST=localhost  
DB_PORT=5432  

IMPORTANT: Do NOT commit this file to version control.

---

### Run Database Migrations

python manage.py migrate  

---

### Create a Superuser (Optional)

python manage.py createsuperuser  

---

### Collect Static Files (Production Only)

python manage.py collectstatic  

---

### Run the Server

python manage.py runserver  

Open in browser:

http://127.0.0.1:8000/  

---

## 🔐 Environment Variables

Sensitive information such as database credentials is stored in the .env file to ensure security and production readiness.

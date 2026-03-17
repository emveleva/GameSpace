# 🎮 Game Space

Game Space is a web application for managing video games and user reviews.

Users can:

- Add, edit, and delete games  
- Add, edit, and delete reviews for games  
- Rate games  
- View game details with platforms and genres  
- Safely delete games and reviews with confirmation  

---

## Technologies Used

- Backend: Django 6  
- Database: PostgreSQL  
- Frontend: HTML, CSS, Bootstrap 5  
- Templates: Django Template Language (DTL)  

---

## Features

### Games Management

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

### Reviews System

Users can:

- Add reviews to games  
- Reviews include:
  - Author  
  - Rating (1–5)  
  - Review text  

- Edit reviews  
- Delete reviews with a confirmation modal  

---

### Safe Deletion

- Dedicated delete page for games  
- Disabled form fields for preview  
- Confirmation before permanent deletion  
- Modal confirmation for review deletion  

---

## Project Setup

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

---

### 4. Configure Environment Variables

Create a .env file in the project root (same level as manage.py) and add:

DB_NAME=game_space  
DB_USER=game_user  
DB_PASSWORD=your_secure_password  
DB_HOST=localhost  
DB_PORT=5432  

❗ Do NOT commit this file to version control.

---

### Run Database Migrations

python manage.py migrate  

---

### Load Default Genres and Platforms (Optional but Recommended)

If you exported your data as fixtures:

python manage.py loaddata genres.json  
python manage.py loaddata platforms.json  

---

### Create a Superuser (Optional)

python manage.py createsuperuser  

Only required if using the Django admin panel.

---

### Collect Static Files (Required for Production)

python manage.py collectstatic  

---

### Run the Server

python manage.py runserver  

Open in browser:

http://127.0.0.1:8000/  

---

## Environment Variables

Sensitive information such as database credentials is stored inside the .env file to ensure security and production readiness.

---

## Future Improvements

- Add user authentication and permissions  
- Add pagination for games and reviews  
- Add REST API support  

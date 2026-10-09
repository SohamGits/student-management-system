# 🎓 Student Management System

A full-stack web application built with **Python** and **Django** that enables teachers and students to manage classrooms, assignments, and submissions through role-based dashboards.

Teachers can create classrooms, enroll students, publish assignments (with optional file attachments), and review submissions. Students can view their classroom, access assignments, and submit work securely.

---

## ✨ Features

### Authentication & Roles
- Student and Teacher registration with role selection
- Email-based login with role verification
- Secure password hashing via Django’s authentication system
- Classroom-key validation for teachers
- Duplicate username/email checks and password confirmation
- Protected routes and automatic redirect for unauthenticated users

### Classroom Management
- Unique classroom keys shared across multiple teachers
- Teachers can add registered students to a classroom
- Students remain unenrolled until added by a teacher
- Many-to-many relationships for flexible membership

### Teacher Dashboard
- View classroom and enrolled students
- Add students by email
- Create assignments with title, description, deadline, and optional attachment
- View and track student submissions

### Student Dashboard
- View enrolled classroom and assignment list
- See deadlines and assignment details
- Upload submissions (stored privately)
- Track submission status (including late submissions)

### Additional Capabilities
- File uploads for assignment attachments and student submissions
- Responsive Bootstrap-based UI with custom styling
- Django Admin integration for development/admin tasks
- Late submission detection and overdue assignment indicators

---

## 🛠️ Tech Stack

| Layer       | Technologies                          |
|-------------|---------------------------------------|
| Backend     | Python, Django 4.2, Django ORM        |
| Frontend    | HTML5, CSS3, Bootstrap, JavaScript, jQuery |
| Database    | SQLite (development)                  |
| Auth        | Django Authentication & Sessions      |
| Storage     | Local media + private file storage    |

---

## 🏗️ Architecture

The project follows Django’s **Model-View-Template (MVT)** pattern:

```
Browser → URLs → Views → Models (ORM) → SQLite
                ↘ Templates (HTML/CSS/JS)
```

---

## 🗄️ Data Models

```
User (Django built-in)
 └── UserProfile (OneToOne)
       ├── date_of_birth
       └── role (student | teacher)

Classroom
 ├── name
 ├── key (unique)
 ├── teachers (M2M → User)
 └── students (M2M → User)

Assignment
 ├── classroom (FK)
 ├── teacher (FK)
 ├── title, description, deadline
 ├── attachment (optional FileField)
 └── created_at

Submission
 ├── assignment (FK)
 ├── student (FK)
 ├── file (private FileField)
 ├── submitted_at
 └── Unique constraint: one submission per student per assignment
```

---

## 📁 Project Structure

```
student-management-system/
├── firstapp/                 # Main application
│   ├── migrations/
│   ├── templates/firstapp/
│   ├── forms.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── tests.py
├── mycore/                   # Project settings
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── static/                   # Global static files
├── media/                    # Public assignment attachments
├── private_media/            # Private student submissions
├── manage.py
├── db.sqlite3
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Git
- pip

### 1. Clone the repository
```bash
git clone https://github.com/SohamGits/student-management-system.git
cd student-management-system
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install django
```

### 4. Apply migrations
```bash
python manage.py migrate
```

### 5. (Optional) Create a superuser for Django Admin
```bash
python manage.py createsuperuser
```

### 6. Run the development server
```bash
python manage.py runserver
```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

---

## 🧪 Testing

Unit tests are available in `firstapp/tests.py`. Run them with:

```bash
python manage.py test firstapp
```

Key areas covered:
- Registration & login (including role and classroom-key validation)
- Classroom membership
- Assignment creation and submission constraints
- Access control for protected views

---

## 🔒 Security Notes

- Passwords are hashed using Django’s built-in password hashers
- CSRF protection is enabled on all forms
- Login-required views and role checks protect dashboards
- Student submission files are stored in a private directory outside public media
- Classroom keys are simple for development purposes and should be strengthened for production use

> **Important:** Do not commit `venv/`, `db.sqlite3`, or the real `SECRET_KEY` in production. Rotate the secret key and use environment variables before deploying.

---

## 📈 Future Improvements

- Email notifications & password reset
- Assignment grading and feedback
- Attendance tracking
- Multiple classroom support per student
- PostgreSQL / production database
- Deployment (e.g. Render, Railway, or Heroku)
- REST API endpoints
- Automated CI tests

---

## 👨‍💻 Author

**Soham Shinde**  
GitHub: [SohamGits](https://github.com/SohamGits)

---

## 📄 License

This project is open source. Feel free to use, modify, and distribute it for learning purposes.

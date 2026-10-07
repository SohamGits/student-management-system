# 🎓 Student Management System

A beginner-friendly, full-stack **Student Management System** built with **Python and Django**, designed to demonstrate practical web development skills including authentication, database relationships, CRUD operations, role-based access, frontend interaction, and Django's MVT architecture.

The system provides separate experiences for **Teachers** and **Students**, allowing teachers to manage their classroom, add students, create assignments, and track submissions, while students can access their classroom, view assignments, and submit their work.

---

## 🚀 Features

### 🔐 Authentication & Registration

- Student and Teacher registration
- Secure password handling using Django's built-in authentication system
- Email-based login
- Role-based login
- Teacher classroom-key verification
- Password confirmation during registration
- Duplicate username and email validation
- Protected dashboard routes
- Login and logout functionality
- Unauthorized users are redirected to the login page

### 🏫 Classroom Management

- Classroom creation using a unique classroom key
- Teachers can join a classroom using the classroom key
- Multiple teachers can belong to the same classroom
- Teachers can add registered students to their classroom
- Students initially remain unenrolled until added by a teacher
- Classroom membership is stored using Django database relationships

### 👨‍🏫 Teacher Dashboard

Teachers can:

- View their classroom
- View enrolled students
- Add students to their classroom
- Manage classroom members
- Create assignments
- Set assignment deadlines
- View student submissions
- Track classroom activity

### 👨‍🎓 Student Dashboard

Students can:

- View their classroom
- View classroom information
- See assignments created by their teachers
- View assignment deadlines
- Submit assignments
- Track their submission status

Students who have not yet been enrolled display:

> You're not enrolled in any classes.

### 📝 Assignment Management

Teachers can:

- Create assignments
- Add assignment descriptions
- Set deadlines
- Associate assignments with their classroom
- View submissions from students

Students can:

- View available assignments
- Read assignment details
- Check deadlines
- Submit their work
- View their submission status

### 📊 Dashboard & User Experience

- Separate Student and Teacher dashboards
- Personalized welcome messages
- Classroom-specific information
- Responsive interface
- Bootstrap-based UI components
- Custom CSS styling
- JavaScript-based frontend interactions
- jQuery used where appropriate for DOM interaction and dynamic behaviour

### 🛠️ Django Admin

The project also makes use of Django's built-in administration system for managing database records during development and administration.

---

## 🧰 Tech Stack

### Backend

- **Python**
- **Django**
- Django Authentication
- Django ORM
- Django Templates

### Frontend

- **HTML5**
- **CSS3**
- **Bootstrap**
- **JavaScript**
- **jQuery**

### Database

- **SQLite** during development
- Django ORM for database interaction
- Django migrations for database schema management

### Development Tools

- **Git**
- **GitHub**
- **GitHub Codespaces**
- Python virtual environment

---

## 🏗️ Application Architecture

The project follows Django's **Model-View-Template (MVT)** architecture.

```text
Browser
   │
   ▼
Django URLs
   │
   ▼
Views
   │
   ├──────────────► Templates
   │                  │
   │                  ▼
   │             HTML / CSS / JS
   │
   ▼
Models
   │
   ▼
Django ORM
   │
   ▼
SQLite Database
```

This structure keeps URL routing, application logic, database models, and presentation separated while allowing them to work together through Django.

---

## 🗄️ Data Model

The application uses Django's built-in `User` model for authentication and extends it through a `UserProfile`.

The main relationships include:

```text
User
 │
 └── UserProfile
       ├── Date of Birth
       └── Role
             ├── Student
             └── Teacher


Classroom
 │
 ├── Teachers
 │
 └── Students
       │
       └── Assignments
              │
              └── Submissions
```

### UserProfile

Stores additional information that isn't provided by Django's default `User` model.

Example fields:

- User
- Date of birth
- Role

### Classroom

Represents a shared classroom.

Example fields:

- Classroom name
- Unique classroom key
- Teachers
- Students

### Assignment

Represents work created by a teacher for students in a classroom.

Example fields:

- Title
- Description
- Classroom
- Teacher
- Deadline
- Created date

### Submission

Represents a student's submission for an assignment.

Example fields:

- Assignment
- Student
- Submission content/file
- Submitted date
- Status

---

## 🔑 Authentication Flow

### Registration

```text
Registration
     │
     ├── Student
     │      └── Create User + UserProfile
     │
     └── Teacher
            │
            ├── Validate classroom key
            │
            ├── Create User + UserProfile
            │
            └── Add teacher to Classroom
```

### Login

```text
Email + Password + Role
          │
          ▼
    Find Django User
          │
          ▼
    Authenticate Password
          │
          ▼
    Verify Selected Role
          │
       ┌──┴──┐
       ▼     ▼
    Teacher Student
       │     │
       ▼     ▼
 Teacher   Student
Dashboard  Dashboard
```

Passwords are handled through Django's authentication framework rather than being stored directly in plaintext.

---

## 🏫 Classroom Workflow

The classroom system uses a shared classroom key.

For example:

```text
Classroom Key: TYITF2
```

Multiple teachers can use the same key:

```text
TYITF2 Classroom
│
├── Teacher A
├── Teacher B
└── Teacher C
```

A teacher can then add registered students to the classroom:

```text
Teacher
   │
   ▼
Enter Student Email
   │
   ▼
Find Registered User
   │
   ▼
Verify Student Role
   │
   ▼
Add Student to Classroom
```

This allows multiple subject teachers to work with the same group of students.

---

## 📁 Project Structure

```text
student-management-system/
│
├── firstapp/
│   ├── migrations/
│   ├── templates/
│   │   └── firstapp/
│   │       ├── login.html
│   │       ├── register.html
│   │       ├── student_dashboard.html
│   │       └── teacher_dashboard.html
│   │
│   ├── static/
│   │   └── ...
│   │
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── mycore/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── static/
│   └── css/
│       └── style.css
│
├── db.sqlite3
├── manage.py
├── .gitignore
└── README.md
```

---

## ⚙️ Getting Started

### Prerequisites

Make sure you have:

- Python 3.x
- Git
- A code editor
- Django

### 1. Clone the repository

```bash
git clone https://github.com/SohamGits/student-management-system.git
cd student-management-system
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

On Linux/macOS:

```bash
source venv/bin/activate
```

### 3. Install Django

```bash
python -m pip install django
```

### 4. Apply database migrations

```bash
python manage.py migrate
```

### 5. Check the project

```bash
python manage.py check
```

### 6. Start the development server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

---

## 🧪 Testing

The application is tested progressively during development.

Important test cases include:

### Authentication

- Successful student registration
- Successful teacher registration
- Duplicate username validation
- Duplicate email validation
- Password mismatch validation
- Invalid teacher classroom key
- Successful student login
- Successful teacher login
- Incorrect role selection
- Invalid credentials
- Logout
- Protected dashboard access

### Classroom

- Teacher joins the correct classroom
- Multiple teachers can share the same classroom
- Student can be added to a classroom
- Student cannot be incorrectly added as a teacher
- Classroom relationships persist in the database

### Assignments

- Teacher creates an assignment
- Assignment is associated with the correct classroom
- Students can view classroom assignments
- Students can submit assignments
- Submission is associated with the correct student and assignment
- Deadline information is displayed correctly

---

## 🔒 Security Considerations

The project uses Django's built-in security and authentication mechanisms wherever appropriate.

These include:

- Django password hashing
- Django authentication sessions
- CSRF protection
- Login-protected views
- Server-side validation
- Role verification
- Database-level relationships
- Django ORM instead of manually constructed SQL queries

The classroom key used during development is intentionally simple and is **not intended to represent production-grade invitation/security infrastructure**.

---

## 📚 What This Project Demonstrates

This project was developed to build practical understanding of full-stack web development using Django.

Key concepts demonstrated include:

- Python fundamentals
- Django project structure
- Django apps
- URL routing
- Views
- Templates
- Template inheritance and template variables
- Forms and POST requests
- CSRF protection
- Django authentication
- Sessions
- Login/logout
- Protected routes
- Django models
- Model relationships
- Database migrations
- Django ORM
- CRUD operations
- HTML/CSS
- Bootstrap
- JavaScript
- DOM manipulation
- jQuery
- Form validation
- Git and GitHub
- Debugging and incremental testing

---

## 🔄 Development Approach

The application was developed incrementally rather than as one large implementation.

The general progression was:

```text
Basic Django Project
        ↓
Frontend & Templates
        ↓
Registration
        ↓
Database Models
        ↓
Authentication
        ↓
Student / Teacher Dashboards
        ↓
Classroom Relationships
        ↓
Student Management
        ↓
Assignments
        ↓
Submissions
        ↓
Testing & Polishing
        ↓
Final GitHub Project
```

Each major feature is verified before moving on to the next part of the system.

---

## 🚧 Future Improvements

Possible improvements beyond the current project scope include:

- Email notifications
- Password reset through email
- File uploads for assignments
- Assignment grading
- Student performance tracking
- Attendance management
- Multiple classroom support
- More granular teacher permissions
- Improved classroom invitation system
- Production database such as PostgreSQL
- Deployment to a cloud platform
- Automated tests
- REST API
- More advanced dashboard analytics

---

## 👨‍💻 Author

**Soham Shinde**

GitHub: [SohamGits](https://github.com/SohamGits)

Repository: [student-management-system](https://github.com/SohamGits/student-management-system)

---

## 📄 License

This project is intended primarily as a learning and portfolio project.

If a specific open-source license is added to the repository, this section should be updated accordingly.

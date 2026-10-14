<div align="center">

# Student Management System

<p align="center">A full-stack web application built with Python and Django that enables teachers and students to manage classrooms, assignments, and submissions through role-based dashboards.

Teachers can create classrooms, enroll students, publish assignments (with optional file attachments), and review submissions. Students can view their classroom, access assignments, and submit work securely.</p>

[![Stars](https://img.shields.io/github/stars/SohamGits/student-management-system?style=flat-square)](https://github.com/SohamGits/student-management-system/stargazers) [![Forks](https://img.shields.io/github/forks/SohamGits/student-management-system?style=flat-square)](https://github.com/SohamGits/student-management-system/network) [![Issues](https://img.shields.io/github/issues/SohamGits/student-management-system?style=flat-square)](https://github.com/SohamGits/student-management-system/issues) [![Watchers](https://img.shields.io/github/watchers/SohamGits/student-management-system?style=flat-square)](https://github.com/SohamGits/student-management-system/watchers) [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](https://opensource.org/licenses/MIT)

![HTML](https://img.shields.io/badge/-HTML-555?style=flat-square&logo=html) ![Python](https://img.shields.io/badge/-Python-555?style=flat-square&logo=python) ![JavaScript](https://img.shields.io/badge/-JavaScript-555?style=flat-square&logo=javascript) ![CSS](https://img.shields.io/badge/-CSS-555?style=flat-square&logo=css) ![Shell](https://img.shields.io/badge/-Shell-555?style=flat-square&logo=shell)

[🌐 View Demo](https://student-management-system-qiku.onrender.com/) · [🐛 Report Bug](https://github.com/SohamGits/student-management-system/issues) · [✨ Request Feature](https://github.com/SohamGits/student-management-system/issues)

</div>

---

## 📋 Table of Contents

- [🌐 Demo](#demo)
- [🚀 Installation](#installation)
- [💻 Usage](#usage)
- [✨ Features](#features)
- [🤝 Contributing](#contributing)
- [📄 License](#license)
- [👤 Contact](#contact)

## 🌐 Demo

[https://student-management-system-qiku.onrender.com/](https://student-management-system-qiku.onrender.com/)

## 🚀 Installation

```bash
git clone https://github.com/SohamGits/student-management-system.git
cd student-management-system

Create and activate a virtual environment:
python -m venv venv

Activate Virtual environment:
# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

Install Dependencies:
pip install django

Apply migrations:
python manage.py migrate

(Optional) Create a superuser for Django Admin:
python manage.py createsuperuser
```

## 💻 Usage

```bash
python manage.py runserver
```

## ✨ Features

- ✅ Email-based login with role verification
- ✅ Secure password hashing via Django’s authentication system
- ✅ Duplicate username/email checks and password confirmation
- ✅ Protected routes and automatic redirect for unauthenticated users


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


## 🤝 Contributing

Any contributions you make are **greatly appreciated**.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## 👤 Contact

**SohamGits**
- GitHub: [@SohamGits](https://github.com/SohamGits)
- Project: [https://github.com/SohamGits/student-management-system](https://github.com/SohamGits/student-management-system)

---

<div align="center">Made by SohamGits</div>

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=12,14,18,24&height=240&section=header&text=Student%20Management%20System&fontSize=46&fontColor=ffffff&animation=fadeIn&fontAlignY=36&desc=Classrooms%20%C2%B7%20Assignments%20%C2%B7%20Submissions&descSize=18&descAlignY=58" alt="Student Management System banner" width="100%"/>

<a href="https://github.com/SohamGits/student-management-system">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=23&duration=3000&pause=1000&color=00b7a4&center=true&vCenter=true&width=827&lines=A+full-stack+Django+web+application;Role-based+dashboards+for+teachers+%26+students;Create+classrooms+%E2%80%A2+Publish+assignments+%E2%80%A2+Review+submissions" alt="Typing animation" />
</a>

<br/>

[![Stars](https://img.shields.io/github/stars/SohamGits/student-management-system?style=for-the-badge&logo=github&color=yellow)](https://github.com/SohamGits/student-management-system/stargazers)
[![Forks](https://img.shields.io/github/forks/SohamGits/student-management-system?style=for-the-badge&logo=git&color=blue)](https://github.com/SohamGits/student-management-system/network)
[![Issues](https://img.shields.io/github/issues/SohamGits/student-management-system?style=for-the-badge&color=red)](https://github.com/SohamGits/student-management-system/issues)
[![Watchers](https://img.shields.io/github/watchers/SohamGits/student-management-system?style=for-the-badge&color=green)](https://github.com/SohamGits/student-management-system/watchers)
[![License: MIT](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)](https://opensource.org/licenses/MIT)

<br/>

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=flat-square&logo=django&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black)
![Shell](https://img.shields.io/badge/Shell-4EAA25?style=flat-square&logo=gnubash&logoColor=white)

<br/>

<a href="https://student-management-system-qiku.onrender.com/"><img src="https://img.shields.io/badge/%F0%9F%8C%90_Live_Demo-Visit_Now-success?style=for-the-badge" alt="Live Demo"/></a>
<a href="https://github.com/SohamGits/student-management-system/issues"><img src="https://img.shields.io/badge/%F0%9F%90%9B_Report-Bug-critical?style=for-the-badge" alt="Report Bug"/></a>
<a href="https://github.com/SohamGits/student-management-system/issues"><img src="https://img.shields.io/badge/%E2%9C%A8_Request-Feature-informational?style=for-the-badge" alt="Request Feature"/></a>

</div>

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%" alt="divider"/>

## 📖 About

**Student Management System** is a full-stack web application built with **Python** and **Django** that lets teachers and students manage classrooms, assignments, and submissions through **role-based dashboards**.

<table align="center">
  <tr>
    <td width="50%" valign="top">
      <h3 align="center">👩‍🏫 For Teachers</h3>
      <ul>
        <li>Create and manage classrooms</li>
        <li>Enroll students</li>
        <li>Publish assignments with optional file attachments</li>
        <li>Review student submissions</li>
      </ul>
    </td>
    <td width="50%" valign="top">
      <h3 align="center">🎓 For Students</h3>
      <ul>
        <li>View your classroom</li>
        <li>Access published assignments</li>
        <li>Submit work securely</li>
        <li>Track your submissions</li>
      </ul>
    </td>
  </tr>
</table>

## 📋 Table of Contents

| | | |
|---|---|---|
| [🌐 Demo](#-demo) | [🚀 Installation](#-installation) | [💻 Usage](#-usage) |
| [✨ Features](#-features) | [🔒 Security](#-security) | [🤝 Contributing](#-contributing) |
| [📄 License](#-license) | [👤 Contact](#-contact) | |

## 🌐 Demo

> 🔗 **Try it live:** [student-management-system-qiku.onrender.com](https://student-management-system-qiku.onrender.com/)
>
> *Hosted on Render's free tier, so the first load may take a few seconds while the server wakes up.*

<!-- Add screenshots here, for example:
<p align="center">
  <img src="docs/teacher-dashboard.png" width="48%" alt="Teacher dashboard"/>
  <img src="docs/student-dashboard.png" width="48%" alt="Student dashboard"/>
</p>
-->

## 🚀 Installation

<details open>
<summary><b>📦 Step-by-step setup</b></summary>

<br/>

**1. Clone the repository**

```bash
git clone https://github.com/SohamGits/student-management-system.git
cd student-management-system
```

**2. Create a virtual environment**

```bash
python -m venv venv
```

**3. Activate it**

```bash
# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

**4. Install dependencies**

```bash
pip install django
```

**5. Apply migrations**

```bash
python manage.py migrate
```

**6. *(Optional)* Create a superuser for Django Admin**

```bash
python manage.py createsuperuser
```

</details>

## 💻 Usage

```bash
python manage.py runserver
```

Then open **http://127.0.0.1:8000/** in your browser.

## ✨ Features

<table>
  <tr>
    <td align="center" width="25%">🔐<br/><b>Email Login</b><br/><sub>Email-based login with role verification</sub></td>
    <td align="center" width="25%">🛡️<br/><b>Secure Passwords</b><br/><sub>Hashed via Django's authentication system</sub></td>
    <td align="center" width="25%">✅<br/><b>Smart Validation</b><br/><sub>Duplicate username/email checks and password confirmation</sub></td>
    <td align="center" width="25%">🚧<br/><b>Protected Routes</b><br/><sub>Automatic redirect for unauthenticated users</sub></td>
  </tr>
  <tr>
    <td align="center" width="25%">🏫<br/><b>Classrooms</b><br/><sub>Teachers create classrooms and enroll students</sub></td>
    <td align="center" width="25%">📝<br/><b>Assignments</b><br/><sub>Publish with optional file attachments</sub></td>
    <td align="center" width="25%">📤<br/><b>Submissions</b><br/><sub>Students submit work securely</sub></td>
    <td align="center" width="25%">👥<br/><b>Role Dashboards</b><br/><sub>Separate views for teachers and students</sub></td>
  </tr>
</table>

## 🔒 Security

The project relies on Django's built-in security and authentication mechanisms wherever appropriate.

| Mechanism | Purpose |
|:---|:---|
| 🔑 **Password hashing** | Django's secure password storage |
| 🍪 **Authentication sessions** | Django session-based auth |
| 🛡️ **CSRF protection** | Guards against cross-site request forgery |
| 🚪 **Login-protected views** | Only authenticated users reach private pages |
| ✔️ **Server-side validation** | Input is verified on the backend |
| 🎭 **Role verification** | Teacher and student access is separated |
| 🔗 **Database-level relationships** | Data integrity through model relations |
| 🗄️ **Django ORM** | No manually constructed SQL queries |

## 🤝 Contributing

Any contributions you make are **greatly appreciated**!

1. 🍴 Fork the project
2. 🌿 Create your feature branch (`git checkout -b feature/amazing-feature`)
3. 💾 Commit your changes (`git commit -m 'Add some amazing feature'`)
4. 📤 Push to the branch (`git push origin feature/amazing-feature`)
5. 🔃 Open a Pull Request

## 📄 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for more information.

## 👤 Contact

<div align="center">

**SohamGits**

[![GitHub](https://img.shields.io/badge/GitHub-@SohamGits-181717?style=for-the-badge&logo=github)](https://github.com/SohamGits)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Soham_Shinde-0A66C2?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/soham-shinde-865648388/)
[![Project](https://img.shields.io/badge/Project-Repository-orange?style=for-the-badge&logo=github)](https://github.com/SohamGits/student-management-system)

<br/>

⭐ **If you found this project useful, please consider giving it a star!** ⭐

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=12,14,18,24&height=120&section=footer" width="100%" alt="footer"/>

</div>

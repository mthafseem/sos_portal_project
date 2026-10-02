# sos_portal_project
# 🎓 School Of Skills Management System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Web%20App-red)
![OOP](https://img.shields.io/badge/OOP-Architecture-green)
![Status](https://img.shields.io/badge/Status-Completed-success)

### A Modern EdTech School Management Platform Built with Python & Streamlit

Manage Students • Staff • Courses • Attendance • Fees • Notices • Analytics

</div>

---

## 📖 Overview

The **School Of Skills Management System** is a modern educational institution management platform developed using **Python, Object-Oriented Programming (OOP), and Streamlit**.

The system is designed to streamline school operations through a centralized dashboard where administrators can manage:

- 👨‍🎓 Students
- 👨‍🏫 Staff Members
- 📚 Programs & Courses
- 💰 Fee Collection
- 📅 Attendance Tracking
- 📢 Notices & Announcements
- 📊 Analytics & Reports

The project follows a clean separation of concerns:

- **sos.py** → Business Logic Layer
- **app.py** → User Interface Layer
- **Streamlit** → Interactive Web Application

---

# ✨ Features

## 👨‍🎓 Student Management

- Add, update and manage student records
- Student enrollment management
- Batch assignment
- Teacher assignment
- Student search functionality
- Soft delete and restore system
- Student profile dashboard

---

## 👨‍🏫 Staff Management

Supports multiple staff categories:

- Teacher
- Student Coordinator
- Media Team
- Accountant

Features:

- Staff registration
- Staff search
- Attendance management
- Attendance analytics
- Soft delete and recovery

---

## 📚 Program Management

Create and manage academic programs including:

- Program Name
- Category
- Duration
- Fees
- Assigned Teacher

Additional capabilities:

- Enrollment tracking
- Student count monitoring
- Program-wise statistics

---

## 💰 Fee Management System

Track student payments efficiently.

Features:

- Fee collection
- Due calculation
- Payment history
- Receipt generation
- Payment status monitoring

Statuses:

- Fully Paid
- Partially Paid
- Unpaid

---

## 📅 Attendance Management

### Student Attendance

- Mark attendance
- Attendance history
- Attendance percentage calculation
- Attendance summaries

### Staff Attendance

- Daily attendance marking
- Attendance analytics
- Attendance reports

---

## 📢 Notice Board System

Create and publish notices such as:

- General Notices
- Urgent Notices
- Event Announcements
- Examination Notifications

---

## 📊 Analytics Dashboard

Monitor institution performance using:

- Student statistics
- Staff statistics
- Program enrollment metrics
- Fee collection insights
- Attendance summaries

---

# 🏗️ System Architecture

```text
+---------------------------+
|       Streamlit UI        |
|         app.py            |
+-------------+-------------+
              |
              v
+---------------------------+
|      Business Logic       |
|         sos.py            |
+-------------+-------------+
              |
              v
+---------------------------+
|      OOP Data Models      |
+---------------------------+

SOS
├── Staff
│   ├── Teacher
│   ├── Accountant
│   ├── MediaTeam
│   └── StudentCoordinator
│
├── Program
│
├── Student
│
└── Notice
```

---

# 🧠 OOP Concepts Implemented

This project demonstrates strong Object-Oriented Programming principles:

### ✅ Inheritance

```python
Teacher(Staff)
Accountant(Staff)
MediaTeam(Staff)
StudentCoordinator(Staff)
```

### ✅ Encapsulation

Private variables:

```python
__attendance
__fees_paid
__payment_history
```

### ✅ Abstraction

```python
class SOS(ABC)
```

### ✅ Polymorphism

Multiple entities sharing common behavior through inherited methods.

---

# 🛠️ Tech Stack

| Technology | Purpose |
|------------|----------|
| Python | Core Programming |
| Streamlit | Frontend Dashboard |
| Pandas | Data Handling |
| OOP | System Architecture |

---

# 📂 Project Structure

```text
School-Of-Skills/
│
├── app.py
├── sos.py
├── requirements.txt
├── logo.png
│
└── README.md
```

---

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/school-of-skills.git

cd school-of-skills
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run Application

```bash
streamlit run app.py
```

---

# 📸 Application Modules

### Dashboard
Institution overview and statistics.

### Students
Manage student information and enrollment.

### Staff
Manage teachers and administrative staff.

### Programs
Create and monitor academic programs.

### Attendance
Track attendance records.

### Fees
Manage fee collection and pending dues.

### Notices
Publish announcements.

### Analytics
Institution-wide insights.

---

# 🎯 Learning Outcomes

This project demonstrates:

- Advanced Python Programming
- Object-Oriented Design
- Streamlit Development
- Educational ERP Concepts
- Data Management
- Dashboard Design
- Business Logic Separation
- Real-World Software Architecture

---

# 🔮 Future Enhancements

- Database Integration (MySQL/PostgreSQL)
- User Authentication
- Role-Based Access Control
- Cloud Deployment
- Student Portal
- Faculty Portal
- PDF Receipt Generation
- Email & SMS Notifications
- REST API Integration
- Mobile Application

---

# 👨‍💻 Author

**Muhammed Thafseem Ebrahim**

B.Tech Computer Science Engineering

Passionate about:
- Python Development
- Data Science
- Full Stack Development
- Educational Technology Solutions

---

# ⭐ Support

If you found this project useful:

⭐ Star the repository

🍴 Fork the repository

🛠️ Contribute to improvements

📢 Share with others

---

<div align="center">

### "Empowering Education Through Technology"

Built with ❤️ using Python & Streamlit

</div>

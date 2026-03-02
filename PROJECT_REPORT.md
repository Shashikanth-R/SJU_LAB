# Automated Electronics Laboratory Management System

## Project Report

---

## 1. Abstract

The **Automated Electronics Laboratory Management System** is a web-based application designed to streamline the management of electronics laboratory equipment, student records, and maintenance activities. This system eliminates manual record-keeping by providing digital tracking of equipment inventory, issue/return operations, and maintenance logs.

---

## 2. Introduction

### 2.1 Problem Statement

Traditional laboratory management relies on manual registers and paper-based tracking, leading to:
- Equipment loss and mismanagement
- Difficulty in tracking student borrowings
- No real-time inventory visibility
- Delayed maintenance reporting
- Inefficient reporting and analytics

### 2.2 Proposed Solution

A comprehensive web application that provides:
- **Real-time inventory tracking** of laboratory equipment
- **Digital issue/return system** for student equipment borrowing
- **Student management** with borrowing history
- **Maintenance logging** and tracking
- **Analytics and reports** for informed decision-making

---

## 3. Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend Framework** | Python Flask 3.0+ | Web server and routing |
| **Database** | MySQL 8.0 | Data storage and management |
| **Database Connector** | mysql-connector-python | Python-MySQL communication |
| **Frontend** | HTML5, CSS3, JavaScript | User interface |
| **Template Engine** | Jinja2 | Dynamic HTML rendering |
| **Icons** | Font Awesome 6.4 | UI icons |
| **Fonts** | Google Fonts (Inter) | Typography |
| **Security** | Werkzeug | Password hashing, session management |

---

## 4. System Architecture

```
┌──────────────────────────────────────────────────────────┐
│                     CLIENT (Browser)                      │
│              HTML + CSS + JavaScript                      │
└─────────────────────────┬────────────────────────────────┘
                          │ HTTP Requests
                          ▼
┌──────────────────────────────────────────────────────────┐
│                   FLASK APPLICATION                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │
│  │   Routes    │  │  Templates  │  │   Models    │       │
│  │  (app.py)   │  │  (Jinja2)   │  │  (Python)   │       │
│  └─────────────┘  └─────────────┘  └─────────────┘       │
└─────────────────────────┬────────────────────────────────┘
                          │ SQL Queries
                          ▼
┌──────────────────────────────────────────────────────────┐
│                   MySQL DATABASE                          │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐    │
│  │ students │ │equipment │ │  issue   │ │maintenance│   │
│  │          │ │          │ │ records  │ │  records  │   │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘    │
└──────────────────────────────────────────────────────────┘
```

---

## 5. Database Schema

### 5.1 Tables Overview

| Table | Description |
|-------|-------------|
| `students` | Student information and department details |
| `staff` | Administrator and lab assistant accounts |
| `equipment` | Laboratory equipment inventory |
| `issue_records` | Equipment borrowing transactions |
| `maintenance_records` | Equipment repair and maintenance logs |
| `experiments` | Lab experiment catalog |

### 5.2 Entity Relationship

- **Students** borrow **Equipment** → creates **Issue Records**
- **Staff** manages **Equipment** and **Maintenance Records**
- **Equipment** can have multiple **Maintenance Records**

---

## 6. Modules & Features

### 6.1 Authentication Module
- Secure staff login with session management
- Role-based access (Admin, Lab Assistant)
- Session timeout after 2 hours

### 6.2 Dashboard
- Overview statistics (total equipment, students, active issues)
- Recent issue/return activities
- Overdue items alerts
- Low stock warnings
- Pending maintenance notifications

### 6.3 Inventory Management
- Add, edit, delete equipment
- Category-wise filtering
- Search functionality
- Track quantity (total vs available)
- Condition status monitoring (Good/Fair/Damaged)

### 6.4 Issue & Return Module
- Issue equipment to students
- Set expected return dates
- Track active issues
- Process equipment returns
- Automatic quantity updates

### 6.5 Student Management
- Add, edit, delete student records
- Search by name, ID, or department
- View complete borrowing history

### 6.6 Maintenance Module
- Log equipment issues
- Track repair status (Pending/In Progress/Completed)
- Record repair costs
- Add repair notes

### 6.7 Reports & Analytics
- Inventory summary report
- Equipment usage statistics
- Student usage report
- Maintenance cost report

---

## 7. Project Structure

```
lohit's project/
├── app.py                  # Main Flask application
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── setup_database.py       # Database initialization
├── sju_logo.jpg           # College logo
│
├── database/
│   ├── schema.sql         # Database schema
│   └── db_helper.py       # Database connection helper
│
├── models/
│   ├── student.py         # Student model
│   ├── equipment.py       # Equipment model
│   ├── issue_return.py    # Issue/Return model
│   ├── maintenance.py     # Maintenance model
│   └── reports.py         # Reports model
│
├── static/
│   ├── css/
│   │   └── style.css      # Stylesheet
│   ├── js/
│   │   └── main.js        # JavaScript
│   └── sju_logo.jpg       # Logo for web pages
│
└── templates/
    ├── base.html              # Base template
    ├── login.html             # Login page
    ├── dashboard.html         # Dashboard
    ├── dashboard_layout.html  # Dashboard layout wrapper
    ├── inventory.html         # Inventory page
    ├── issue_equipment.html   # Issue/Return page
    ├── students.html          # Student management
    ├── student_history.html   # Student history
    ├── maintenance.html       # Maintenance page
    └── reports.html           # Reports page
```

---

## 8. Screenshots

*(Add screenshots of each module here)*

- Login Page
- Dashboard
- Inventory Management
- Issue & Return
- Student Management
- Maintenance
- Reports

---

## 9. Future Enhancements

1. **Email Notifications** - Send reminders for overdue items
2. **Barcode/QR Scanning** - Quick equipment identification
3. **Mobile App** - Access from mobile devices
4. **Export Reports** - PDF and Excel export functionality
5. **Reservation System** - Pre-book equipment for experiments
6. **Equipment Images** - Visual identification of items

---

## 10. Conclusion

The Automated Electronics Laboratory Management System successfully digitizes laboratory operations, providing real-time tracking, efficient record management, and valuable analytics. This system reduces manual effort, minimizes equipment loss, and improves overall laboratory efficiency.

---

## 11. References

- Flask Documentation: https://flask.palletsprojects.com/
- MySQL Documentation: https://dev.mysql.com/doc/
- Font Awesome Icons: https://fontawesome.com/
- Google Fonts: https://fonts.google.com/

---

**Developed for:** St. Joseph's University (SJU)
**Academic Year:** 2025-2026

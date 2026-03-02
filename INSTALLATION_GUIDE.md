# Installation Guide

## Automated Electronics Laboratory Management System

---

## Prerequisites

Before installing this application, ensure you have the following software installed on your system:

### 1. Python (Version 3.10 or higher)

**Download:** https://www.python.org/downloads/

**Installation Steps (Windows):**
1. Download the latest Python installer
2. Run the installer
3. ✅ **IMPORTANT:** Check "Add Python to PATH" during installation
4. Click "Install Now"
5. Verify installation by opening Command Prompt and typing:
   ```bash
   python --version
   ```

### 2. MySQL Server (Version 8.0 or higher)

**Download:** https://dev.mysql.com/downloads/mysql/

**Alternative (Easier):** Install **XAMPP** which includes MySQL
- Download from: https://www.apachefriends.org/download.html

**Installation Steps (XAMPP - Recommended):**
1. Download XAMPP installer
2. Run and install XAMPP
3. Open XAMPP Control Panel
4. Start **MySQL** service

---

## Installation Steps

### Step 1: Copy the Project Folder

Copy the entire project folder `lohit's project` to any location on the new computer.

**Example:** `C:\Projects\lab-management-system\`

---

### Step 2: Open Command Prompt / Terminal

**Windows:**
1. Press `Win + R`
2. Type `cmd` and press Enter
3. Navigate to the project folder:
   ```bash
   cd "C:\Projects\lab-management-system"
   ```

**OR** Right-click inside the project folder while holding Shift, then select "Open in Terminal"

---

### Step 3: Create a Virtual Environment (Recommended)

```bash
python -m venv venv
```

**Activate the virtual environment:**

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

You should see `(venv)` at the beginning of your command prompt.

---

### Step 4: Install Required Python Packages

```bash
pip install -r requirements.txt
```

This will install:
- Flask (Web Framework)
- mysql-connector-python (Database Connector)
- Werkzeug (Security utilities)

---

### Step 5: Configure the Database Connection

1. Open the file `config.py` in any text editor (Notepad, VS Code, etc.)

2. Update the database settings to match your MySQL installation:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',              # Your MySQL username
    'password': '',              # Your MySQL password (leave empty if none)
    'database': 'lab_management',
    'autocommit': False
}
```

**Common configurations:**

| Setup | User | Password |
|-------|------|----------|
| XAMPP (default) | `root` | `` (empty) |
| WAMP (default) | `root` | `` (empty) |
| MySQL standalone | `root` | Your password |

---

### Step 6: Set Up the Database

**Option A: Using the Setup Script**

```bash
python setup_database.py
```

**Option B: Manual Setup (if Option A fails)**

1. Open MySQL command line or phpMyAdmin (http://localhost/phpmyadmin)

2. Run the following SQL command to create the database:
   ```sql
   CREATE DATABASE IF NOT EXISTS lab_management;
   ```

3. Select the database:
   ```sql
   USE lab_management;
   ```

4. Copy and execute the contents of `database/schema.sql`

---

### Step 7: Run the Application

```bash
python app.py
```

You should see output like:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

---

### Step 8: Access the Application

1. Open any web browser (Chrome, Firefox, Edge, etc.)
2. Go to: **http://127.0.0.1:5000** or **http://localhost:5000**

---

## Default Login Credentials

| Field | Value |
|-------|-------|
| **Email** | admin@lab.edu |
| **Password** | admin123 |

---

## Troubleshooting

### Issue: "Module not found" error

**Solution:** Make sure you activated the virtual environment and installed requirements:
```bash
venv\Scripts\activate
pip install -r requirements.txt
```

### Issue: Database connection failed

**Solutions:**
1. Ensure MySQL service is running (check XAMPP Control Panel)
2. Verify username and password in `config.py`
3. Make sure the database `lab_management` exists

### Issue: Port 5000 is already in use

**Solution:** Edit `config.py` and change the PORT:
```python
PORT = 5001  # or any other available port
```

### Issue: Python is not recognized

**Solution:** Python was not added to PATH during installation
- Reinstall Python and check "Add Python to PATH"
- Or manually add Python to system PATH

---

## Stopping the Application

To stop the running server:
- Press `Ctrl + C` in the command prompt

---

## Quick Reference Commands

| Action | Command |
|--------|---------|
| Navigate to project | `cd "path/to/project"` |
| Activate virtual env | `venv\Scripts\activate` |
| Install dependencies | `pip install -r requirements.txt` |
| Setup database | `python setup_database.py` |
| Run application | `python app.py` |
| Stop application | `Ctrl + C` |

---

## Contact & Support

For any issues or questions, please contact the project team.

---

**Document Version:** 1.0  
**Last Updated:** January 2026

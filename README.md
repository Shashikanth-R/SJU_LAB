# Automated Electronics Laboratory Management System

A comprehensive web-based system for managing electronics laboratory equipment, students, and maintenance activities.

## Features

- **Equipment Inventory Management** - Track all laboratory equipment with real-time availability
- **Issue & Return System** - Manage equipment checkout and returns with automatic availability updates
- **Student Management** - Maintain student records and usage history
- **Maintenance Tracking** - Log and track equipment repairs and maintenance
- **Comprehensive Reports** - Generate detailed reports for inventory, usage, and maintenance
- **Modern UI** - Beautiful, responsive interface with gradient designs and smooth animations

## Technology Stack

- **Backend**: Python Flask
- **Database**: MySQL
- **Frontend**: HTML5, CSS3, JavaScript
- **Libraries**: mysql-connector-python, Werkzeug

## Installation

### Prerequisites

- Python 3.7 or higher
- MySQL Server 5.7 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone or download the project**
   ```bash
   cd "lohit's project"
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure MySQL Database**
   - Open MySQL command line or MySQL Workbench
   - Update the password in `config.py`:
     ```python
     DB_CONFIG = {
         'host': 'localhost',
         'user': 'root',
         'password': 'YOUR_MYSQL_PASSWORD',  # Update this
         'database': 'lab_management',
         'autocommit': False
     }
     ```

4. **Create Database and Tables**
   ```bash
   mysql -u root -p < database/schema.sql
   ```
   Or manually run the SQL file in MySQL Workbench

5. **Run the Application**
   ```bash
   python app.py
   ```

6. **Access the Application**
   - Open your browser and navigate to: `http://127.0.0.1:5000`
   - Login with default credentials:
     - **Email**: admin@lab.edu
     - **Password**: admin123

## Project Structure

```
lohit's project/
│
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
│
├── database/
│   ├── schema.sql             # Database schema
│   └── db_helper.py           # Database helper functions
│
├── models/
│   ├── student.py             # Student model
│   ├── equipment.py           # Equipment model
│   ├── issue_return.py        # Issue/Return model
│   ├── maintenance.py         # Maintenance model
│   └── reports.py             # Reports model
│
├── templates/
│   ├── base.html              # Base template
│   ├── login.html             # Login page
│   ├── dashboard_layout.html  # Dashboard layout
│   ├── dashboard.html         # Dashboard page
│   ├── inventory.html         # Inventory management
│   ├── issue_equipment.html   # Issue & return page
│   ├── students.html          # Student management
│   ├── student_history.html   # Student history
│   ├── maintenance.html       # Maintenance tracking
│   └── reports.html           # Reports page
│
└── static/
    ├── css/
    │   └── style.css          # Custom styles
    └── js/
        └── main.js            # JavaScript functions
```

## Usage Guide

### Dashboard
- View real-time statistics of equipment, issues, and maintenance
- Monitor alerts for overdue items and low stock
- Quick access to recent activities

### Inventory Management
- Add new equipment with details (name, category, model, quantity, location)
- Edit equipment information
- Track availability and condition status
- Search and filter by category

### Issue & Return
- Issue equipment to students with expected return dates
- View all active issues
- Process returns with one click
- Automatic availability updates

### Student Management
- Register new students
- Edit student information
- View student usage history
- Search students by ID, name, or department

### Maintenance
- Log equipment faults and issues
- Update repair status (pending, in progress, completed)
- Track repair costs
- View maintenance history

### Reports
- **Inventory Summary**: Stock levels by category
- **Usage Statistics**: Most used equipment
- **Student Usage**: Student activity reports
- **Maintenance Report**: Repair costs and status

## Database Schema

### Tables
- **students** - Student information
- **staff** - Staff/admin accounts
- **equipment** - Equipment inventory
- **experiments** - Lab experiments
- **issue_records** - Equipment issue/return tracking
- **maintenance_records** - Maintenance and repair logs

## Default Credentials

- **Admin Account**
  - Email: admin@lab.edu
  - Password: admin123

## Sample Data

The database schema includes sample data:
- 10 equipment items across different categories
- 5 sample students
- 4 sample experiments

## Features Highlights

✅ Real-time inventory tracking  
✅ Automatic availability updates  
✅ Overdue item alerts  
✅ Low stock warnings  
✅ Comprehensive search and filters  
✅ Beautiful, modern UI with gradients  
✅ Responsive design for all devices  
✅ Detailed usage history  
✅ Multiple report types  
✅ Secure session management  

## Troubleshooting

### Database Connection Error
- Verify MySQL is running
- Check credentials in `config.py`
- Ensure database `lab_management` exists

### Module Import Error
- Run `pip install -r requirements.txt`
- Ensure you're in the correct directory

### Port Already in Use
- Change PORT in `config.py` to a different value (e.g., 5001)

## Future Enhancements

- Email notifications for overdue items
- Barcode scanning for equipment
- Mobile app integration
- Advanced analytics dashboard
- Export reports to PDF/Excel
- User role-based permissions

## License

This project is created for educational purposes.

## Support

For issues or questions, please contact the lab administrator.

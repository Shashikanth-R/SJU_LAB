"""
Automated Electronics Laboratory Management System
Main Flask Application
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta
import os

# Import models
from models.student import Student
from models.equipment import Equipment
from models.issue_return import IssueReturn
from models.maintenance import Maintenance
from models.reports import Reports
from database.db_helper import db
from config import SECRET_KEY, DEBUG, HOST, PORT

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)

# Initialize database connection
db.connect()

# Login required decorator
def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'staff_id' not in session:
            flash('Please login to access this page', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    """Redirect to login or dashboard"""
    if 'staff_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Staff login"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Query staff
        query = "SELECT * FROM staff WHERE email = %s"
        result = db.execute_query(query, (email,), fetch=True)
        
        if result:
            staff = result[0]
            # For demo, accept any password (in production, use proper hashing)
            if password == 'admin123' or password == 'staff123':
                session['staff_id'] = staff['staff_id']
                session['staff_name'] = staff['name']
                session['staff_role'] = staff['role']
                flash(f'Welcome back, {staff["name"]}!', 'success')
                return redirect(url_for('dashboard'))
        
        flash('Invalid email or password', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    flash('You have been logged out successfully', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard"""
    # Get dashboard statistics
    stats = Reports.get_dashboard_stats()
    
    # Get recent activities
    recent_issues = IssueReturn.get_active_issues()[:5]
    overdue_items = IssueReturn.get_overdue_items()
    pending_maintenance = Maintenance.get_pending_maintenance()[:5]
    low_stock = Equipment.get_low_stock(threshold=5)
    
    return render_template('dashboard.html',
                         stats=stats,
                         recent_issues=recent_issues,
                         overdue_items=overdue_items,
                         pending_maintenance=pending_maintenance,
                         low_stock=low_stock)

@app.route('/inventory')
@login_required
def inventory():
    """Equipment inventory page"""
    search = request.args.get('search', '')
    category = request.args.get('category', '')
    
    if search:
        equipment_list = Equipment.search_equipment(search)
    elif category:
        equipment_list = Equipment.get_by_category(category)
    else:
        equipment_list = Equipment.get_all_equipment()
    
    categories = Equipment.get_categories()
    
    return render_template('inventory.html',
                         equipment_list=equipment_list,
                         categories=categories,
                         current_category=category,
                         search_term=search)

@app.route('/inventory/add', methods=['POST'])
@login_required
def add_equipment():
    """Add new equipment"""
    name = request.form.get('name')
    category = request.form.get('category')
    model_number = request.form.get('model_number')
    quantity = int(request.form.get('quantity', 0))
    location = request.form.get('location')
    
    result = Equipment.add_equipment(name, category, model_number, quantity, location)
    
    if result:
        flash(f'Equipment "{name}" added successfully!', 'success')
    else:
        flash('Failed to add equipment', 'danger')
    
    return redirect(url_for('inventory'))

@app.route('/inventory/edit/<int:equipment_id>', methods=['POST'])
@login_required
def edit_equipment(equipment_id):
    """Edit equipment"""
    name = request.form.get('name')
    category = request.form.get('category')
    model_number = request.form.get('model_number')
    quantity = int(request.form.get('quantity', 0))
    location = request.form.get('location')
    condition = request.form.get('condition_status')
    
    result = Equipment.update_equipment(equipment_id, name, category, model_number, 
                                       quantity, location, condition)
    
    if result is not False:
        flash('Equipment updated successfully!', 'success')
    else:
        flash('Failed to update equipment', 'danger')
    
    return redirect(url_for('inventory'))

@app.route('/inventory/delete/<int:equipment_id>')
@login_required
def delete_equipment(equipment_id):
    """Delete equipment"""
    result = Equipment.delete_equipment(equipment_id)
    
    if result is not False:
        flash('Equipment deleted successfully!', 'success')
    else:
        flash('Failed to delete equipment. It may be currently issued.', 'danger')
    
    return redirect(url_for('inventory'))

@app.route('/issue')
@login_required
def issue_page():
    """Issue equipment page"""
    students = Student.get_all_students()
    equipment_list = Equipment.get_all_equipment()
    active_issues = IssueReturn.get_active_issues()
    
    return render_template('issue_equipment.html',
                         students=students,
                         equipment_list=equipment_list,
                         active_issues=active_issues)

@app.route('/issue/equipment', methods=['POST'])
@login_required
def issue_equipment():
    """Issue equipment to student"""
    student_id = request.form.get('student_id')
    equipment_id = int(request.form.get('equipment_id'))
    quantity = int(request.form.get('quantity', 1))
    days = int(request.form.get('days', 7))
    
    result = IssueReturn.issue_equipment(student_id, equipment_id, quantity, 
                                        days, session['staff_id'])
    
    if result['success']:
        flash(result['message'], 'success')
    else:
        flash(result['message'], 'danger')
    
    return redirect(url_for('issue_page'))

@app.route('/return/<int:issue_id>')
@login_required
def return_equipment(issue_id):
    """Return equipment"""
    result = IssueReturn.return_equipment(issue_id)
    
    if result['success']:
        flash(result['message'], 'success')
    else:
        flash(result['message'], 'danger')
    
    return redirect(url_for('issue_page'))

@app.route('/students')
@login_required
def students():
    """Student management page"""
    search = request.args.get('search', '')
    
    if search:
        student_list = Student.search_students(search)
    else:
        student_list = Student.get_all_students()
    
    return render_template('students.html',
                         student_list=student_list,
                         search_term=search)

@app.route('/students/add', methods=['POST'])
@login_required
def add_student():
    """Add new student"""
    student_id = request.form.get('student_id')
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    department = request.form.get('department')
    year = int(request.form.get('year', 1))
    
    result = Student.add_student(student_id, name, email, phone, department, year)
    
    if result is not False:
        flash(f'Student "{name}" added successfully!', 'success')
    else:
        flash('Failed to add student. Student ID or email may already exist.', 'danger')
    
    return redirect(url_for('students'))

@app.route('/students/edit/<student_id>', methods=['POST'])
@login_required
def edit_student(student_id):
    """Edit student"""
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    department = request.form.get('department')
    year = int(request.form.get('year', 1))
    
    result = Student.update_student(student_id, name, email, phone, department, year)
    
    if result is not False:
        flash('Student updated successfully!', 'success')
    else:
        flash('Failed to update student', 'danger')
    
    return redirect(url_for('students'))

@app.route('/students/delete/<student_id>')
@login_required
def delete_student(student_id):
    """Delete student"""
    result = Student.delete_student(student_id)
    
    if result is not False:
        flash('Student deleted successfully!', 'success')
    else:
        flash('Failed to delete student', 'danger')
    
    return redirect(url_for('students'))

@app.route('/students/history/<student_id>')
@login_required
def student_history(student_id):
    """View student history"""
    student = Student.get_student(student_id)
    history = Student.get_student_history(student_id)
    
    return render_template('student_history.html',
                         student=student,
                         history=history)

@app.route('/maintenance')
@login_required
def maintenance():
    """Maintenance management page"""
    all_maintenance = Maintenance.get_all_maintenance()
    pending = Maintenance.get_pending_maintenance()
    equipment_list = Equipment.get_all_equipment()
    
    return render_template('maintenance.html',
                         all_maintenance=all_maintenance,
                         pending=pending,
                         equipment_list=equipment_list)

@app.route('/maintenance/add', methods=['POST'])
@login_required
def add_maintenance():
    """Log new maintenance issue"""
    equipment_id = int(request.form.get('equipment_id'))
    issue_description = request.form.get('issue_description')
    
    result = Maintenance.log_maintenance(equipment_id, issue_description, session['staff_id'])
    
    if result:
        flash('Maintenance issue logged successfully!', 'success')
    else:
        flash('Failed to log maintenance issue', 'danger')
    
    return redirect(url_for('maintenance'))

@app.route('/maintenance/update/<int:maintenance_id>', methods=['POST'])
@login_required
def update_maintenance(maintenance_id):
    """Update maintenance record"""
    status = request.form.get('status')
    cost = float(request.form.get('cost', 0))
    notes = request.form.get('notes', '')
    
    repair_date = datetime.now() if status == 'completed' else None
    
    result = Maintenance.update_maintenance(maintenance_id, status, repair_date, cost, notes)
    
    if result is not False:
        flash('Maintenance record updated successfully!', 'success')
    else:
        flash('Failed to update maintenance record', 'danger')
    
    return redirect(url_for('maintenance'))

@app.route('/reports')
@login_required
def reports():
    """Reports page"""
    report_type = request.args.get('type', 'inventory')
    
    data = None
    if report_type == 'inventory':
        data = Reports.get_inventory_summary()
    elif report_type == 'usage':
        data = Reports.get_usage_statistics()
    elif report_type == 'students':
        data = Reports.get_student_usage_report()
    elif report_type == 'maintenance':
        data = Reports.get_maintenance_report()
    
    return render_template('reports.html',
                         report_type=report_type,
                         data=data)

# API endpoints for AJAX requests
@app.route('/api/equipment/<int:equipment_id>')
@login_required
def api_get_equipment(equipment_id):
    """Get equipment details"""
    equipment = Equipment.get_equipment(equipment_id)
    return jsonify(equipment if equipment else {})

@app.route('/api/student/<student_id>')
@login_required
def api_get_student(student_id):
    """Get student details"""
    student = Student.get_student(student_id)
    return jsonify(student if student else {})

if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=DEBUG)

"""
Student Model
Handles all student-related database operations
"""

from database.db_helper import db

class Student:
    @staticmethod
    def add_student(student_id, name, email, phone, department, year):
        """Add a new student"""
        query = """
            INSERT INTO students (student_id, name, email, phone, department, year)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        return db.execute_query(query, (student_id, name, email, phone, department, year))
    
    @staticmethod
    def get_all_students():
        """Get all students"""
        query = "SELECT * FROM students ORDER BY student_id"
        return db.execute_query(query, fetch=True)
    
    @staticmethod
    def get_student(student_id):
        """Get student by ID"""
        query = "SELECT * FROM students WHERE student_id = %s"
        result = db.execute_query(query, (student_id,), fetch=True)
        return result[0] if result else None
    
    @staticmethod
    def update_student(student_id, name, email, phone, department, year):
        """Update student information"""
        query = """
            UPDATE students 
            SET name = %s, email = %s, phone = %s, department = %s, year = %s
            WHERE student_id = %s
        """
        return db.execute_query(query, (name, email, phone, department, year, student_id))
    
    @staticmethod
    def delete_student(student_id):
        """Delete a student"""
        query = "DELETE FROM students WHERE student_id = %s"
        return db.execute_query(query, (student_id,))
    
    @staticmethod
    def search_students(search_term):
        """Search students by name or ID"""
        query = """
            SELECT * FROM students 
            WHERE student_id LIKE %s OR name LIKE %s OR department LIKE %s
            ORDER BY student_id
        """
        search_pattern = f"%{search_term}%"
        return db.execute_query(query, (search_pattern, search_pattern, search_pattern), fetch=True)
    
    @staticmethod
    def get_student_history(student_id):
        """Get student's issue history"""
        query = """
            SELECT ir.*, e.name as equipment_name, e.category, s.name as issued_by_name
            FROM issue_records ir
            JOIN equipment e ON ir.equipment_id = e.equipment_id
            JOIN staff s ON ir.issued_by = s.staff_id
            WHERE ir.student_id = %s
            ORDER BY ir.issue_date DESC
        """
        return db.execute_query(query, (student_id,), fetch=True)

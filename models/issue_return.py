"""
Issue and Return Model
Handles equipment issue and return operations
"""

from database.db_helper import db
from datetime import datetime, timedelta
from models.equipment import Equipment

class IssueReturn:
    @staticmethod
    def issue_equipment(student_id, equipment_id, quantity, days, issued_by):
        """Issue equipment to a student"""
        # Check availability
        if not Equipment.check_availability(equipment_id, quantity):
            return {'success': False, 'message': 'Insufficient quantity available'}
        
        issue_date = datetime.now()
        expected_return = (datetime.now() + timedelta(days=days)).date()
        
        # Create issue record
        query = """
            INSERT INTO issue_records 
            (student_id, equipment_id, quantity, issue_date, expected_return_date, issued_by, status)
            VALUES (%s, %s, %s, %s, %s, %s, 'issued')
            RETURNING issue_id
        """
        result = db.execute_query(query, (student_id, equipment_id, quantity, 
                                            issue_date, expected_return, issued_by), fetch=True)
        issue_id = result[0]['issue_id'] if result else None
        
        if issue_id:
            # Update equipment availability
            Equipment.update_availability(equipment_id, -quantity)
            return {'success': True, 'message': 'Equipment issued successfully', 'issue_id': issue_id}
        
        return {'success': False, 'message': 'Failed to issue equipment'}
    
    @staticmethod
    def return_equipment(issue_id):
        """Return equipment"""
        # Get issue details
        issue = IssueReturn.get_issue(issue_id)
        if not issue:
            return {'success': False, 'message': 'Issue record not found'}
        
        if issue['status'] == 'returned':
            return {'success': False, 'message': 'Equipment already returned'}
        
        return_date = datetime.now()
        
        # Update issue record
        query = """
            UPDATE issue_records 
            SET actual_return_date = %s, status = 'returned'
            WHERE issue_id = %s
        """
        result = db.execute_query(query, (return_date, issue_id))
        
        if result is not False:
            # Update equipment availability
            Equipment.update_availability(issue['equipment_id'], issue['quantity'])
            return {'success': True, 'message': 'Equipment returned successfully'}
        
        return {'success': False, 'message': 'Failed to return equipment'}
    
    @staticmethod
    def get_issue(issue_id):
        """Get issue record by ID"""
        query = "SELECT * FROM issue_records WHERE issue_id = %s"
        result = db.execute_query(query, (issue_id,), fetch=True)
        return result[0] if result else None
    
    @staticmethod
    def get_active_issues(student_id=None):
        """Get all active (not returned) issues"""
        if student_id:
            query = """
                SELECT ir.*, e.name as equipment_name, e.category, s.name as student_name
                FROM issue_records ir
                JOIN equipment e ON ir.equipment_id = e.equipment_id
                JOIN students s ON ir.student_id = s.student_id
                WHERE ir.status = 'issued' AND ir.student_id = %s
                ORDER BY ir.issue_date DESC
            """
            return db.execute_query(query, (student_id,), fetch=True)
        else:
            query = """
                SELECT ir.*, e.name as equipment_name, e.category, s.name as student_name
                FROM issue_records ir
                JOIN equipment e ON ir.equipment_id = e.equipment_id
                JOIN students s ON ir.student_id = s.student_id
                WHERE ir.status = 'issued'
                ORDER BY ir.issue_date DESC
            """
            return db.execute_query(query, fetch=True)
    
    @staticmethod
    def get_all_issues():
        """Get all issue records"""
        query = """
            SELECT ir.*, e.name as equipment_name, e.category, 
                   s.name as student_name, st.name as issued_by_name
            FROM issue_records ir
            JOIN equipment e ON ir.equipment_id = e.equipment_id
            JOIN students s ON ir.student_id = s.student_id
            JOIN staff st ON ir.issued_by = st.staff_id
            ORDER BY ir.issue_date DESC
        """
        return db.execute_query(query, fetch=True)
    
    @staticmethod
    def get_overdue_items():
        """Get overdue equipment"""
        query = """
            SELECT ir.*, e.name as equipment_name, s.name as student_name, s.phone
            FROM issue_records ir
            JOIN equipment e ON ir.equipment_id = e.equipment_id
            JOIN students s ON ir.student_id = s.student_id
            WHERE ir.status = 'issued' AND ir.expected_return_date < CURRENT_DATE
            ORDER BY ir.expected_return_date
        """
        return db.execute_query(query, fetch=True)
    
    @staticmethod
    def update_overdue_status():
        """Update status of overdue items"""
        query = """
            UPDATE issue_records 
            SET status = 'overdue'
            WHERE status = 'issued' AND expected_return_date < CURRENT_DATE
        """
        return db.execute_query(query)
    
    @staticmethod
    def get_recent_returns(limit=10):
        """Get recently returned equipment"""
        query = """
            SELECT ir.*, e.name as equipment_name, s.name as student_name
            FROM issue_records ir
            JOIN equipment e ON ir.equipment_id = e.equipment_id
            JOIN students s ON ir.student_id = s.student_id
            WHERE ir.status = 'returned'
            ORDER BY ir.actual_return_date DESC
            LIMIT %s
        """
        return db.execute_query(query, (limit,), fetch=True)

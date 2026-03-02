"""
Reports Model
Handles report generation for various lab activities
"""

from database.db_helper import db

class Reports:
    @staticmethod
    def get_inventory_summary():
        """Generate inventory summary report"""
        query = """
            SELECT 
                category,
                COUNT(*) as item_count,
                SUM(total_quantity) as total_items,
                SUM(available_quantity) as available_items,
                SUM(total_quantity - available_quantity) as issued_items
            FROM equipment
            GROUP BY category
            ORDER BY category
        """
        return db.execute_query(query, fetch=True)
    
    @staticmethod
    def get_equipment_status():
        """Get equipment status summary"""
        query = """
            SELECT 
                condition_status,
                COUNT(*) as count
            FROM equipment
            GROUP BY condition_status
        """
        return db.execute_query(query, fetch=True)
    
    @staticmethod
    def get_usage_statistics(start_date=None, end_date=None):
        """Get equipment usage statistics"""
        if start_date and end_date:
            query = """
                SELECT 
                    e.name as equipment_name,
                    e.category,
                    COUNT(ir.issue_id) as times_issued,
                    SUM(ir.quantity) as total_quantity_issued
                FROM equipment e
                LEFT JOIN issue_records ir ON e.equipment_id = ir.equipment_id
                WHERE ir.issue_date BETWEEN %s AND %s
                GROUP BY e.equipment_id
                ORDER BY times_issued DESC
            """
            return db.execute_query(query, (start_date, end_date), fetch=True)
        else:
            query = """
                SELECT 
                    e.name as equipment_name,
                    e.category,
                    COUNT(ir.issue_id) as times_issued,
                    SUM(ir.quantity) as total_quantity_issued
                FROM equipment e
                LEFT JOIN issue_records ir ON e.equipment_id = ir.equipment_id
                GROUP BY e.equipment_id
                ORDER BY times_issued DESC
            """
            return db.execute_query(query, fetch=True)
    
    @staticmethod
    def get_student_usage_report():
        """Get student usage statistics"""
        query = """
            SELECT 
                s.student_id,
                s.name,
                s.department,
                COUNT(ir.issue_id) as total_issues,
                SUM(CASE WHEN ir.status = 'returned' THEN 1 ELSE 0 END) as returned,
                SUM(CASE WHEN ir.status = 'issued' THEN 1 ELSE 0 END) as active,
                SUM(CASE WHEN ir.status = 'overdue' THEN 1 ELSE 0 END) as overdue
            FROM students s
            LEFT JOIN issue_records ir ON s.student_id = ir.student_id
            GROUP BY s.student_id
            ORDER BY total_issues DESC
        """
        return db.execute_query(query, fetch=True)
    
    @staticmethod
    def get_maintenance_report(start_date=None, end_date=None):
        """Get maintenance report"""
        if start_date and end_date:
            query = """
                SELECT 
                    e.name as equipment_name,
                    e.category,
                    COUNT(mr.maintenance_id) as maintenance_count,
                    SUM(mr.cost) as total_cost,
                    SUM(CASE WHEN mr.status = 'completed' THEN 1 ELSE 0 END) as completed,
                    SUM(CASE WHEN mr.status = 'pending' THEN 1 ELSE 0 END) as pending
                FROM equipment e
                LEFT JOIN maintenance_records mr ON e.equipment_id = mr.equipment_id
                WHERE mr.reported_date BETWEEN %s AND %s
                GROUP BY e.equipment_id
                ORDER BY maintenance_count DESC
            """
            return db.execute_query(query, (start_date, end_date), fetch=True)
        else:
            query = """
                SELECT 
                    e.name as equipment_name,
                    e.category,
                    COUNT(mr.maintenance_id) as maintenance_count,
                    SUM(mr.cost) as total_cost,
                    SUM(CASE WHEN mr.status = 'completed' THEN 1 ELSE 0 END) as completed,
                    SUM(CASE WHEN mr.status = 'pending' THEN 1 ELSE 0 END) as pending
                FROM equipment e
                LEFT JOIN maintenance_records mr ON e.equipment_id = mr.equipment_id
                GROUP BY e.equipment_id
                ORDER BY maintenance_count DESC
            """
            return db.execute_query(query, fetch=True)
    
    @staticmethod
    def get_dashboard_stats():
        """Get statistics for dashboard"""
        query = """
            SELECT 
                (SELECT COUNT(*) FROM equipment) as total_equipment,
                (SELECT SUM(total_quantity) FROM equipment) as total_items,
                (SELECT SUM(available_quantity) FROM equipment) as available_items,
                (SELECT COUNT(*) FROM students) as total_students,
                (SELECT COUNT(*) FROM issue_records WHERE status = 'issued') as active_issues,
                (SELECT COUNT(*) FROM issue_records WHERE status = 'overdue') as overdue_issues,
                (SELECT COUNT(*) FROM maintenance_records WHERE status = 'pending') as pending_maintenance,
                (SELECT COUNT(*) FROM maintenance_records WHERE status = 'in_progress') as ongoing_maintenance
        """
        result = db.execute_query(query, fetch=True)
        return result[0] if result else None

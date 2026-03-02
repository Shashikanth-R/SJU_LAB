"""
Maintenance Model
Handles equipment maintenance and repair tracking
"""

from database.db_helper import db
from datetime import datetime

class Maintenance:
    @staticmethod
    def log_maintenance(equipment_id, issue_description, reported_by):
        """Log a new maintenance issue"""
        query = """
            INSERT INTO maintenance_records 
            (equipment_id, reported_by, issue_description, reported_date, status)
            VALUES (%s, %s, %s, %s, 'pending')
            RETURNING maintenance_id
        """
        result = db.execute_query(query, (equipment_id, reported_by, issue_description, datetime.now()), fetch=True)
        return result[0]['maintenance_id'] if result else None
    
    @staticmethod
    def update_maintenance(maintenance_id, status, repair_date=None, cost=0, notes=''):
        """Update maintenance record"""
        if repair_date:
            query = """
                UPDATE maintenance_records 
                SET status = %s, repair_date = %s, cost = %s, notes = %s
                WHERE maintenance_id = %s
            """
            return db.execute_query(query, (status, repair_date, cost, notes, maintenance_id))
        else:
            query = """
                UPDATE maintenance_records 
                SET status = %s, cost = %s, notes = %s
                WHERE maintenance_id = %s
            """
            return db.execute_query(query, (status, cost, notes, maintenance_id))
    
    @staticmethod
    def get_all_maintenance():
        """Get all maintenance records"""
        query = """
            SELECT mr.*, e.name as equipment_name, e.category, s.name as reported_by_name
            FROM maintenance_records mr
            JOIN equipment e ON mr.equipment_id = e.equipment_id
            JOIN staff s ON mr.reported_by = s.staff_id
            ORDER BY mr.reported_date DESC
        """
        return db.execute_query(query, fetch=True)
    
    @staticmethod
    def get_pending_maintenance():
        """Get pending maintenance records"""
        query = """
            SELECT mr.*, e.name as equipment_name, e.category, s.name as reported_by_name
            FROM maintenance_records mr
            JOIN equipment e ON mr.equipment_id = e.equipment_id
            JOIN staff s ON mr.reported_by = s.staff_id
            WHERE mr.status = 'pending'
            ORDER BY mr.reported_date
        """
        return db.execute_query(query, fetch=True)
    
    @staticmethod
    def get_maintenance_by_equipment(equipment_id):
        """Get maintenance history for specific equipment"""
        query = """
            SELECT mr.*, s.name as reported_by_name
            FROM maintenance_records mr
            JOIN staff s ON mr.reported_by = s.staff_id
            WHERE mr.equipment_id = %s
            ORDER BY mr.reported_date DESC
        """
        return db.execute_query(query, (equipment_id,), fetch=True)
    
    @staticmethod
    def get_maintenance_stats():
        """Get maintenance statistics"""
        query = """
            SELECT 
                COUNT(*) as total_records,
                SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending,
                SUM(CASE WHEN status = 'in_progress' THEN 1 ELSE 0 END) as in_progress,
                SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed,
                SUM(cost) as total_cost
            FROM maintenance_records
        """
        result = db.execute_query(query, fetch=True)
        return result[0] if result else None
    
    @staticmethod
    def get_recent_maintenance(limit=10):
        """Get recent maintenance records"""
        query = """
            SELECT mr.*, e.name as equipment_name, s.name as reported_by_name
            FROM maintenance_records mr
            JOIN equipment e ON mr.equipment_id = e.equipment_id
            JOIN staff s ON mr.reported_by = s.staff_id
            ORDER BY mr.reported_date DESC
            LIMIT %s
        """
        return db.execute_query(query, (limit,), fetch=True)

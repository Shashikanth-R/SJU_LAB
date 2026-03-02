"""
Equipment Model
Handles all equipment-related database operations
"""

from database.db_helper import db

class Equipment:
    @staticmethod
    def add_equipment(name, category, model_number, total_quantity, location):
        """Add new equipment"""
        from datetime import date
        query = """
            INSERT INTO equipment 
            (name, category, model_number, total_quantity, available_quantity, location, added_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING equipment_id
        """
        result = db.execute_query(query, (name, category, model_number, total_quantity, 
                                       total_quantity, location, date.today()), fetch=True)
        return result[0]['equipment_id'] if result else None
    
    @staticmethod
    def get_all_equipment():
        """Get all equipment"""
        query = "SELECT * FROM equipment ORDER BY category, name"
        return db.execute_query(query, fetch=True)
    
    @staticmethod
    def get_equipment(equipment_id):
        """Get equipment by ID"""
        query = "SELECT * FROM equipment WHERE equipment_id = %s"
        result = db.execute_query(query, (equipment_id,), fetch=True)
        return result[0] if result else None
    
    @staticmethod
    def update_equipment(equipment_id, name, category, model_number, total_quantity, location, condition_status):
        """Update equipment information"""
        query = """
            UPDATE equipment 
            SET name = %s, category = %s, model_number = %s, total_quantity = %s, 
                location = %s, condition_status = %s
            WHERE equipment_id = %s
        """
        return db.execute_query(query, (name, category, model_number, total_quantity, 
                                       location, condition_status, equipment_id))
    
    @staticmethod
    def delete_equipment(equipment_id):
        """Delete equipment"""
        query = "DELETE FROM equipment WHERE equipment_id = %s"
        return db.execute_query(query, (equipment_id,))
    
    @staticmethod
    def update_availability(equipment_id, quantity_change):
        """Update available quantity (positive to add, negative to subtract)"""
        query = """
            UPDATE equipment 
            SET available_quantity = available_quantity + %s
            WHERE equipment_id = %s
        """
        return db.execute_query(query, (quantity_change, equipment_id))
    
    @staticmethod
    def check_availability(equipment_id, required_quantity):
        """Check if equipment is available in required quantity"""
        query = "SELECT available_quantity FROM equipment WHERE equipment_id = %s"
        result = db.execute_query(query, (equipment_id,), fetch=True)
        if result:
            return result[0]['available_quantity'] >= required_quantity
        return False
    
    @staticmethod
    def get_by_category(category):
        """Get equipment by category"""
        query = "SELECT * FROM equipment WHERE category = %s ORDER BY name"
        return db.execute_query(query, (category,), fetch=True)
    
    @staticmethod
    def get_categories():
        """Get all unique categories"""
        query = "SELECT DISTINCT category FROM equipment ORDER BY category"
        return db.execute_query(query, fetch=True)
    
    @staticmethod
    def search_equipment(search_term):
        """Search equipment by name or category"""
        query = """
            SELECT * FROM equipment 
            WHERE name LIKE %s OR category LIKE %s OR model_number LIKE %s
            ORDER BY category, name
        """
        search_pattern = f"%{search_term}%"
        return db.execute_query(query, (search_pattern, search_pattern, search_pattern), fetch=True)
    
    @staticmethod
    def get_low_stock(threshold=5):
        """Get equipment with low stock"""
        query = """
            SELECT * FROM equipment 
            WHERE available_quantity <= %s AND available_quantity > 0
            ORDER BY available_quantity
        """
        return db.execute_query(query, (threshold,), fetch=True)
    
    @staticmethod
    def get_out_of_stock():
        """Get out of stock equipment"""
        query = "SELECT * FROM equipment WHERE available_quantity = 0"
        return db.execute_query(query, fetch=True)

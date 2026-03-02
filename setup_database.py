
import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG

def setup_database():
    try:
        # Connect to MySQL server (without database name first)
        connection = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Read schema file
            with open('database/schema.sql', 'r') as file:
                schema_sql = file.read()
            
            # Execute statements
            # Split by semicolon to handle multiple statements manually if needed, 
            # or use multi=True
            statements = schema_sql.split(';')
            
            for statement in statements:
                if statement.strip():
                    try:
                        cursor.execute(statement)
                        # Consuming any unread result if exists
                        while cursor.nextset():
                            pass
                    except Error as e:
                        print(f"Error executing statement: {e}")
            
            connection.commit()
            print("Database setup completed successfully!")
            
            cursor.close()
            connection.close()
            return True
            
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return False

if __name__ == "__main__":
    setup_database()

import psycopg2
from psycopg2 import Error
from config import DB_CONFIG

def setup_database():
    try:
        # Connect to PostgreSQL server (without database name first, connecting to 'postgres' default db)
        connection = psycopg2.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database='postgres'
        )
        connection.autocommit = True
        cursor = connection.cursor()
        
        # Create database if it doesn't exist
        db_name = DB_CONFIG['database']
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
        exists = cursor.fetchone()
        if not exists:
            cursor.execute(f"CREATE DATABASE {db_name}")
            print(f"Database {db_name} created.")
        
        cursor.close()
        connection.close()

        # Connect to the actual database
        connection = psycopg2.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database=db_name
        )
        cursor = connection.cursor()
        
        # Read schema file
        with open('database/schema_pg.sql', 'r') as file:
            schema_sql = file.read()
        
        # Execute schema
        cursor.execute(schema_sql)
        connection.commit()
        
        print("PostgreSQL Database setup completed successfully!")
        
        cursor.close()
        connection.close()
        return True
            
    except Error as e:
        print(f"Error while connecting to PostgreSQL: {e}")
        return False
    except FileNotFoundError:
        print("Error: database/schema_pg.sql not found.")
        return False

if __name__ == "__main__":
    setup_database()

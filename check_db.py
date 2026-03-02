
import mysql.connector
from mysql.connector import Error

def check_connection(user, password):
    try:
        conn = mysql.connector.connect(host='localhost', user=user, password=password)
        if conn.is_connected():
            print(f"SUCCESS: Connected with user='{user}'")
            conn.close()
            return True
    except Error as e:
        print(f"FAILED: user='{user}' - {e}")
        return False

if __name__ == "__main__":
    # Check updated config user
    print("Checking 'shashikanth'...")
    check_connection('shashikanth', 'Shashi@30')
    
    # Check default root
    print("\nChecking 'root' (empty password)...")
    check_connection('root', '')

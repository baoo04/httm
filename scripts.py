import sys
from getpass import getpass 
from werkzeug.security import generate_password_hash
from dao.dao import get_db_connection

def createsuperuser():
    print("=== Create Admin ===")
    username = input("Username: ").strip()
    full_name = input("Full name: ").strip()
    while True:
        password = getpass("Password: ")
        confirm = getpass("Confirm password: ")

        if password != confirm:
            print("Passwords do not match. Try again.\n")
        elif len(password) < 6:
            print("Password must be at least 6 characters.\n")
        else:
            break
    hashed_password = generate_password_hash(password)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM tblAdmin WHERE username=%s", (username,))
    if cursor.fetchone():
        print(f"Username '{username}' already exists.")
        cursor.close()
        conn.close()
        return
    cursor.execute("""
        INSERT INTO tblAdmin (username, password, full_name)
        VALUES (%s, %s, %s)
    """, (username, hashed_password, full_name))
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Admin '{username}' created successfully!")

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "createsuperuser":
        createsuperuser()
    else:
        print("Usage: python scripts.py createsuperuser")

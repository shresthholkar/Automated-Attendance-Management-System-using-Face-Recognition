import sqlite3
from sqlite3 import Error

DB_NAME = "attendance.db"

def create_connection():
    """ create a database connection to the SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
    return conn

def create_tables():
    """ create tables for users, face_encodings, and attendance """
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            # Users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE
                );
            """)
            # Face encodings table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS face_encodings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    encoding BLOB NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                );
            """)
            # Attendance table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS attendance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                );
            """)
            conn.commit()
        except Error as e:
            print(f"Error creating tables: {e}")
        finally:
            conn.close()
    else:
        print("Error! Cannot create the database connection.")

def add_user(name):
    """ Add a new user to the users table """
    conn = create_connection()
    user_id = None
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name) VALUES (?)", (name,))
        conn.commit()
        user_id = cursor.lastrowid
    except Error as e:
        print(f"Error adding user: {e}")
    finally:
        conn.close()
    return user_id

def add_face_encoding(user_id, encoding):
    """ Add face encoding for a user """
    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO face_encodings (user_id, encoding) VALUES (?, ?)", (user_id, encoding))
        conn.commit()
    except Error as e:
        print(f"Error adding face encoding: {e}")
    finally:
        conn.close()

def get_all_users():
    """ Get all users """
    conn = create_connection()
    users = []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM users")
        users = cursor.fetchall()
    except Error as e:
        print(f"Error fetching users: {e}")
    finally:
        conn.close()
    return users

def delete_user(user_id):
    """ Delete a user and their face encodings and attendance records """
    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM face_encodings WHERE user_id = ?", (user_id,))
        cursor.execute("DELETE FROM attendance WHERE user_id = ?", (user_id,))
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
    except Error as e:
        print(f"Error deleting user: {e}")
    finally:
        conn.close()

def get_face_encodings():
    """ Get all face encodings with user ids """
    conn = create_connection()
    encodings = []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, encoding FROM face_encodings")
        encodings = cursor.fetchall()
    except Error as e:
        print(f"Error fetching face encodings: {e}")
    finally:
        conn.close()
    return encodings

def mark_attendance(user_id):
    """ Mark attendance for a user """
    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO attendance (user_id) VALUES (?)", (user_id,))
        conn.commit()
    except Error as e:
        print(f"Error marking attendance: {e}")
    finally:
        conn.close()

def get_attendance_records():
    """ Get all attendance records with user names and timestamps """
    conn = create_connection()
    records = []
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT users.name, attendance.timestamp
            FROM attendance
            JOIN users ON attendance.user_id = users.id
            ORDER BY attendance.timestamp DESC
        """)
        records = cursor.fetchall()
    except Error as e:
        print(f"Error fetching attendance records: {e}")
    finally:
        conn.close()
    return records

if __name__ == "__main__":
    create_tables()

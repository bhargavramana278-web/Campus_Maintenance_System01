import sqlite3
import os
import hashlib
from datetime import datetime

# Ensure data directory exists
os.makedirs("data", exist_ok=True)
DB_PATH = os.path.join("data", "campus.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def hash_password(password):
    """Return SHA-256 hash of password."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def init_db():
    """Initialize database tables, migrate columns, and populate sample data if empty."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT NOT NULL,
            role TEXT NOT NULL,
            department TEXT,
            created_at TEXT NOT NULL
        )
    ''')
    
    # Complaints Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            complaint_id TEXT UNIQUE NOT NULL,
            student_name TEXT NOT NULL,
            department TEXT NOT NULL,
            building TEXT NOT NULL,
            room_no TEXT NOT NULL,
            category TEXT NOT NULL,
            problem TEXT NOT NULL,
            priority TEXT NOT NULL,
            status TEXT NOT NULL,
            date TEXT NOT NULL,
            username TEXT
        )
    ''')
    
    # Migration: add username column if older table without it exists
    cursor.execute("PRAGMA table_info(complaints)")
    columns = [col[1] for col in cursor.fetchall()]
    if "username" not in columns:
        cursor.execute("ALTER TABLE complaints ADD COLUMN username TEXT")
    
    # Maintenance Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS maintenance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            complaint_id TEXT NOT NULL,
            staff_name TEXT NOT NULL,
            repair_date TEXT NOT NULL,
            cost REAL NOT NULL,
            remarks TEXT,
            FOREIGN KEY (complaint_id) REFERENCES complaints (complaint_id)
        )
    ''')
    
    conn.commit()
    conn.close()
    
    seed_users()
    seed_sample_data()

def seed_users():
    """Populate default users for testing and role simulation."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        users = [
            ("admin", hash_password("admin123"), "Administrator", "admin", "Administration", now),
            ("staff", hash_password("staff123"), "Suresh Kumar", "staff", "Facilities & Maintenance", now),
            ("student1", hash_password("student123"), "Rahul Sharma", "student", "BCA", now),
            ("student2", hash_password("student123"), "Priya Singh", "student", "CSE", now),
        ]
        cursor.executemany('''
            INSERT INTO users (username, password_hash, full_name, role, department, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', users)
        conn.commit()
    conn.close()

def authenticate_user(username, password):
    """Verify credentials and return user profile dict or None."""
    conn = get_connection()
    cursor = conn.cursor()
    pw_hash = hash_password(password)
    cursor.execute('''
        SELECT id, username, full_name, role, department 
        FROM users 
        WHERE LOWER(username) = LOWER(?) AND password_hash = ?
    ''', (username.strip(), pw_hash))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {
            "id": row[0],
            "username": row[1],
            "full_name": row[2],
            "role": row[3],
            "department": row[4] or "General"
        }
    return None

def register_user(username, password, full_name, role="student", department="General"):
    """Register a new user account."""
    username = username.strip().lower()
    full_name = full_name.strip()
    
    if not username or not password or not full_name:
        return False, "Username, password, and full name are required."
    
    if len(password) < 4:
        return False, "Password must be at least 4 characters long."
        
    conn = get_connection()
    cursor = conn.cursor()
    try:
        pw_hash = hash_password(password)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
            INSERT INTO users (username, password_hash, full_name, role, department, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (username, pw_hash, full_name, role, department, now))
        conn.commit()
        conn.close()
        return True, "Registration successful! You can now log in."
    except sqlite3.IntegrityError:
        conn.close()
        return False, f"Username '{username}' already exists. Please choose another."
    except Exception as e:
        conn.close()
        return False, str(e)

def generate_complaint_id():
    """Generate incremental ticket ID (e.g., CMP001)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM complaints")
    count = cursor.fetchone()[0]
    conn.close()
    return f"CMP{count + 1:03d}"

def add_complaint(student_name, department, building, room_no, category, problem, priority, username=None):
    """Add a new complaint ticket with optional student username attribution."""
    conn = get_connection()
    cursor = conn.cursor()
    complaint_id = generate_complaint_id()
    today_date = datetime.now().strftime("%Y-%m-%d")
    status = "Pending"
    
    cursor.execute('''
        INSERT INTO complaints (complaint_id, student_name, department, building, room_no, category, problem, priority, status, date, username)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (complaint_id, student_name, department, building, room_no, category, problem, priority, status, today_date, username))
    
    conn.commit()
    conn.close()
    return complaint_id

def fetch_all_complaints():
    """Fetch all tickets campus-wide."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT complaint_id, student_name, department, building, room_no, category, priority, status, date FROM complaints ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def fetch_student_complaints(username):
    """Fetch complaints reported by a specific student."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT complaint_id, student_name, department, building, room_no, category, priority, status, date 
        FROM complaints 
        WHERE LOWER(username) = LOWER(?)
        ORDER BY id DESC
    ''', (username,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_student_metrics(username):
    """Get complaint count breakdown for a specific student."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT status, COUNT(*) FROM complaints WHERE LOWER(username) = LOWER(?) GROUP BY status", (username,))
    counts = dict(cursor.fetchall())
    cursor.execute("SELECT COUNT(*) FROM complaints WHERE LOWER(username) = LOWER(?)", (username,))
    total = cursor.fetchone()[0]
    conn.close()
    return {
        "total": total,
        "pending": counts.get("Pending", 0),
        "in_progress": counts.get("In Progress", 0),
        "resolved": counts.get("Resolved", 0)
    }

def search_complaint_by_id(complaint_id):
    """Look up a single complaint record by its ticket ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM complaints WHERE complaint_id = ?", (complaint_id,))
    record = cursor.fetchone()
    conn.close()
    return record

def update_status(complaint_id, new_status):
    """Update status of a complaint."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE complaints SET status = ? WHERE complaint_id = ?", (new_status, complaint_id))
    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()
    return rows_affected > 0

def add_maintenance_record(complaint_id, staff_name, repair_date, cost, remarks):
    """Log repair completion and cost, automatically setting status to Resolved."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO maintenance (complaint_id, staff_name, repair_date, cost, remarks)
        VALUES (?, ?, ?, ?, ?)
    ''', (complaint_id, staff_name, repair_date, cost, remarks))
    
    cursor.execute("UPDATE complaints SET status = 'Resolved' WHERE complaint_id = ?", (complaint_id,))
    conn.commit()
    conn.close()

def seed_sample_data():
    """Populate initial sample complaints if table is empty."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM complaints")
    if cursor.fetchone()[0] == 0:
        samples = [
            ("CMP001", "Rahul Sharma", "BCA", "Block A", "204", "Electrical", "Fan not working", "Medium", "Pending", "2026-08-18", "student1"),
            ("CMP002", "Priya Singh", "CSE", "Block B", "101", "Furniture", "Broken chair in lab", "Low", "Resolved", "2026-08-10", "student2"),
            ("CMP003", "Aman Verma", "ECE", "Computer Lab", "302", "IT", "Projector fault", "High", "In Progress", "2026-08-15", None),
            ("CMP004", "Neha Gupta", "MCA", "Block C", "118", "Plumbing", "Tap leakage", "High", "Resolved", "2026-08-12", None),
            ("CMP005", "Rohan Mehta", "BBA", "Library", "001", "Internet", "Wi-Fi down", "Medium", "Pending", "2026-08-19", None),
            ("CMP006", "Sanya Kapoor", "BCA", "Hostel Block", "405", "AC/Cooling", "AC unit leaking water", "High", "In Progress", "2026-08-20", None),
        ]
        cursor.executemany('''
            INSERT INTO complaints (complaint_id, student_name, department, building, room_no, category, problem, priority, status, date, username)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', samples)
        
        maint_samples = [
            ("CMP002", "Suresh Kumar", "2026-08-11", 450.0, "Chair leg welded"),
            ("CMP004", "Amit Verma", "2026-08-13", 800.0, "Replaced valve fitting")
        ]
        cursor.executemany('''
            INSERT INTO maintenance (complaint_id, staff_name, repair_date, cost, remarks)
            VALUES (?, ?, ?, ?, ?)
        ''', maint_samples)
        
        conn.commit()
    else:
        # Link existing sample records to student accounts if username is empty
        cursor.execute("UPDATE complaints SET username = 'student1' WHERE complaint_id = 'CMP001' AND (username IS NULL OR username = '')")
        cursor.execute("UPDATE complaints SET username = 'student2' WHERE complaint_id = 'CMP002' AND (username IS NULL OR username = '')")
        conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized and migrated successfully.")
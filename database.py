import sqlite3
import os
from datetime import datetime

# Ensure data directory exists
os.makedirs("data", exist_ok=True)
DB_PATH = os.path.join("data", "campus.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    """Initialize database tables and populate sample data if empty."""
    conn = get_connection()
    cursor = conn.cursor()
    
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
            date TEXT NOT NULL
        )
    ''')
    
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
    seed_sample_data()

def generate_complaint_id():
    """Generate incremental ticket ID (e.g., CMP001)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM complaints")
    count = cursor.fetchone()[0]
    conn.close()
    return f"CMP{count + 1:03d}"

def add_complaint(student_name, department, building, room_no, category, problem, priority):
    conn = get_connection()
    cursor = conn.cursor()
    complaint_id = generate_complaint_id()
    today_date = datetime.now().strftime("%Y-%m-%d")
    status = "Pending"
    
    cursor.execute('''
        INSERT INTO complaints (complaint_id, student_name, department, building, room_no, category, problem, priority, status, date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (complaint_id, student_name, department, building, room_no, category, problem, priority, status, today_date))
    
    conn.commit()
    conn.close()
    return complaint_id

def fetch_all_complaints():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT complaint_id, student_name, department, building, room_no, category, priority, status, date FROM complaints")
    rows = cursor.fetchall()
    conn.close()
    return rows

def search_complaint_by_id(complaint_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM complaints WHERE complaint_id = ?", (complaint_id,))
    record = cursor.fetchone()
    conn.close()
    return record

def update_status(complaint_id, new_status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE complaints SET status = ? WHERE complaint_id = ?", (new_status, complaint_id))
    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()
    return rows_affected > 0

def add_maintenance_record(complaint_id, staff_name, repair_date, cost, remarks):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO maintenance (complaint_id, staff_name, repair_date, cost, remarks)
        VALUES (?, ?, ?, ?, ?)
    ''', (complaint_id, staff_name, repair_date, cost, remarks))
    
    # Auto-update status to Resolved when repair details are logged
    cursor.execute("UPDATE complaints SET status = 'Resolved' WHERE complaint_id = ?", (complaint_id,))
    conn.commit()
    conn.close()

def seed_sample_data():
    """Populate initial sample data if table is empty."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM complaints")
    if cursor.fetchone()[0] == 0:
        samples = [
            ("CMP001", "Rahul Sharma", "BCA", "Block A", "204", "Electrical", "Fan not working", "Medium", "Pending", "2026-08-18"),
            ("CMP002", "Priya Singh", "CSE", "Block B", "101", "Furniture", "Broken chair in lab", "Low", "Resolved", "2026-08-10"),
            ("CMP003", "Aman Verma", "ECE", "Computer Lab", "302", "IT", "Projector fault", "High", "In Progress", "2026-08-15"),
            ("CMP004", "Neha Gupta", "MCA", "Block C", "118", "Plumbing", "Tap leakage", "High", "Resolved", "2026-08-12"),
            ("CMP005", "Rohan Mehta", "BBA", "Library", "001", "Internet", "Wi-Fi down", "Medium", "Pending", "2026-08-19"),
            ("CMP006", "Sanya Kapoor", "BCA", "Hostel Block", "405", "AC/Cooling", "AC unit leaking water", "High", "In Progress", "2026-08-20"),
        ]
        cursor.executemany('''
            INSERT INTO complaints (complaint_id, student_name, department, building, room_no, category, problem, priority, status, date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
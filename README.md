# CampusFix — Maintenance Control System

A desktop campus maintenance ticket management and analytics system built with Python, Tkinter, SQLite3, Pandas, and Matplotlib.

## Key Features

### 🔍 Live Search & Dynamic Filtering
- **Multi-Field Live Search**: Type ticket ID, student name, building, room number, or category to instantly filter records as you type.
- **Dropdown Filters**: Real-time filtering by **Status** (Pending, In Progress, Resolved), **Category** (Electrical, Plumbing, IT, etc.), and **Priority** (High, Medium, Low).
- **Color-Coded Status Badges**:
  - 🔴 **Pending**: Crimson badge
  - 🟡 **In Progress**: Amber/Orange badge
  - 🟢 **Resolved**: Emerald Green badge
- **Interactive Double-Click**: Double-click any row to view full details or jump straight to status update.

### 🔐 Role-Based Access Control & Authentication
- **Student Portal**:
  - Personal dashboard tracking individual ticket counts (Pending, In Progress, Resolved).
  - Lodge new maintenance tickets with student credentials verified.
  - View personal complaint history with live search and status updates.
  - Self-registration for new students.
- **Admin & Staff Portal**:
  - Campus-wide metrics and total expenditure tracking.
  - Master list of all complaints across departments and buildings with instant filtering.
  - Search tickets by ID and update status.
  - Maintenance logger: records staff name, repair date, cost (₹), and remarks.
  - Analytics dashboard with dark-themed Matplotlib charts.
  - One-click CSV export.

### 🔑 Default Demo Accounts
One-click demo login buttons are provided on the sign-in screen:

| Role | Username | Password | Access Level |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin` | `admin123` | Full Access (All Tickets, Updates, Reports, Analytics) |
| **Maintenance Staff** | `staff` | `staff123` | Operational Access (Tickets, Maintenance Logging) |
| **Student** | `student1` | `student123` | Student Access (Personal Tickets, Lodge Complaints) |

## Tech Stack

- **GUI**: Python Tkinter & ttk (Dark Theme styling)
- **Security**: SHA-256 password hashing
- **Database**: SQLite3
- **Analytics & Data Processing**: Pandas
- **Visualization**: Matplotlib

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/bhargavramana278-web/Campus_Maintenance_System01.git
   cd Campus_Maintenance_System01
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```

## Project Structure

```text
Campus_Maintenance_System01/
├── analysis.py          # Data analysis, chart generation, and CSV export
├── database.py          # SQLite database schema, user auth, and CRUD operations
├── main.py              # Tkinter UI, authentication views, and live search tables
├── requirements.txt     # Python package requirements
├── .gitignore           # Git ignore configuration
├── data/                # SQLite database storage
└── reports/             # Generated CSV reports
```

# CampusFix — Maintenance Control System

A desktop campus maintenance ticket management and analytics system built with Python, Tkinter, SQLite3, Pandas, and Matplotlib.

## Key Features

### 🔐 Role-Based Access Control & Authentication
- **Student Portal**:
  - Personal dashboard tracking individual ticket statuses (Pending, In Progress, Resolved).
  - Lodge new maintenance tickets with student details automatically authenticated and secured.
  - View personal complaint history with real-time status updates.
  - Self-registration for new students.
- **Admin & Staff Portal**:
  - Campus-wide metrics and total expenditure tracking.
  - Master list of all complaints across departments and buildings.
  - Search tickets by ID and update status.
  - Maintenance logger: records staff name, repair date, cost, and remarks.
  - Analytics dashboard with dark-themed Matplotlib charts.
  - One-click CSV export.

### 🔑 Default Demo Accounts
For instant evaluation and testing, one-click demo login buttons are provided on the sign-in screen:

| Role | Username | Password | Access Level |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin` | `admin123` | Full Access (All Tickets, Updates, Reports, Analytics) |
| **Maintenance Staff** | `staff` | `staff123` | Operational Access (Tickets, Maintenance Logging) |
| **Student** | `student1` | `student123` | Student Access (Personal Tickets, Lodge Complaints) |

## Tech Stack

- **GUI**: Python Tkinter & ttk
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
├── main.py              # Tkinter UI, authentication views, and role-based workflows
├── requirements.txt     # Python package requirements
├── .gitignore           # Git ignore configuration
├── data/                # SQLite database storage
└── reports/             # Generated CSV reports
```

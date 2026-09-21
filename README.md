# CampusFix — Maintenance Control System

A desktop maintenance ticket management and analytics system built with Python, Tkinter, SQLite3, Pandas, and Matplotlib.

## Features

- **Interactive Dashboard**: View real-time statistics including total complaints, pending vs resolved issues, and total repair expenses.
- **Ticket Registration**: Submit maintenance tickets categorized by department, building, room number, priority, and category (Electrical, Plumbing, IT, etc.).
- **Ticket Search & Update**: Search tickets by ID or building, update ticket status, priority, and room assignments.
- **Maintenance Log**: Log repair completions with assigned staff names, repair dates, costs, and remarks.
- **Analytics & Visualizations**: Multi-panel dark-themed charts displaying:
  - Complaint status breakdown (donut chart)
  - Complaints per department (bar chart)
  - Issues by category (horizontal bar chart)
  - Repair expenditure by category
- **CSV Export**: Export all complaint records to CSV with a single click.

## Tech Stack

- **GUI**: Python Tkinter & ttk
- **Database**: SQLite3
- **Data Processing & Analytics**: Pandas
- **Visualization**: Matplotlib

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/<your-username>/Campus_Maintenance_System01.git
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
├── database.py          # SQLite database schema, connections, and CRUD operations
├── main.py              # Tkinter UI and main application entry point
├── requirements.txt     # Python package requirements
├── .gitignore           # Git ignore configuration
├── data/                # SQLite database storage
└── reports/             # Generated CSV reports
```

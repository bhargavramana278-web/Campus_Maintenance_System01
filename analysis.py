import sqlite3
import os
import pandas as pd
import matplotlib.pyplot as plt

DB_PATH = os.path.join("data", "campus.db")

def get_summary_metrics():
    """Calculate summary metrics using Pandas."""
    conn = sqlite3.connect(DB_PATH)
    df_complaints = pd.read_sql_query("SELECT * FROM complaints", conn)
    df_maint = pd.read_sql_query("SELECT * FROM maintenance", conn)
    conn.close()

    total_complaints = len(df_complaints)
    pending = len(df_complaints[df_complaints['status'] == 'Pending'])
    in_progress = len(df_complaints[df_complaints['status'] == 'In Progress'])
    resolved = len(df_complaints[df_complaints['status'] == 'Resolved'])
    
    total_cost = df_maint['cost'].sum() if not df_maint.empty else 0.0
    avg_cost = df_maint['cost'].mean() if not df_maint.empty else 0.0
    
    most_common_cat = df_complaints['category'].mode()[0] if not df_complaints.empty else "N/A"
    most_reported_building = df_complaints['building'].mode()[0] if not df_complaints.empty else "N/A"

    return {
        "total": total_complaints,
        "pending": pending,
        "in_progress": in_progress,
        "resolved": resolved,
        "total_cost": total_cost,
        "avg_cost": avg_cost,
        "top_category": most_common_cat,
        "top_building": most_reported_building
    }

def generate_analytics_dashboard():
    """Generate multi-panel Matplotlib charts."""
    conn = sqlite3.connect(DB_PATH)
    df_complaints = pd.read_sql_query("SELECT * FROM complaints", conn)
    df_maint = pd.read_sql_query("SELECT * FROM maintenance", conn)
    conn.close()

    if df_complaints.empty:
        print("No data available for charts.")
        return

    # Style Configuration matching the screenshots
    plt.style.use('dark_background')
    fig, axes = plt.subplots(2, 2, figsize=(11, 7))
    fig.patch.set_facecolor('#0d1b2a')

    for ax in axes.flat:
        ax.set_facecolor('#1b263b')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#415a77')
        ax.spines['bottom'].set_color('#415a77')
        ax.tick_params(colors='#e0e1dd')

    # Chart 1: Complaints by Category (Horizontal Bar)
    cat_counts = df_complaints['category'].value_counts()
    axes[0, 0].barh(cat_counts.index, cat_counts.values, color='#4cc9f0')
    axes[0, 0].set_title('Complaints by Category', color='#e0e1dd', fontsize=11, fontweight='bold')

    # Chart 2: Status Distribution (Pie Chart)
    status_counts = df_complaints['status'].value_counts()
    colors = ['#f72585', '#4895ef', '#4cb963']
    axes[0, 1].pie(status_counts.values, labels=status_counts.index, autopct='%1.1f%%', colors=colors, textprops={'color': '#e0e1dd'})
    axes[0, 1].set_title('Status Distribution', color='#e0e1dd', fontsize=11, fontweight='bold')

    # Chart 3: Complaints by Building
    bldg_counts = df_complaints['building'].value_counts()
    axes[1, 0].bar(bldg_counts.index, bldg_counts.values, color='#f72585')
    axes[1, 0].set_title('Complaints by Building', color='#e0e1dd', fontsize=11, fontweight='bold')
    axes[1, 0].tick_params(axis='x', rotation=25)

    # Chart 4: Maintenance Cost by Category
    if not df_maint.empty:
        merged = pd.merge(df_maint, df_complaints, on='complaint_id')
        cost_by_cat = merged.groupby('category')['cost'].sum()
        axes[1, 1].bar(cost_by_cat.index, cost_by_cat.values, color='#4cb963')
    axes[1, 1].set_title('Repair Cost by Category (₹)', color='#e0e1dd', fontsize=11, fontweight='bold')
    axes[1, 1].tick_params(axis='x', rotation=25)

    plt.tight_layout()
    plt.show()

def export_to_csv():
    """Export complaints table to CSV format."""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM complaints", conn)
    conn.close()
    
    os.makedirs("reports", exist_ok=True)
    out_file = os.path.join("reports", "complaints_report.csv")
    df.to_csv(out_file, index=False)
    return out_file
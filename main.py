import tkinter as tk
from tkinter import ttk, messagebox
import database as db
import analysis as ana

# Color Scheme Definitions
COLOR_BG = "#0d1b2a"
COLOR_PANEL = "#1b263b"
COLOR_ACCENT = "#e0a96d"
COLOR_TEXT = "#ffffff"
COLOR_BTN = "#415a77"

class CampusMaintenanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CampusFix — Maintenance Control System")
        self.root.geometry("900x600")
        self.root.configure(bg=COLOR_BG)

        db.init_db()
        self.create_header()
        self.create_navigation()
        self.container = tk.Frame(self.root, bg=COLOR_BG)
        self.container.pack(fill="both", expand=True, padx=20, pady=10)

        self.show_dashboard()

    def create_header(self):
        header = tk.Frame(self.root, bg=COLOR_PANEL, height=60)
        header.pack(fill="x", side="top")
        
        lbl_logo = tk.Label(header, text="CF", font=("Helvetica", 14, "bold"), fg=COLOR_BG, bg=COLOR_ACCENT, width=3)
        lbl_logo.pack(side="left", padx=15, pady=10)
        
        lbl_title = tk.Label(header, text="CampusFix  |  Maintenance Control System", font=("Helvetica", 14, "bold"), fg=COLOR_TEXT, bg=COLOR_PANEL)
        lbl_title.pack(side="left", pady=10)

    def create_navigation(self):
        nav = tk.Frame(self.root, bg=COLOR_BG)
        nav.pack(fill="x", pady=10)

        buttons = [
            ("Dashboard", self.show_dashboard),
            ("Register", self.show_register),
            ("All Tickets", self.show_view_all),
            ("Search / Update", self.show_search_update),
            ("Maintenance Log", self.show_maintenance_log),
            ("Reports", self.show_reports),
        ]

        for text, command in buttons:
            btn = tk.Button(nav, text=text, font=("Helvetica", 10, "bold"), fg=COLOR_TEXT, bg=COLOR_BTN,
                            activebackground=COLOR_ACCENT, activeforeground=COLOR_BG, bd=0, padx=12, pady=6, command=command)
            btn.pack(side="left", padx=5)

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    # --- SCREEN 1: DASHBOARD ---
    def show_dashboard(self):
        self.clear_container()
        
        lbl_welcome = tk.Label(self.container, text="EVERY SQUEAK, LEAK, AND FLICKER — LOGGED, TRACKED, FIXED.",
                               font=("Helvetica", 14, "bold"), fg=COLOR_ACCENT, bg=COLOR_BG, wraplength=700, justify="left")
        lbl_welcome.pack(anchor="w", pady=15)

        metrics = ana.get_summary_metrics()
        
        metrics_frame = tk.Frame(self.container, bg=COLOR_BG)
        metrics_frame.pack(fill="x", pady=10)

        cards = [
            ("Total Complaints", metrics["total"]),
            ("Pending", metrics["pending"]),
            ("In Progress", metrics["in_progress"]),
            ("Resolved", metrics["resolved"]),
        ]

        for title, val in cards:
            card = tk.Frame(metrics_frame, bg=COLOR_PANEL, bd=1, relief="ridge", width=180, height=90)
            card.pack(side="left", padx=10, expand=True, fill="both")
            
            lbl_val = tk.Label(card, text=str(val), font=("Helvetica", 22, "bold"), fg=COLOR_ACCENT, bg=COLOR_PANEL)
            lbl_val.pack(pady=(10, 0))
            
            lbl_title = tk.Label(card, text=title, font=("Helvetica", 9), fg=COLOR_TEXT, bg=COLOR_PANEL)
            lbl_title.pack(pady=(0, 10))

    # --- SCREEN 2: REGISTER COMPLAINT ---
    def show_register(self):
        self.clear_container()

        lbl_head = tk.Label(self.container, text="Register a Complaint", font=("Helvetica", 14, "bold"), fg=COLOR_ACCENT, bg=COLOR_BG)
        lbl_head.pack(anchor="w", pady=10)

        form = tk.Frame(self.container, bg=COLOR_PANEL, padx=20, pady=20)
        form.pack(fill="both", expand=True)

        fields = [
            ("Student Name", "entry_name"),
            ("Department", "combo_dept"),
            ("Building", "combo_bldg"),
            ("Room No.", "entry_room"),
            ("Category", "combo_cat"),
            ("Priority", "combo_prio")
        ]

        self.form_widgets = {}

        for i, (label_text, widget_key) in enumerate(fields):
            row = i // 2
            col = (i % 2) * 2

            lbl = tk.Label(form, text=label_text, font=("Helvetica", 10), fg=COLOR_TEXT, bg=COLOR_PANEL)
            lbl.grid(row=row, column=col, sticky="w", padx=10, pady=8)

            if "entry" in widget_key:
                w = tk.Entry(form, font=("Helvetica", 10), width=25)
            elif widget_key == "combo_dept":
                w = ttk.Combobox(form, values=["BCA", "CSE", "ECE", "MCA", "BBA"], width=23, state="readonly")
            elif widget_key == "combo_bldg":
                w = ttk.Combobox(form, values=["Block A", "Block B", "Block C", "Computer Lab", "Library", "Hostel Block"], width=23, state="readonly")
            elif widget_key == "combo_cat":
                w = ttk.Combobox(form, values=["Electrical", "Furniture", "Plumbing", "IT", "Internet", "Cleaning", "AC/Cooling", "Other"], width=23, state="readonly")
            elif widget_key == "combo_prio":
                w = ttk.Combobox(form, values=["Low", "Medium", "High"], width=23, state="readonly")

            w.grid(row=row, column=col + 1, padx=10, pady=8)
            self.form_widgets[widget_key] = w

        lbl_prob = tk.Label(form, text="Problem Description", font=("Helvetica", 10), fg=COLOR_TEXT, bg=COLOR_PANEL)
        lbl_prob.grid(row=3, column=0, sticky="nw", padx=10, pady=8)

        self.txt_problem = tk.Text(form, width=60, height=4, font=("Helvetica", 10))
        self.txt_problem.grid(row=3, column=1, columnspan=3, padx=10, pady=8, sticky="w")

        btn_sub = tk.Button(form, text="Submit Complaint", font=("Helvetica", 10, "bold"), fg=COLOR_BG, bg=COLOR_ACCENT, bd=0, padx=15, pady=8, command=self.submit_complaint_form)
        btn_sub.grid(row=4, column=1, pady=15, sticky="w")

    def submit_complaint_form(self):
        name = self.form_widgets["entry_name"].get().strip()
        dept = self.form_widgets["combo_dept"].get()
        bldg = self.form_widgets["combo_bldg"].get()
        room = self.form_widgets["entry_room"].get().strip()
        cat = self.form_widgets["combo_cat"].get()
        prio = self.form_widgets["combo_prio"].get()
        prob = self.txt_problem.get("1.0", tk.END).strip()

        if not name or not dept or not bldg or not room or not cat or not prio or not prob:
            messagebox.showerror("Validation Error", "Please fill in all required fields.")
            return

        cid = db.add_complaint(name, dept, bldg, room, cat, prob, prio)
        messagebox.showinfo("Success", f"Complaint Registered Successfully!\nTicket ID: {cid}")
        self.show_register()

    # --- SCREEN 3: VIEW ALL COMPLAINTS ---
    def show_view_all(self):
        self.clear_container()

        lbl_head = tk.Label(self.container, text="All Complaints", font=("Helvetica", 14, "bold"), fg=COLOR_ACCENT, bg=COLOR_BG)
        lbl_head.pack(anchor="w", pady=10)

        cols = ("ID", "Student Name", "Department", "Building", "Room", "Category", "Priority", "Status", "Date")
        tree = ttk.Treeview(self.container, columns=cols, show="headings", height=15)

        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=95, anchor="center")

        tree.pack(fill="both", expand=True)

        for record in db.fetch_all_complaints():
            tree.insert("", tk.END, values=record)

    # --- SCREEN 4: SEARCH & UPDATE STATUS ---
    def show_search_update(self):
        self.clear_container()

        frame_search = tk.Frame(self.container, bg=COLOR_PANEL, padx=15, pady=15)
        frame_search.pack(fill="x", pady=10)

        tk.Label(frame_search, text="Enter Complaint ID:", font=("Helvetica", 10), fg=COLOR_TEXT, bg=COLOR_PANEL).pack(side="left", padx=5)
        
        self.ent_search_id = tk.Entry(frame_search, font=("Helvetica", 10), width=15)
        self.ent_search_id.pack(side="left", padx=5)

        btn_search = tk.Button(frame_search, text="Search", font=("Helvetica", 10, "bold"), fg=COLOR_BG, bg=COLOR_ACCENT, bd=0, padx=10, command=self.perform_search)
        btn_search.pack(side="left", padx=5)

        self.frame_details = tk.Frame(self.container, bg=COLOR_BG)
        self.frame_details.pack(fill="both", expand=True, pady=10)

    def perform_search(self):
        for widget in self.frame_details.winfo_children():
            widget.destroy()

        cid = self.ent_search_id.get().strip()
        record = db.search_complaint_by_id(cid)

        if not record:
            messagebox.showerror("Not Found", f"No record found for ID: {cid}")
            return

        # Record Indexing: 1:cid, 2:name, 3:dept, 4:bldg, 5:room, 6:cat, 7:prob, 8:prio, 9:status, 10:date
        info_txt = f"ID: {record[1]}  |  Student: {record[2]}  |  Building: {record[4]} ({record[5]})\nCategory: {record[6]}  |  Priority: {record[8]}  |  Date: {record[10]}\n\nProblem: {record[7]}"
        
        lbl_info = tk.Label(self.frame_details, text=info_txt, font=("Helvetica", 10), fg=COLOR_TEXT, bg=COLOR_PANEL, justify="left", padx=15, pady=15)
        lbl_info.pack(fill="x", pady=10)

        frame_upd = tk.Frame(self.frame_details, bg=COLOR_PANEL, padx=15, pady=15)
        frame_upd.pack(fill="x")

        tk.Label(frame_upd, text=f"Current Status: {record[9]}", font=("Helvetica", 10, "bold"), fg=COLOR_ACCENT, bg=COLOR_PANEL).pack(side="left", padx=10)
        tk.Label(frame_upd, text="Update To:", font=("Helvetica", 10), fg=COLOR_TEXT, bg=COLOR_PANEL).pack(side="left", padx=5)

        self.combo_new_status = ttk.Combobox(frame_upd, values=["Pending", "In Progress", "Resolved"], state="readonly", width=15)
        self.combo_new_status.set(record[9])
        self.combo_new_status.pack(side="left", padx=5)

        btn_upd = tk.Button(frame_upd, text="Save Status", font=("Helvetica", 10, "bold"), fg=COLOR_BG, bg=COLOR_ACCENT, bd=0, padx=10, command=lambda: self.save_status(record[1]))
        btn_upd.pack(side="left", padx=10)

    def save_status(self, cid):
        new_status = self.combo_new_status.get()
        if db.update_status(cid, new_status):
            messagebox.showinfo("Success", f"Status for {cid} updated to '{new_status}'.")
            self.perform_search()

    # --- SCREEN 5: ADD MAINTENANCE LOG ---
    def show_maintenance_log(self):
        self.clear_container()

        lbl_head = tk.Label(self.container, text="Add Maintenance Details", font=("Helvetica", 14, "bold"), fg=COLOR_ACCENT, bg=COLOR_BG)
        lbl_head.pack(anchor="w", pady=10)

        form = tk.Frame(self.container, bg=COLOR_PANEL, padx=20, pady=20)
        form.pack(fill="both", expand=True)

        labels = ["Complaint ID", "Staff Name", "Repair Date (YYYY-MM-DD)", "Cost (₹)", "Remarks"]
        self.maint_entries = {}

        for i, text in enumerate(labels):
            tk.Label(form, text=text, font=("Helvetica", 10), fg=COLOR_TEXT, bg=COLOR_PANEL).grid(row=i, column=0, sticky="w", padx=10, pady=8)
            ent = tk.Entry(form, font=("Helvetica", 10), width=30)
            ent.grid(row=i, column=1, padx=10, pady=8)
            self.maint_entries[text] = ent

        btn_save = tk.Button(form, text="Save Maintenance Record", font=("Helvetica", 10, "bold"), fg=COLOR_BG, bg=COLOR_ACCENT, bd=0, padx=15, pady=8, command=self.save_maintenance)
        btn_save.grid(row=5, column=1, pady=15, sticky="w")

    def save_maintenance(self):
        cid = self.maint_entries["Complaint ID"].get().strip()
        staff = self.maint_entries["Staff Name"].get().strip()
        rdate = self.maint_entries["Repair Date (YYYY-MM-DD)"].get().strip()
        cost_str = self.maint_entries["Cost (₹)"].get().strip()
        remarks = self.maint_entries["Remarks"].get().strip()

        if not cid or not db.search_complaint_by_id(cid):
            messagebox.showerror("Error", "Valid Complaint ID is required.")
            return

        try:
            cost = float(cost_str)
            if cost < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Cost must be a valid non-negative number.")
            return

        db.add_maintenance_record(cid, staff, rdate, cost, remarks)
        messagebox.showinfo("Success", f"Maintenance details added and {cid} marked as Resolved!")
        self.show_maintenance_log()

    # --- SCREEN 6: REPORTS & ANALYTICS ---
    def show_reports(self):
        self.clear_container()

        lbl_head = tk.Label(self.container, text="Reports & Data Analytics", font=("Helvetica", 14, "bold"), fg=COLOR_ACCENT, bg=COLOR_BG)
        lbl_head.pack(anchor="w", pady=10)

        metrics = ana.get_summary_metrics()

        summary_txt = (
            f"• Total Complaints Logged: {metrics['total']}\n"
            f"• Pending: {metrics['pending']}  |  In Progress: {metrics['in_progress']}  |  Resolved: {metrics['resolved']}\n"
            f"• Total Maintenance Expenditure: ₹{metrics['total_cost']:,.2f}\n"
            f"• Average Cost per Repair: ₹{metrics['avg_cost']:,.2f}\n"
            f"• Most Common Problem Category: {metrics['top_category']}\n"
            f"• Building with Highest Complaints: {metrics['top_building']}"
        )

        lbl_summary = tk.Label(self.container, text=summary_txt, font=("Helvetica", 11), fg=COLOR_TEXT, bg=COLOR_PANEL, justify="left", padx=20, pady=15)
        lbl_summary.pack(fill="x", pady=10)

        btn_frame = tk.Frame(self.container, bg=COLOR_BG)
        btn_frame.pack(fill="x", pady=10)

        btn_charts = tk.Button(btn_frame, text="Render Analytics Dashboard (Matplotlib)", font=("Helvetica", 10, "bold"), fg=COLOR_BG, bg=COLOR_ACCENT, bd=0, padx=15, pady=8, command=ana.generate_analytics_dashboard)
        btn_charts.pack(side="left", padx=5)

        btn_export = tk.Button(btn_frame, text="Export Tickets to CSV", font=("Helvetica", 10, "bold"), fg=COLOR_TEXT, bg=COLOR_BTN, bd=0, padx=15, pady=8, command=self.export_csv)
        btn_export.pack(side="left", padx=5)

    def export_csv(self):
        path = ana.export_to_csv()
        messagebox.showinfo("Export Successful", f"Data exported successfully to:\n{path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CampusMaintenanceApp(root)
    root.mainloop()
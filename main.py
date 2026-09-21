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
COLOR_MUTED = "#8d99ae"
COLOR_DANGER = "#e63946"
COLOR_SUCCESS = "#4cb963"
COLOR_WARNING = "#f39c12"

class CampusMaintenanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CampusFix — Maintenance Control System")
        self.root.geometry("1040x680")
        self.root.minsize(940, 620)
        self.root.configure(bg=COLOR_BG)

        # Active Session
        self.current_user = None

        # Setup TTK Theme & Treeview Styles
        self.setup_ttk_styles()

        # Initialize Database
        db.init_db()

        # UI Components
        self.header_frame = None
        self.nav_frame = None
        self.container = None

        self.create_shell()
        self.show_login_screen()

    def setup_ttk_styles(self):
        """Configure ttk styles for dark theme Treeviews and Comboboxes."""
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass

        # Dark theme Treeview
        style.configure(
            "Treeview",
            background=COLOR_PANEL,
            foreground=COLOR_TEXT,
            fieldbackground=COLOR_PANEL,
            rowheight=28,
            font=("Helvetica", 9),
            borderwidth=0
        )
        style.configure(
            "Treeview.Heading",
            background="#24334a",
            foreground=COLOR_ACCENT,
            font=("Helvetica", 10, "bold"),
            relief="flat",
            padding=5
        )
        style.map("Treeview", background=[("selected", "#3d5a80")], foreground=[("selected", "#ffffff")])
        style.map("Treeview.Heading", background=[("active", "#314463")])

    def create_shell(self):
        """Create main persistent layout frames."""
        self.header_frame = tk.Frame(self.root, bg=COLOR_PANEL, height=60)
        self.header_frame.pack(fill="x", side="top")

        self.nav_frame = tk.Frame(self.root, bg=COLOR_BG)
        self.nav_frame.pack(fill="x", pady=(8, 4))

        self.container = tk.Frame(self.root, bg=COLOR_BG)
        self.container.pack(fill="both", expand=True, padx=20, pady=10)

    def clear_container(self):
        """Clear dynamic content area."""
        for widget in self.container.winfo_children():
            widget.destroy()

    def update_header(self):
        """Render header with branding and user status."""
        for widget in self.header_frame.winfo_children():
            widget.destroy()

        # Logo & Title
        lbl_logo = tk.Label(self.header_frame, text="CF", font=("Helvetica", 14, "bold"), fg=COLOR_BG, bg=COLOR_ACCENT, width=3)
        lbl_logo.pack(side="left", padx=15, pady=10)

        lbl_title = tk.Label(self.header_frame, text="CampusFix  |  Maintenance Control System", font=("Helvetica", 14, "bold"), fg=COLOR_TEXT, bg=COLOR_PANEL)
        lbl_title.pack(side="left", pady=10)

        # Logged-in User Profile & Logout Button
        if self.current_user:
            btn_logout = tk.Button(
                self.header_frame, text="Logout", font=("Helvetica", 9, "bold"),
                fg=COLOR_TEXT, bg=COLOR_DANGER, activebackground="#b71c1c", activeforeground=COLOR_TEXT,
                bd=0, padx=12, pady=5, cursor="hand2", command=self.logout
            )
            btn_logout.pack(side="right", padx=15, pady=12)

            role_badge = self.current_user['role'].upper()
            user_info = f"👤 {self.current_user['full_name']}  [{role_badge}]"
            lbl_user = tk.Label(self.header_frame, text=user_info, font=("Helvetica", 10, "bold"), fg=COLOR_ACCENT, bg=COLOR_PANEL)
            lbl_user.pack(side="right", padx=10, pady=14)

    def update_navigation(self):
        """Render navigation buttons based on current user role."""
        for widget in self.nav_frame.winfo_children():
            widget.destroy()

        if not self.current_user:
            return

        role = self.current_user.get("role", "student")

        if role == "student":
            buttons = [
                ("My Dashboard", self.show_student_dashboard),
                ("Register Complaint", self.show_register),
                ("My Tickets", self.show_my_tickets),
            ]
        else:
            # Admin & Staff Navigation
            buttons = [
                ("Dashboard", self.show_dashboard),
                ("Register", self.show_register),
                ("All Tickets", self.show_view_all),
                ("Search / Update", self.show_search_update),
                ("Maintenance Log", self.show_maintenance_log),
                ("Reports", self.show_reports),
            ]

        for text, command in buttons:
            btn = tk.Button(
                self.nav_frame, text=text, font=("Helvetica", 10, "bold"), fg=COLOR_TEXT, bg=COLOR_BTN,
                activebackground=COLOR_ACCENT, activeforeground=COLOR_BG, bd=0, padx=12, pady=6,
                cursor="hand2", command=command
            )
            btn.pack(side="left", padx=5)

    # ==========================================
    # --- AUTHENTICATION & LOGIN SCREENS ---
    # ==========================================
    def show_login_screen(self):
        """Display the modern login card with demo buttons."""
        self.clear_container()
        self.update_header()
        self.update_navigation()

        wrapper = tk.Frame(self.container, bg=COLOR_BG)
        wrapper.pack(expand=True)

        card = tk.Frame(wrapper, bg=COLOR_PANEL, bd=1, relief="ridge", padx=30, pady=25)
        card.pack()

        lbl_icon = tk.Label(card, text="🔐", font=("Helvetica", 28), fg=COLOR_ACCENT, bg=COLOR_PANEL)
        lbl_icon.pack(pady=(0, 5))

        lbl_title = tk.Label(card, text="Account Sign In", font=("Helvetica", 16, "bold"), fg=COLOR_TEXT, bg=COLOR_PANEL)
        lbl_title.pack(pady=(0, 20))

        # Username
        tk.Label(card, text="Username", font=("Helvetica", 10), fg=COLOR_MUTED, bg=COLOR_PANEL, anchor="w").pack(fill="x")
        self.ent_login_user = tk.Entry(card, font=("Helvetica", 11), width=32, bd=0, highlightthickness=1, highlightbackground=COLOR_BTN)
        self.ent_login_user.pack(pady=(4, 12), ipady=5)

        # Password
        tk.Label(card, text="Password", font=("Helvetica", 10), fg=COLOR_MUTED, bg=COLOR_PANEL, anchor="w").pack(fill="x")
        self.ent_login_pass = tk.Entry(card, font=("Helvetica", 11), width=32, show="•", bd=0, highlightthickness=1, highlightbackground=COLOR_BTN)
        self.ent_login_pass.pack(pady=(4, 16), ipady=5)
        self.ent_login_pass.bind("<Return>", lambda event: self.handle_login())

        # Login Button
        btn_login = tk.Button(
            card, text="Sign In", font=("Helvetica", 11, "bold"),
            fg=COLOR_BG, bg=COLOR_ACCENT, activebackground="#f0be85", bd=0,
            cursor="hand2", pady=8, command=self.handle_login
        )
        btn_login.pack(fill="x", pady=(5, 15))

        # Toggle to Registration
        lbl_register = tk.Label(card, text="New Student? Register here", font=("Helvetica", 9, "underline"), fg=COLOR_ACCENT, bg=COLOR_PANEL, cursor="hand2")
        lbl_register.pack(pady=(0, 15))
        lbl_register.bind("<Button-1>", lambda event: self.show_register_user_screen())

        # Demo Credentials Shortcut
        sep = tk.Frame(card, bg=COLOR_BTN, height=1)
        sep.pack(fill="x", pady=(5, 10))

        tk.Label(card, text="Quick 1-Click Demo Login:", font=("Helvetica", 9), fg=COLOR_MUTED, bg=COLOR_PANEL).pack(pady=(0, 6))

        demo_frame = tk.Frame(card, bg=COLOR_PANEL)
        demo_frame.pack()

        tk.Button(demo_frame, text="Admin", font=("Helvetica", 8, "bold"), fg=COLOR_TEXT, bg=COLOR_BTN, bd=0, padx=8, pady=4, cursor="hand2", command=lambda: self.quick_demo_login("admin", "admin123")).pack(side="left", padx=3)
        tk.Button(demo_frame, text="Staff", font=("Helvetica", 8, "bold"), fg=COLOR_TEXT, bg=COLOR_BTN, bd=0, padx=8, pady=4, cursor="hand2", command=lambda: self.quick_demo_login("staff", "staff123")).pack(side="left", padx=3)
        tk.Button(demo_frame, text="Student", font=("Helvetica", 8, "bold"), fg=COLOR_TEXT, bg=COLOR_BTN, bd=0, padx=8, pady=4, cursor="hand2", command=lambda: self.quick_demo_login("student1", "student123")).pack(side="left", padx=3)

    def quick_demo_login(self, username, password):
        """Shortcut for quick evaluation."""
        self.ent_login_user.delete(0, tk.END)
        self.ent_login_user.insert(0, username)
        self.ent_login_pass.delete(0, tk.END)
        self.ent_login_pass.insert(0, password)
        self.handle_login()

    def handle_login(self):
        """Validate credentials and launch role dashboard."""
        username = self.ent_login_user.get().strip()
        password = self.ent_login_pass.get().strip()

        if not username or not password:
            messagebox.showwarning("Incomplete", "Please enter both username and password.")
            return

        user = db.authenticate_user(username, password)
        if not user:
            messagebox.showerror("Login Failed", "Invalid username or password.\nPlease check your credentials.")
            return

        self.current_user = user
        self.update_header()
        self.update_navigation()

        if user["role"] == "student":
            self.show_student_dashboard()
        else:
            self.show_dashboard()

    def show_register_user_screen(self):
        """Screen for new students to register an account."""
        self.clear_container()

        wrapper = tk.Frame(self.container, bg=COLOR_BG)
        wrapper.pack(expand=True)

        card = tk.Frame(wrapper, bg=COLOR_PANEL, bd=1, relief="ridge", padx=30, pady=25)
        card.pack()

        lbl_icon = tk.Label(card, text="📝", font=("Helvetica", 26), fg=COLOR_ACCENT, bg=COLOR_PANEL)
        lbl_icon.pack(pady=(0, 5))

        lbl_title = tk.Label(card, text="Student Registration", font=("Helvetica", 16, "bold"), fg=COLOR_TEXT, bg=COLOR_PANEL)
        lbl_title.pack(pady=(0, 15))

        fields = [
            ("Full Name", "reg_name"),
            ("Department", "reg_dept"),
            ("Desired Username", "reg_user"),
            ("Password", "reg_pass"),
        ]

        self.reg_entries = {}
        for label_text, key in fields:
            tk.Label(card, text=label_text, font=("Helvetica", 9), fg=COLOR_MUTED, bg=COLOR_PANEL, anchor="w").pack(fill="x", pady=(4, 0))
            if key == "reg_dept":
                w = ttk.Combobox(card, values=["BCA", "CSE", "ECE", "MCA", "BBA", "Civil", "Mechanical"], state="readonly", font=("Helvetica", 10), width=30)
                w.set("BCA")
            elif key == "reg_pass":
                w = tk.Entry(card, font=("Helvetica", 11), width=32, show="•", bd=0, highlightthickness=1, highlightbackground=COLOR_BTN)
            else:
                w = tk.Entry(card, font=("Helvetica", 11), width=32, bd=0, highlightthickness=1, highlightbackground=COLOR_BTN)
            w.pack(pady=(2, 8), ipady=4)
            self.reg_entries[key] = w

        btn_reg = tk.Button(
            card, text="Create Student Account", font=("Helvetica", 10, "bold"),
            fg=COLOR_BG, bg=COLOR_ACCENT, activebackground="#f0be85", bd=0,
            cursor="hand2", pady=8, command=self.handle_registration
        )
        btn_reg.pack(fill="x", pady=(10, 10))

        btn_back = tk.Button(card, text="Back to Login", font=("Helvetica", 9), fg=COLOR_TEXT, bg=COLOR_BTN, bd=0, pady=4, cursor="hand2", command=self.show_login_screen)
        btn_back.pack(fill="x")

    def handle_registration(self):
        """Process registration form."""
        name = self.reg_entries["reg_name"].get().strip()
        dept = self.reg_entries["reg_dept"].get().strip()
        username = self.reg_entries["reg_user"].get().strip()
        password = self.reg_entries["reg_pass"].get().strip()

        success, msg = db.register_user(username, password, name, role="student", department=dept)
        if success:
            messagebox.showinfo("Success", msg)
            self.show_login_screen()
            self.ent_login_user.insert(0, username)
        else:
            messagebox.showerror("Registration Error", msg)

    def logout(self):
        """Clear active user session and redirect to login."""
        if messagebox.askyesno("Logout", "Are you sure you want to sign out?"):
            self.current_user = None
            self.show_login_screen()

    # ==========================================
    # --- SCREEN: STUDENT DASHBOARD ---
    # ==========================================
    def show_student_dashboard(self):
        """Dashboard tailored specifically for the logged-in student."""
        self.clear_container()

        welcome_text = f"Welcome back, {self.current_user['full_name']}! ({self.current_user['department']} Department)"
        lbl_welcome = tk.Label(self.container, text=welcome_text, font=("Helvetica", 14, "bold"), fg=COLOR_ACCENT, bg=COLOR_BG)
        lbl_welcome.pack(anchor="w", pady=(10, 5))

        lbl_sub = tk.Label(self.container, text="Track your campus maintenance tickets or report a new issue below.", font=("Helvetica", 10), fg=COLOR_MUTED, bg=COLOR_BG)
        lbl_sub.pack(anchor="w", pady=(0, 15))

        metrics = db.get_student_metrics(self.current_user["username"])

        metrics_frame = tk.Frame(self.container, bg=COLOR_BG)
        metrics_frame.pack(fill="x", pady=10)

        cards = [
            ("My Total Tickets", metrics["total"], COLOR_ACCENT),
            ("Pending Review", metrics["pending"], COLOR_WARNING),
            ("In Progress", metrics["in_progress"], "#3498db"),
            ("Resolved / Fixed", metrics["resolved"], COLOR_SUCCESS),
        ]

        for title, val, color in cards:
            card = tk.Frame(metrics_frame, bg=COLOR_PANEL, bd=1, relief="ridge", width=180, height=90)
            card.pack(side="left", padx=10, expand=True, fill="both")

            lbl_val = tk.Label(card, text=str(val), font=("Helvetica", 22, "bold"), fg=color, bg=COLOR_PANEL)
            lbl_val.pack(pady=(10, 0))

            lbl_title = tk.Label(card, text=title, font=("Helvetica", 9), fg=COLOR_TEXT, bg=COLOR_PANEL)
            lbl_title.pack(pady=(0, 10))

        # Quick Actions
        actions_frame = tk.Frame(self.container, bg=COLOR_PANEL, padx=20, pady=20)
        actions_frame.pack(fill="x", pady=20)

        tk.Label(actions_frame, text="Need something repaired or fixed?", font=("Helvetica", 12, "bold"), fg=COLOR_TEXT, bg=COLOR_PANEL).pack(anchor="w")
        tk.Label(actions_frame, text="Submit a ticket for lighting, Wi-Fi, classroom furniture, water leakage, or AC issues.", font=("Helvetica", 9), fg=COLOR_MUTED, bg=COLOR_PANEL).pack(anchor="w", pady=(2, 10))

        btn_new_ticket = tk.Button(
            actions_frame, text="➕ Lodge New Complaint", font=("Helvetica", 10, "bold"),
            fg=COLOR_BG, bg=COLOR_ACCENT, activebackground="#f0be85", bd=0, padx=15, pady=8, cursor="hand2",
            command=self.show_register
        )
        btn_new_ticket.pack(side="left", padx=(0, 10))

        btn_my_tickets = tk.Button(
            actions_frame, text="📋 View My Tickets", font=("Helvetica", 10, "bold"),
            fg=COLOR_TEXT, bg=COLOR_BTN, activebackground=COLOR_ACCENT, bd=0, padx=15, pady=8, cursor="hand2",
            command=self.show_my_tickets
        )
        btn_my_tickets.pack(side="left")

    # ==========================================
    # --- HELPER: CONFIGURE TREE TAGS ---
    # ==========================================
    def configure_tree_tags(self, tree):
        """Attach color-coded status badges and styling to Treeview tags."""
        tree.tag_configure("status_pending", foreground="#ff6b6b")
        tree.tag_configure("status_in_progress", foreground="#f39c12")
        tree.tag_configure("status_resolved", foreground="#4cb963")
        tree.tag_configure("row_even", background="#172235")
        tree.tag_configure("row_odd", background="#1b263b")

    # ==========================================
    # --- SCREEN: MY TICKETS (STUDENT ONLY) ---
    # ==========================================
    def show_my_tickets(self):
        """Displays tickets submitted by logged-in student with live search."""
        self.clear_container()

        lbl_head = tk.Label(self.container, text="My Maintenance Tickets", font=("Helvetica", 14, "bold"), fg=COLOR_ACCENT, bg=COLOR_BG)
        lbl_head.pack(anchor="w", pady=(5, 10))

        raw_records = db.fetch_student_complaints(self.current_user["username"])

        # Filter bar
        filter_bar = tk.Frame(self.container, bg=COLOR_PANEL, padx=12, pady=10)
        filter_bar.pack(fill="x", pady=(0, 10))

        tk.Label(filter_bar, text="🔍 Search:", font=("Helvetica", 9, "bold"), fg=COLOR_TEXT, bg=COLOR_PANEL).pack(side="left", padx=(0, 5))
        ent_search = tk.Entry(filter_bar, font=("Helvetica", 9), width=20)
        ent_search.pack(side="left", padx=(0, 15))

        tk.Label(filter_bar, text="Status:", font=("Helvetica", 9, "bold"), fg=COLOR_TEXT, bg=COLOR_PANEL).pack(side="left", padx=(0, 5))
        combo_status = ttk.Combobox(filter_bar, values=["All Statuses", "Pending", "In Progress", "Resolved"], state="readonly", width=14)
        combo_status.set("All Statuses")
        combo_status.pack(side="left", padx=(0, 15))

        lbl_count = tk.Label(filter_bar, text="", font=("Helvetica", 9), fg=COLOR_MUTED, bg=COLOR_PANEL)
        lbl_count.pack(side="right", padx=5)

        cols = ("Ticket ID", "Building", "Room", "Category", "Priority", "Status", "Date Submitted")
        tree = ttk.Treeview(self.container, columns=cols, show="headings", height=14)

        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")

        tree.pack(fill="both", expand=True)
        self.configure_tree_tags(tree)

        def refresh_table(*args):
            query = ent_search.get().strip().lower()
            sel_status = combo_status.get()

            for item in tree.get_children():
                tree.delete(item)

            count = 0
            for i, r in enumerate(raw_records):
                # r: (complaint_id, student_name, department, building, room_no, category, priority, status, date)
                cid, _, _, bldg, room, cat, prio, status, date = r

                # Apply Filters
                if sel_status != "All Statuses" and status != sel_status:
                    continue

                combined_text = f"{cid} {bldg} {room} {cat} {prio} {status} {date}".lower()
                if query and query not in combined_text:
                    continue

                display_row = (cid, bldg, room, cat, prio, f"● {status}", date)
                status_tag = f"status_{status.lower().replace(' ', '_')}"
                row_tag = "row_even" if count % 2 == 0 else "row_odd"

                tree.insert("", tk.END, values=display_row, tags=(status_tag, row_tag))
                count += 1

            lbl_count.config(text=f"Showing {count} of {len(raw_records)} tickets")

        ent_search.bind("<KeyRelease>", refresh_table)
        combo_status.bind("<<ComboboxSelected>>", refresh_table)

        # Double click to view details
        def on_ticket_double_click(event):
            item = tree.selection()
            if not item:
                return
            vals = tree.item(item[0], "values")
            cid = vals[0]
            rec = db.search_complaint_by_id(cid)
            if rec:
                details = (
                    f"Ticket ID: {rec[1]}\n"
                    f"Category: {rec[6]}  |  Priority: {rec[8]}\n"
                    f"Location: {rec[4]} (Room {rec[5]})\n"
                    f"Status: {rec[9]}  |  Submitted: {rec[10]}\n\n"
                    f"Problem Reported:\n{rec[7]}"
                )
                messagebox.showinfo(f"Ticket Details — {cid}", details)

        tree.bind("<Double-1>", on_ticket_double_click)
        refresh_table()

    # ==========================================
    # --- SCREEN 1: CAMPUS-WIDE DASHBOARD ---
    # ==========================================
    def show_dashboard(self):
        """Full campus analytics dashboard for Admin & Staff."""
        self.clear_container()

        lbl_welcome = tk.Label(self.container, text="EVERY SQUEAK, LEAK, AND FLICKER — LOGGED, TRACKED, FIXED.",
                               font=("Helvetica", 14, "bold"), fg=COLOR_ACCENT, bg=COLOR_BG, wraplength=750, justify="left")
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

    # ==========================================
    # --- SCREEN 2: REGISTER COMPLAINT ---
    # ==========================================
    def show_register(self):
        self.clear_container()

        lbl_head = tk.Label(self.container, text="Register a Maintenance Complaint", font=("Helvetica", 14, "bold"), fg=COLOR_ACCENT, bg=COLOR_BG)
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
        is_student = (self.current_user and self.current_user.get("role") == "student")

        for i, (label_text, widget_key) in enumerate(fields):
            row = i // 2
            col = (i % 2) * 2

            lbl = tk.Label(form, text=label_text, font=("Helvetica", 10), fg=COLOR_TEXT, bg=COLOR_PANEL)
            lbl.grid(row=row, column=col, sticky="w", padx=10, pady=8)

            if widget_key == "entry_name":
                w = tk.Entry(form, font=("Helvetica", 10), width=25)
                if is_student:
                    w.insert(0, self.current_user["full_name"])
                    w.config(state="readonly")
            elif widget_key == "combo_dept":
                w = ttk.Combobox(form, values=["BCA", "CSE", "ECE", "MCA", "BBA", "Civil", "Mechanical"], width=23, state="readonly")
                if is_student and self.current_user.get("department"):
                    w.set(self.current_user["department"])
                    w.config(state="disabled")
                else:
                    w.set("BCA")
            elif widget_key == "combo_bldg":
                w = ttk.Combobox(form, values=["Block A", "Block B", "Block C", "Computer Lab", "Library", "Hostel Block"], width=23, state="readonly")
                w.set("Block A")
            elif widget_key == "combo_cat":
                w = ttk.Combobox(form, values=["Electrical", "Furniture", "Plumbing", "IT", "Internet", "Cleaning", "AC/Cooling", "Other"], width=23, state="readonly")
                w.set("Electrical")
            elif widget_key == "combo_prio":
                w = ttk.Combobox(form, values=["Low", "Medium", "High"], width=23, state="readonly")
                w.set("Medium")
            elif widget_key == "entry_room":
                w = tk.Entry(form, font=("Helvetica", 10), width=25)

            w.grid(row=row, column=col + 1, padx=10, pady=8)
            self.form_widgets[widget_key] = w

        lbl_prob = tk.Label(form, text="Problem Description", font=("Helvetica", 10), fg=COLOR_TEXT, bg=COLOR_PANEL)
        lbl_prob.grid(row=3, column=0, sticky="nw", padx=10, pady=8)

        self.txt_problem = tk.Text(form, width=60, height=4, font=("Helvetica", 10))
        self.txt_problem.grid(row=3, column=1, columnspan=3, padx=10, pady=8, sticky="w")

        btn_sub = tk.Button(form, text="Submit Complaint", font=("Helvetica", 10, "bold"), fg=COLOR_BG, bg=COLOR_ACCENT, bd=0, padx=15, pady=8, cursor="hand2", command=self.submit_complaint_form)
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

        username = self.current_user["username"] if self.current_user else None
        cid = db.add_complaint(name, dept, bldg, room, cat, prob, prio, username=username)
        messagebox.showinfo("Success", f"Complaint Registered Successfully!\nTicket ID: {cid}")

        if self.current_user and self.current_user.get("role") == "student":
            self.show_my_tickets()
        else:
            self.show_register()

    # ==========================================
    # --- SCREEN 3: VIEW ALL COMPLAINTS (ENHANCED) ---
    # ==========================================
    def show_view_all(self):
        """Displays all campus tickets with live search, filters, and color badges."""
        self.clear_container()

        lbl_head = tk.Label(self.container, text="All Campus Complaints", font=("Helvetica", 14, "bold"), fg=COLOR_ACCENT, bg=COLOR_BG)
        lbl_head.pack(anchor="w", pady=(5, 10))

        raw_records = db.fetch_all_complaints()

        # Filter Toolbar Frame
        filter_bar = tk.Frame(self.container, bg=COLOR_PANEL, padx=12, pady=10)
        filter_bar.pack(fill="x", pady=(0, 10))

        # Search box
        tk.Label(filter_bar, text="🔍 Search:", font=("Helvetica", 9, "bold"), fg=COLOR_TEXT, bg=COLOR_PANEL).pack(side="left", padx=(0, 5))
        ent_search = tk.Entry(filter_bar, font=("Helvetica", 9), width=18)
        ent_search.pack(side="left", padx=(0, 12))

        # Status Filter
        tk.Label(filter_bar, text="Status:", font=("Helvetica", 9, "bold"), fg=COLOR_TEXT, bg=COLOR_PANEL).pack(side="left", padx=(0, 5))
        combo_status = ttk.Combobox(filter_bar, values=["All Statuses", "Pending", "In Progress", "Resolved"], state="readonly", width=13)
        combo_status.set("All Statuses")
        combo_status.pack(side="left", padx=(0, 12))

        # Category Filter
        tk.Label(filter_bar, text="Category:", font=("Helvetica", 9, "bold"), fg=COLOR_TEXT, bg=COLOR_PANEL).pack(side="left", padx=(0, 5))
        combo_cat = ttk.Combobox(filter_bar, values=["All Categories", "Electrical", "Furniture", "Plumbing", "IT", "Internet", "Cleaning", "AC/Cooling", "Other"], state="readonly", width=14)
        combo_cat.set("All Categories")
        combo_cat.pack(side="left", padx=(0, 12))

        # Priority Filter
        tk.Label(filter_bar, text="Priority:", font=("Helvetica", 9, "bold"), fg=COLOR_TEXT, bg=COLOR_PANEL).pack(side="left", padx=(0, 5))
        combo_prio = ttk.Combobox(filter_bar, values=["All Priorities", "High", "Medium", "Low"], state="readonly", width=12)
        combo_prio.set("All Priorities")
        combo_prio.pack(side="left", padx=(0, 12))

        # Reset button
        def reset_filters():
            ent_search.delete(0, tk.END)
            combo_status.set("All Statuses")
            combo_cat.set("All Categories")
            combo_prio.set("All Priorities")
            apply_filter()

        btn_reset = tk.Button(filter_bar, text="Reset", font=("Helvetica", 8, "bold"), fg=COLOR_TEXT, bg=COLOR_BTN, bd=0, padx=8, pady=3, cursor="hand2", command=reset_filters)
        btn_reset.pack(side="left")

        # Result Counter
        lbl_count = tk.Label(filter_bar, text="", font=("Helvetica", 9), fg=COLOR_MUTED, bg=COLOR_PANEL)
        lbl_count.pack(side="right", padx=5)

        # Complaints Table
        cols = ("ID", "Student Name", "Department", "Building", "Room", "Category", "Priority", "Status", "Date")
        tree = ttk.Treeview(self.container, columns=cols, show="headings", height=14)

        col_widths = {"ID": 80, "Student Name": 125, "Department": 75, "Building": 105, "Room": 65, "Category": 100, "Priority": 80, "Status": 110, "Date": 95}
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=col_widths.get(col, 95), anchor="center")

        tree.pack(fill="both", expand=True)
        self.configure_tree_tags(tree)

        # Dynamic Filtering logic
        def apply_filter(*args):
            query = ent_search.get().strip().lower()
            sel_status = combo_status.get()
            sel_cat = combo_cat.get()
            sel_prio = combo_prio.get()

            for item in tree.get_children():
                tree.delete(item)

            matched_count = 0
            for i, r in enumerate(raw_records):
                # r: (complaint_id, student_name, department, building, room_no, category, priority, status, date)
                cid, sname, dept, bldg, room, cat, prio, status, dt = r

                if sel_status != "All Statuses" and status != sel_status:
                    continue
                if sel_cat != "All Categories" and cat != sel_cat:
                    continue
                if sel_prio != "All Priorities" and prio != sel_prio:
                    continue

                row_search_text = f"{cid} {sname} {dept} {bldg} {room} {cat} {prio} {status} {dt}".lower()
                if query and query not in row_search_text:
                    continue

                status_tag = f"status_{status.lower().replace(' ', '_')}"
                row_tag = "row_even" if matched_count % 2 == 0 else "row_odd"

                display_row = (cid, sname, dept, bldg, room, cat, prio, f"● {status}", dt)
                tree.insert("", tk.END, values=display_row, tags=(status_tag, row_tag))
                matched_count += 1

            lbl_count.config(text=f"Showing {matched_count} of {len(raw_records)} tickets")

        ent_search.bind("<KeyRelease>", apply_filter)
        combo_status.bind("<<ComboboxSelected>>", apply_filter)
        combo_cat.bind("<<ComboboxSelected>>", apply_filter)
        combo_prio.bind("<<ComboboxSelected>>", apply_filter)

        # Double click to open Search / Update for that ticket
        def on_row_double_click(event):
            item = tree.selection()
            if not item:
                return
            vals = tree.item(item[0], "values")
            ticket_id = vals[0]
            self.show_search_update()
            self.ent_search_id.insert(0, ticket_id)
            self.perform_search()

        tree.bind("<Double-1>", on_row_double_click)
        apply_filter()

    # ==========================================
    # --- SCREEN 4: SEARCH & UPDATE STATUS ---
    # ==========================================
    def show_search_update(self):
        self.clear_container()

        frame_search = tk.Frame(self.container, bg=COLOR_PANEL, padx=15, pady=15)
        frame_search.pack(fill="x", pady=10)

        tk.Label(frame_search, text="Enter Complaint ID:", font=("Helvetica", 10), fg=COLOR_TEXT, bg=COLOR_PANEL).pack(side="left", padx=5)

        self.ent_search_id = tk.Entry(frame_search, font=("Helvetica", 10), width=15)
        self.ent_search_id.pack(side="left", padx=5)

        btn_search = tk.Button(frame_search, text="Search", font=("Helvetica", 10, "bold"), fg=COLOR_BG, bg=COLOR_ACCENT, bd=0, padx=10, cursor="hand2", command=self.perform_search)
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

        btn_upd = tk.Button(frame_upd, text="Save Status", font=("Helvetica", 10, "bold"), fg=COLOR_BG, bg=COLOR_ACCENT, bd=0, padx=10, cursor="hand2", command=lambda: self.save_status(record[1]))
        btn_upd.pack(side="left", padx=10)

    def save_status(self, cid):
        new_status = self.combo_new_status.get()
        if db.update_status(cid, new_status):
            messagebox.showinfo("Success", f"Status for {cid} updated to '{new_status}'.")
            self.perform_search()

    # ==========================================
    # --- SCREEN 5: ADD MAINTENANCE LOG ---
    # ==========================================
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
            
            # Default staff name to logged-in user if available
            if text == "Staff Name" and self.current_user:
                ent.insert(0, self.current_user["full_name"])

            ent.grid(row=i, column=1, padx=10, pady=8)
            self.maint_entries[text] = ent

        btn_save = tk.Button(form, text="Save Maintenance Record", font=("Helvetica", 10, "bold"), fg=COLOR_BG, bg=COLOR_ACCENT, bd=0, padx=15, pady=8, cursor="hand2", command=self.save_maintenance)
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

    # ==========================================
    # --- SCREEN 6: REPORTS & ANALYTICS ---
    # ==========================================
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

        btn_charts = tk.Button(btn_frame, text="Render Analytics Dashboard (Matplotlib)", font=("Helvetica", 10, "bold"), fg=COLOR_BG, bg=COLOR_ACCENT, bd=0, padx=15, pady=8, cursor="hand2", command=ana.generate_analytics_dashboard)
        btn_charts.pack(side="left", padx=5)

        btn_export = tk.Button(btn_frame, text="Export Tickets to CSV", font=("Helvetica", 10, "bold"), fg=COLOR_TEXT, bg=COLOR_BTN, bd=0, padx=15, pady=8, cursor="hand2", command=self.export_csv)
        btn_export.pack(side="left", padx=5)

    def export_csv(self):
        path = ana.export_to_csv()
        messagebox.showinfo("Export Successful", f"Data exported successfully to:\n{path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CampusMaintenanceApp(root)
    root.mainloop()
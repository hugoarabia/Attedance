import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3
import smtplib, ssl, datetime

class AMSApp(tk.Tk):
    def __init__(self):
        super().__init__()
        # ---------------- SETUP ROOT WINDOW ----------------
        self.title("AMS")
        self.geometry("1000x700")
        self.resizable(False, False)
        self.configure(bg="lightgray")
        
        # ---------------- TITLE LABEL (Always Visible) ----------------
        self.title_label = tk.Label(self, text="ATTENDANCE MANAGEMENT SYSTEM", 
                                    font=("Helvetica", 24, "bold"), 
                                    bg="#4682B4", fg="white", pady=10)
        self.title_label.pack(fill=tk.X)
        
        # ---------------- DATABASE SETUP ----------------
        self.conn = sqlite3.connect('professor_student.db')
        self.cursor = self.conn.cursor()
        self.setup_database()
        
        # ---------------- GMAIL REMINDER FEATURE ----------------
        self.GMAIL_SENDER = "bio.hunters10@gmail.com"      # <-- Replace with your Gmail address
        self.GMAIL_PASSWORD = "ljab fqkc ptdf qwzk"         # <-- Replace with your Gmail app password
        
        # Professor login status
        self.is_professor_logged_in = False
        
        # ---------------- BUILD UI ----------------
        self.create_widgets()
        self.show_login_frame()
    
    def setup_database(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS students (
            first_name TEXT,
            middle_name TEXT,
            last_name TEXT,
            suffix TEXT,
            student_number TEXT PRIMARY KEY,
            course TEXT,
            section TEXT,
            year_level TEXT
        )''')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS professors (
            username TEXT PRIMARY KEY,
            password TEXT
        )''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                account_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT,
                middle_name TEXT,
                last_name TEXT,
                suffix TEXT,
                age TEXT,
                birthdate TEXT,
                email TEXT UNIQUE,
                cell_number TEXT,
                fingerprint_status TEXT
            )
        ''')
        self.conn.commit()
    
    def create_widgets(self):
        self.create_login_frame()
        self.create_register_frame()
        self.create_dashboard_frame()
    
    # ------------------ TOGGLE PASSWORD FUNCTIONS ------------------
    def toggle_password(self, entry, checkbox_var):
        if checkbox_var.get():
            entry.config(show="")
        else:
            entry.config(show="*")
    
    def toggle_password_signup(self):
        if self.password_checkbox_var_reg.get():
            self.password_entry_reg.config(show="")
            self.confirm_password_entry_reg.config(show="")
        else:
            self.password_entry_reg.config(show="*")
            self.confirm_password_entry_reg.config(show="*")
    
    # ------------------ NAVIGATION FUNCTIONS ------------------
    def show_dashboard(self):
        self.login_frame.pack_forget()
        self.register_frame.pack_forget()
        self.dashboard_frame.pack(fill="both", expand=True)
    
    def go_back_to_login(self):
        self.is_professor_logged_in = False
        self.dashboard_frame.pack_forget()
        self.register_frame.pack_forget()
        self.login_frame.pack(fill="both", expand=True)
    
    # ------------------ FINGERPRINT FUNCTIONS ------------------
    def scan_fingerprint(self):
        # Used in the Sign Up form (professors)
        self.fingerprint_status.config(text="Fingerprint Status: Scanning...", fg="blue")
        self.fingerprint_status.after(2000, lambda: self.fingerprint_status.config(text="Fingerprint Status: Scanned Successfully", fg="green"))
    
    def register_fingerprint(self):
        # Currently unused; included per original code
        if self.fingerprint_status.cget("text") == "Fingerprint Status: Scanned Successfully":
            messagebox.showinfo("Success", "Fingerprint registered successfully!")
        else:
            messagebox.showwarning("Warning", "Please scan your fingerprint first.")
    
    # ------------------ PROFESSOR REGISTRATION & LOGIN ------------------
    def register_professor(self):
        username = self.username_entry_reg.get().strip()
        password = self.password_entry_reg.get().strip()
        confirm_password = self.confirm_password_entry_reg.get().strip()
        
        if not username or not password:
            messagebox.showerror("Input Error", "Please fill in both fields.")
            return
        
        if password != confirm_password:
            messagebox.showerror("Password Error", "Passwords do not match.")
            return
        
        try:
            self.cursor.execute("INSERT INTO professors (username, password) VALUES (?, ?)", (username, password))
            self.conn.commit()
            messagebox.showinfo("Success", "Professor registered successfully!")
            
            # Clear the entry fields
            self.username_entry_reg.delete(0, tk.END)
            self.password_entry_reg.delete(0, tk.END)
            self.confirm_password_entry_reg.delete(0, tk.END)
            
            # Show login screen
            self.register_frame.pack_forget()
            self.login_frame.pack(fill="both", expand=True)
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists.")
    
    def login_professor(self):
        username = self.username_entry_log.get().strip()
        password = self.password_entry_log.get().strip()
        
        if not username or not password:
            messagebox.showerror("Input Error", "Please fill in both fields.")
            return
        
        self.cursor.execute("SELECT * FROM professors WHERE username = ?", (username,))
        professor = self.cursor.fetchone()
        
        if professor and professor[1] == password:
            messagebox.showinfo("Success", "Login successful!")
            self.is_professor_logged_in = True
            self.show_dashboard()
        else:
            messagebox.showerror("Error", "Invalid username or password.")
    
    def switch_to_register(self):
        self.login_frame.pack_forget()
        self.register_frame.pack(fill="both", expand=True)
    
    # ------------------ DASHBOARD & LEFT MENU ------------------
    def show_dashboard_screen(self):
        self.clear_right_frame()
        dashboard_label = tk.Label(self.right_frame, text="DASHBOARD", 
                                   font=("Helvetica", 18, "bold"), bg="#4682B4", fg="white")
        dashboard_label.pack(pady=10)
        first_text_label = tk.Label(self.right_frame, text="Welcome to the Dashboard!",
                                    font=("Helvetica", 20), bg="lightgray", wraplength=400)
        first_text_label.pack(anchor="center", padx=10, pady=10)
    
    def show_records_screen(self):
        self.clear_right_frame()
        records_label = tk.Label(self.right_frame, text="VIEW/ADD RECORDS", 
                                 font=("Helvetica", 20, "bold"), bg="#91BDF5")
        records_label.pack(pady=10)
        second_text_label = tk.Label(self.right_frame, text="COURSES",
                                     font=("Helvetica", 20), bg="lightgray", wraplength=400)
        second_text_label.pack(anchor="center", padx=5, pady=10)
        bsit_button = tk.Button(self.right_frame, text="BACHELOR OF SCIENCE IN INFORMATION TECHNOLOGY", 
                                 font=("Arial", 14), bg="#4682B4", fg="white", command=self.yearlevel_and_section_frame)
        bsit_button.pack(pady=10, ipadx=5, ipady=21)
        bscs_button = tk.Button(self.right_frame, text="BACHELOR OF SCIENCE IN COMPUTER SCIENCE", 
                                font=("Arial", 14), bg="#4682B4", fg="white")
        bscs_button.pack(pady=10, ipadx=38, ipady=20)
        add_course_button = tk.Button(self.right_frame, text="BACHELOR OF SCIENCE IN INFORMATION SYSTEM", 
                                      font=("Arial", 14), bg="#4682B4", fg="white")
        add_course_button.pack(pady=10, ipadx=36, ipady=20)
    
    def show_schedule_screen(self):
        self.clear_right_frame()
        schedule_label = tk.Label(self.right_frame, text="SCHEDULE", 
                                  font=("Helvetica", 18, "bold"), bg="lightgray")
        schedule_label.pack(pady=10)
        third_text_label = tk.Label(self.right_frame, text="",
                                    font=("Helvetica", 20), bg="lightgray", wraplength=400)
        third_text_label.pack(anchor="center", padx=10, pady=10)
        reminder_button = tk.Button(self.right_frame, text="Schedule Class Reminder", 
                                    font=("Arial", 12), bg="#4682B4", fg="white", command=self.schedule_email_reminder)
        reminder_button.pack(pady=10, ipadx=10, ipady=5)
    
    # ------------------ ACCOUNTS SECTION ------------------
    def show_account_screen(self):
        self.clear_right_frame()
        account_label = tk.Label(self.right_frame, text="ACCOUNT", 
                                 font=("Helvetica", 18, "bold"), bg="lightgray")
        account_label.pack(pady=10)
        register_account_button = tk.Button(self.right_frame, text="Register Account", 
                                            font=("Arial", 12), bg="#4682B4", fg="white", command=self.show_register_account_form)
        register_account_button.pack(pady=10)
        delete_account_button = tk.Button(self.right_frame, text="Delete Account", 
                                          font=("Arial", 12), bg="#4682B4", fg="white", command=self.delete_account)
        delete_account_button.pack(pady=10)
    
    def show_register_account_form(self):
        self.clear_right_frame()
        title_label = tk.Label(self.right_frame, text="REGISTER YOUR ACCOUNT",
                               font=("Helvetica", 18, "bold"), bg="lightgray")
        title_label.pack(pady=10)
        
        form_frame = tk.Frame(self.right_frame, bg="white", bd=2, relief=tk.SUNKEN)
        form_frame.pack(padx=20, pady=20, fill="both", expand=False)
        
        # First Name
        tk.Label(form_frame, text="First Name:", font=("Arial", 12), bg="white")\
            .grid(row=0, column=0, padx=10, pady=10, sticky="e")
        entry_first_name = tk.Entry(form_frame, font=("Arial", 12), width=25)
        entry_first_name.grid(row=0, column=1, padx=10, pady=10)
        
        # Middle Name
        tk.Label(form_frame, text="Middle Name (Optional):", font=("Arial", 12), bg="white")\
            .grid(row=1, column=0, padx=10, pady=10, sticky="e")
        entry_middle_name = tk.Entry(form_frame, font=("Arial", 12), width=25)
        entry_middle_name.grid(row=1, column=1, padx=10, pady=10)
        
        # Last Name
        tk.Label(form_frame, text="Last Name:", font=("Arial", 12), bg="white")\
            .grid(row=2, column=0, padx=10, pady=10, sticky="e")
        entry_last_name = tk.Entry(form_frame, font=("Arial", 12), width=25)
        entry_last_name.grid(row=2, column=1, padx=10, pady=10)
        
        # Suffix
        tk.Label(form_frame, text="Suffix:", font=("Arial", 12), bg="white")\
            .grid(row=3, column=0, padx=10, pady=10, sticky="e")
        entry_suffix = tk.Entry(form_frame, font=("Arial", 12), width=25)
        entry_suffix.grid(row=3, column=1, padx=10, pady=10)
        
        # Age
        tk.Label(form_frame, text="Age:", font=("Arial", 12), bg="white")\
            .grid(row=4, column=0, padx=10, pady=10, sticky="e")
        entry_age = tk.Entry(form_frame, font=("Arial", 12), width=25)
        entry_age.grid(row=4, column=1, padx=10, pady=10)
        
        # Birthdate
        tk.Label(form_frame, text="Birthdate:", font=("Arial", 12), bg="white")\
            .grid(row=5, column=0, padx=10, pady=10, sticky="e")
        entry_birthdate = tk.Entry(form_frame, font=("Arial", 12), width=25)
        entry_birthdate.grid(row=5, column=1, padx=10, pady=10)
        
        # Email
        tk.Label(form_frame, text="Email:", font=("Arial", 12), bg="white")\
            .grid(row=6, column=0, padx=10, pady=10, sticky="e")
        entry_email = tk.Entry(form_frame, font=("Arial", 12), width=25)
        entry_email.grid(row=6, column=1, padx=10, pady=10)
        
        # Cell Number
        tk.Label(form_frame, text="Cell Number:", font=("Arial", 12), bg="white")\
            .grid(row=7, column=0, padx=10, pady=10, sticky="e")
        entry_cell = tk.Entry(form_frame, font=("Arial", 12), width=25)
        entry_cell.grid(row=7, column=1, padx=10, pady=10)
        
        # Fingerprint
        fingerprint_label = tk.Label(form_frame, text="Fingerprint Status: Not Scanned", 
                                     font=("Arial", 10), fg="red", bg="white")
        fingerprint_label.grid(row=8, column=0, columnspan=2, pady=10)
        
        def scan_fingerprint_account():
            fingerprint_label.config(text="Fingerprint Status: Scanning...", fg="blue")
            fingerprint_label.after(2000, lambda: fingerprint_label.config(text="Fingerprint Status: Scanned Successfully", fg="green"))
        
        scan_btn = tk.Button(form_frame, text="Scan Fingerprint", font=("Arial", 12), bg="blue", fg="white", 
                             command=scan_fingerprint_account)
        scan_btn.grid(row=9, column=0, padx=10, pady=10, sticky="e")
        
        def register_account_inner():
            first_name = entry_first_name.get().strip()
            middle_name = entry_middle_name.get().strip()
            last_name = entry_last_name.get().strip()
            suffix = entry_suffix.get().strip()
            age = entry_age.get().strip()
            birthdate = entry_birthdate.get().strip()
            email = entry_email.get().strip()
            cell = entry_cell.get().strip()
            fp_status = fingerprint_label.cget("text")
            
            if not first_name or not last_name or not email:
                messagebox.showerror("Input Error", "Please fill at least First Name, Last Name, and Email.")
                return
            
            try:
                self.cursor.execute('''
                    INSERT INTO accounts (first_name, middle_name, last_name, suffix, age, birthdate, email, cell_number, fingerprint_status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (first_name, middle_name, last_name, suffix, age, birthdate, email, cell, fp_status))
                self.conn.commit()
                messagebox.showinfo("Success", "Account registered successfully!")
                
                entry_first_name.delete(0, tk.END)
                entry_middle_name.delete(0, tk.END)
                entry_last_name.delete(0, tk.END)
                entry_suffix.delete(0, tk.END)
                entry_age.delete(0, tk.END)
                entry_birthdate.delete(0, tk.END)
                entry_email.delete(0, tk.END)
                entry_cell.delete(0, tk.END)
                fingerprint_label.config(text="Fingerprint Status: Not Scanned", fg="red")
                
                self.show_account_screen()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "An account with that Email already exists.")
        
        register_btn = tk.Button(form_frame, text="Register", font=("Arial", 12), bg="#4682B4", fg="white",
                                 command=register_account_inner)
        register_btn.grid(row=9, column=1, padx=10, pady=10, sticky="w")
        
        cancel_btn = tk.Button(self.right_frame, text="Cancel", font=("Arial", 12), bg="gray", fg="white",
                               command=self.show_account_screen)
        cancel_btn.pack()
    
    def delete_account(self):
        email_to_delete = simpledialog.askstring("Delete Account", "Enter Email of the account to delete:")
        if not email_to_delete:
            return
        self.cursor.execute("SELECT * FROM accounts WHERE email = ?", (email_to_delete,))
        account = self.cursor.fetchone()
        if account:
            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete account with Email: {email_to_delete}?")
            if confirm:
                self.cursor.execute("DELETE FROM accounts WHERE email = ?", (email_to_delete,))
                self.conn.commit()
                messagebox.showinfo("Deleted", f"Account with email '{email_to_delete}' has been deleted.")
        else:
            messagebox.showerror("Not Found", f"No account found with email '{email_to_delete}'.")
    
    # ------------------ YEAR LEVEL & SECTION (SCROLLABLE) ------------------
    def on_mouse_wheel(self, event, canvas):
        canvas.yview_scroll(-1 * (event.delta // 120), "units")
    
    def add_section(self, year_frame, add_button):
        entry_frame = tk.Frame(year_frame, bg="lightgray")
        entry_frame.pack(pady=5)
        section_entry = tk.Entry(entry_frame, font=("Arial", 14), width=25, bd=2, bg="white")
        section_entry.pack(side="left", padx=5)
        confirm_button = tk.Button(entry_frame, text="Confirm", font=("Arial", 12), bg="#4682B4", fg="white",
                                   command=lambda: self.confirm_add_section(year_frame, entry_frame, section_entry.get(), add_button))
        confirm_button.pack(side="left", padx=5)
    
    def confirm_add_section(self, year_frame, entry_frame, new_section, add_button):
        if new_section:
            add_button.pack_forget()
            section_button = tk.Button(year_frame, text=new_section, font=("Arial", 14), bg="#4682B4", fg="white")
            section_button.pack(pady=5, ipadx=200, ipady=5)
            add_button.pack(pady=5, ipadx=190, ipady=5)
        entry_frame.destroy()
    
    def yearlevel_and_section_frame(self):
        self.clear_right_frame()
        yearlevel_label = tk.Label(self.right_frame, text="VIEW/ADD RECORDS", 
                                   font=("Helvetica", 18, "bold"), bg="#4682B4", fg="white")
        yearlevel_label.pack(pady=10)
        
        container = tk.Frame(self.right_frame, bg="lightgray")
        container.pack(fill="both", expand=True)
        
        def set_scrollbars(*args):
            left_scrollbar.set(*args)
            right_scrollbar.set(*args)
        
        canvas = tk.Canvas(container, bg="lightgray", width=800, height=460, yscrollcommand=set_scrollbars)
        left_scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        right_scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        left_scrollbar.pack(side="left", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        right_scrollbar.pack(side="left", fill="y")
        
        scroll_frame = tk.Frame(canvas, bg="lightgray")
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        
        canvas.bind_all("<MouseWheel>", lambda event: self.on_mouse_wheel(event, canvas))
        
        section_names = {
            1: ["LFCA111M010", "LFCA322M011"],
            2: ["LFCA211M025", "LFCA211A005"],
            3: ["LFCA311M045", "LFCA311M046"],
            4: ["LFCA411M055", "LFCA411M056"]
        }
        
        for year in range(1, 5):
            year_frame = tk.Frame(scroll_frame, bg="lightgray", width=750, relief=tk.SUNKEN, bd=2)
            year_frame.pack(fill=tk.X, padx=10, pady=10)
            if year == 1:
                year_label_text = "1ST YEAR"
            elif year == 2:
                year_label_text = "2ND YEAR"
            elif year == 3:
                year_label_text = "3RD YEAR"
            else:
                year_label_text = "4TH YEAR"
            year_label = tk.Label(year_frame, text=year_label_text, font=("Helvetica", 15, "bold"), fg="white", bg="gray")
            year_label.pack(anchor="w", padx=5, pady=10)
            for section in section_names.get(year, []):
                section_button = tk.Button(year_frame, text=section, font=("Arial", 14), bg="#4682B4", fg="white")
                section_button.pack(pady=5, ipadx=200, ipady=5)
            add_section_button = tk.Button(year_frame, text="ADD SECTION (+)", font=("Arial", 14), bg="#4682B4", fg="white")
            add_section_button.config(command=lambda yf=year_frame, ab=add_section_button: self.add_section(yf, ab))
            add_section_button.pack(pady=5, ipadx=190, ipady=5)
    
    def clear_right_frame(self):
        for widget in self.right_frame.winfo_children():
            widget.destroy()
    
    # ------------------ GMAIL REMINDER FEATURE ------------------
    def send_email_reminder(self, recipient, subject, body):
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(self.GMAIL_SENDER, self.GMAIL_PASSWORD)
                msg = f"Subject: {subject}\nFrom: {self.GMAIL_SENDER}\nTo: {recipient}\n\n{body}"
                server.sendmail(self.GMAIL_SENDER, recipient, msg)
            messagebox.showinfo("Email Sent", f"Reminder email sent to {recipient}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send email: {e}")
    
    def send_bulk_email_reminder(self, recipients, subject, body):
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(self.GMAIL_SENDER, self.GMAIL_PASSWORD)
                for recipient in recipients:
                    msg = f"Subject: {subject}\nFrom: {self.GMAIL_SENDER}\nTo: {recipient}\n\n{body}"
                    server.sendmail(self.GMAIL_SENDER, recipient, msg)
            messagebox.showinfo("Email Sent", f"Reminder email sent to {len(recipients)} recipients.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send bulk email: {e}")
    
    def schedule_email_reminder(self):
        reminder_window = tk.Toplevel(self)
        reminder_window.title("Schedule Class Reminder Email")
        reminder_window.geometry("400x350")
        
        tk.Label(reminder_window, text="Recipient Email(s):", font=("Arial", 10)).pack(pady=5)
        tk.Label(reminder_window, text="(Enter emails separated by commas or newlines.\nLeave empty for all students)", font=("Arial", 8)).pack()
        text_emails = tk.Text(reminder_window, width=40, height=4)
        text_emails.pack(pady=5)
        
        tk.Label(reminder_window, text="Date (YYYY-MM-DD):").pack(pady=5)
        entry_date = tk.Entry(reminder_window, width=20)
        entry_date.pack(pady=5)
        
        tk.Label(reminder_window, text="Time (HH:MM, 24hr):").pack(pady=5)
        entry_time = tk.Entry(reminder_window, width=20)
        entry_time.pack(pady=5)
        
        tk.Label(reminder_window, text="Subject:").pack(pady=5)
        entry_subject = tk.Entry(reminder_window, width=40)
        entry_subject.insert(0, "Class Reminder")
        entry_subject.pack(pady=5)
        
        tk.Label(reminder_window, text="Message:").pack(pady=5)
        text_message = tk.Text(reminder_window, width=40, height=5)
        text_message.insert("1.0", "This is a reminder that you have a class to attend.")
        text_message.pack(pady=5)
        
        def schedule_action():
            emails_input = text_emails.get("1.0", tk.END).strip()
            recipients = []
            if emails_input:
                for line in emails_input.splitlines():
                    for email in line.split(','):
                        email = email.strip()
                        if email:
                            recipients.append(email)
            date_str = entry_date.get().strip()
            time_str = entry_time.get().strip()
            subject = entry_subject.get().strip()
            body = text_message.get("1.0", tk.END).strip()
            
            if not date_str or not time_str:
                messagebox.showerror("Input Error", "Please fill in the date and time.")
                return
            
            try:
                scheduled_dt = datetime.datetime.strptime(date_str + " " + time_str, "%Y-%m-%d %H:%M")
            except ValueError:
                messagebox.showerror("Format Error", "Please enter date as YYYY-MM-DD and time as HH:MM (24hr).")
                return
            
            now = datetime.datetime.now()
            delay_ms = int((scheduled_dt - now).total_seconds() * 1000)
            if delay_ms < 0:
                messagebox.showerror("Input Error", "The scheduled time is in the past.")
                return
            
            if recipients:
                if len(recipients) == 1:
                    self.after(delay_ms, lambda: self.send_email_reminder(recipients[0], subject, body))
                else:
                    self.after(delay_ms, lambda: self.send_bulk_email_reminder(recipients, subject, body))
                messagebox.showinfo("Scheduled", f"Email reminder scheduled for {scheduled_dt.strftime('%Y-%m-%d %H:%M')} to {len(recipients)} recipient(s).")
            else:
                self.cursor.execute("SELECT email FROM accounts")
                all_recipients = [row[0] for row in self.cursor.fetchall()]
                if not all_recipients:
                    messagebox.showerror("Error", "No student emails found in the database.")
                    return
                self.after(delay_ms, lambda: self.send_bulk_email_reminder(all_recipients, subject, body))
                messagebox.showinfo("Scheduled", f"Bulk email reminder scheduled for {scheduled_dt.strftime('%Y-%m-%d %H:%M')} for {len(all_recipients)} recipients.")
            reminder_window.destroy()
        
        btn_schedule = tk.Button(reminder_window, text="Schedule Reminder", font=("Arial", 12), bg="#4682B4", fg="white", command=schedule_action)
        btn_schedule.pack(pady=10)
    
    # ------------------ UI FRAME CREATION ------------------
    def create_login_frame(self):
        self.login_frame = tk.Frame(self, bg="#E7E7E7")
        mid_frame = tk.Frame(self.login_frame, bg="lightgray", width=400, height=400, relief=tk.SUNKEN, bd=2)
        mid_frame.pack(fill=None, expand=False, padx=50, pady=100)
        mid_frame.pack_propagate(False)
        
        login_label = tk.Label(mid_frame, text="LOG IN", font=("Helvetica", 20, "bold"), bg="lightgray")
        login_label.pack(pady=20)
        
        username_label_log = tk.Label(mid_frame, text="Username:", font=("Arial", 12), bg="lightgray")
        username_label_log.pack(pady=5)
        self.username_entry_log = tk.Entry(mid_frame, font=("Arial", 12), width=30, bd=2)
        self.username_entry_log.pack(pady=10, ipady=5)
        
        password_label_log = tk.Label(mid_frame, text="Password:", font=("Arial", 12), bg="lightgray")
        password_label_log.pack(pady=5)
        self.password_entry_log = tk.Entry(mid_frame, font=("Arial", 12), width=30, show="*", bd=2)
        self.password_entry_log.pack(pady=5, ipady=5)
        
        self.password_checkbox_var_log = tk.BooleanVar()
        password_checkbox_log = tk.Checkbutton(mid_frame, text="Show Password", variable=self.password_checkbox_var_log, 
                                               command=lambda: self.toggle_password(self.password_entry_log, self.password_checkbox_var_log), bg="lightgray")
        password_checkbox_log.pack(pady=5)
        
        login_button = tk.Button(mid_frame, text="Login", font=("Arial", 12), bg="#4682B4", fg="white", command=self.login_professor)
        login_button.pack(pady=10, ipadx=12)
        
        create_account_button = tk.Button(mid_frame, text="Create Account", font=("Arial", 12), bg="#4682B4", fg="white", command=self.switch_to_register)
        create_account_button.pack(pady=10)
    
    def create_register_frame(self):
        self.register_frame = tk.Frame(self, bg="#E7E7E7")
        mid_frame_register = tk.Frame(self.register_frame, bg="lightgray", width=450, height=500, relief=tk.SUNKEN, bd=2)
        mid_frame_register.pack(fill=None, expand=False, padx=50, pady=50)
        mid_frame_register.pack_propagate(False)
        
        register_label = tk.Label(mid_frame_register, text="SIGN UP", font=("Helvetica", 20, "bold"), bg="lightgray")
        register_label.pack(pady=10)
        
        username_label_reg = tk.Label(mid_frame_register, text="Username:", font=("Arial", 12), bg="lightgray")
        username_label_reg.pack(pady=3)
        self.username_entry_reg = tk.Entry(mid_frame_register, font=("Arial", 12), width=30, bd=2)
        self.username_entry_reg.pack(pady=5, ipady=5)
        
        password_label_reg = tk.Label(mid_frame_register, text="Password:", font=("Arial", 12), bg="lightgray")
        password_label_reg.pack(pady=3)
        self.password_entry_reg = tk.Entry(mid_frame_register, font=("Arial", 12), width=30, show="*", bd=2)
        self.password_entry_reg.pack(pady=3, ipady=5)
        
        confirm_password_entry_reg_label = tk.Label(mid_frame_register, text="Confirm Password:", font=("Arial", 12), bg="lightgray")
        confirm_password_entry_reg_label.pack(pady=3)
        self.confirm_password_entry_reg = tk.Entry(mid_frame_register, font=("Arial", 12), width=30, show="*", bd=2)
        self.confirm_password_entry_reg.pack(pady=5, ipady=5)
        
        self.password_checkbox_var_reg = tk.BooleanVar()
        password_checkbox_reg = tk.Checkbutton(mid_frame_register, text="Show Password", variable=self.password_checkbox_var_reg, 
                                               command=self.toggle_password_signup, bg="lightgray")
        password_checkbox_reg.pack(pady=5)
        
        self.fingerprint_status = tk.Label(mid_frame_register, text="Fingerprint Status: Not Scanned", font=("Arial", 10), fg="red")
        self.fingerprint_status.pack(pady=10)
        
        scan_btn = tk.Button(mid_frame_register, text="Scan Fingerprint", font=("Arial", 12), bg="blue", fg="white", command=self.scan_fingerprint)
        scan_btn.pack(pady=5)
        
        register_button = tk.Button(mid_frame_register, text="Register", font=("Arial", 12), bg="#4682B4", fg="white", command=self.register_professor)
        register_button.pack(pady=10)
        
        back_to_login_button = tk.Button(mid_frame_register, text="Back to Login", font=("Arial", 12), bg="#4682B4", fg="white", command=self.go_back_to_login)
        back_to_login_button.pack(pady=10)
    
    def create_dashboard_frame(self):
        self.dashboard_frame = tk.Frame(self, bg="white")
        
        self.left_frame = tk.Frame(self.dashboard_frame, bg="lightgray", width=200, relief=tk.SUNKEN, bd=2)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        self.left_frame.pack_propagate(False)
        self.left_frame.config(height=600)
        
        menu_label = tk.Label(self.left_frame, text="MENU", font=("Helvetica", 18, "bold"), bg="lightgray")
        menu_label.pack(pady=10)
        
        menu_buttons_frame = tk.Frame(self.left_frame, bg="lightgray")
        menu_buttons_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        dashboard_button = tk.Button(menu_buttons_frame, text="DASHBOARD", font=("Arial", 12), bg="white", command=self.show_dashboard_screen)
        dashboard_button.pack(fill="x", pady=10)
        
        records_button = tk.Button(menu_buttons_frame, text="VIEW/ADD RECORDS", font=("Arial", 12), bg="white", command=self.show_records_screen)
        records_button.pack(fill="x", pady=10)
        
        schedule_button = tk.Button(menu_buttons_frame, text="SCHEDULE", font=("Arial", 12), bg="white", command=self.show_schedule_screen)
        schedule_button.pack(fill="x", pady=10)
        
        account_button = tk.Button(menu_buttons_frame, text="ACCOUNT", font=("Arial", 12), bg="white", command=self.show_account_screen)
        account_button.pack(fill="x", pady=10)
        
        logout_button = tk.Button(menu_buttons_frame, text="LOG OUT", font=("Arial", 12), bg="white", command=self.go_back_to_login)
        logout_button.pack(fill="x", pady=10)
        
        self.right_frame = tk.Frame(self.dashboard_frame, bg="lightgray", width=600, relief=tk.SUNKEN, bd=2)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        dashboard_label = tk.Label(self.right_frame, text="DASHBOARD", font=("Helvetica", 18, "bold"), bg="lightgray")
        dashboard_label.pack(pady=10)
    
    def show_login_frame(self):
        self.register_frame.pack_forget()
        self.dashboard_frame.pack_forget()
        self.login_frame.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = AMSApp()
    app.mainloop()

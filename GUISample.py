import tkinter as tk
from tkinter import messagebox
import sqlite3

# Initialize Tkinter root window
root = tk.Tk()
root.title("Professor Registration and Login")
root.geometry("900x600")
root.configure(bg="lightgray")

# Create SQLite connection
conn = sqlite3.connect('professor_student.db')
cursor = conn.cursor()

# Create the students table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS students (
    first_name TEXT,
    middle_name TEXT,
    last_name TEXT,
    suffix TEXT,
    student_number TEXT PRIMARY KEY,
    course TEXT,
    section TEXT,
    year_level TEXT
)''')

# Create the professors table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS professors (
    username TEXT PRIMARY KEY,
    password TEXT
)''')
conn.commit()

# Professor login status
is_professor_logged_in = False

# Function to toggle password visibility
def toggle_password(entry, checkbox_var):
    if checkbox_var.get():
        entry.config(show="")
    else:
        entry.config(show="*")

# Function to show the Dashboard Screen
def show_dashboard():
    login_frame.pack_forget()
    register_frame.pack_forget()
    student_registration_frame.pack_forget()
    dashboard_frame.pack(fill="both", expand=True)

# Function to show student registration form
def show_student_registration():
    global is_professor_logged_in

    if not is_professor_logged_in:
        messagebox.showerror("Access Denied", "You must log in as a professor first.")
        return

    login_frame.pack_forget()
    register_frame.pack_forget()
    dashboard_frame.pack_forget()
    student_registration_frame.pack(fill="both", expand=True)

def register_student():
    student_data = {
        "First Name": first_name_entry.get().strip(),
        "Middle Name (Optional)": middle_name_entry.get().strip(),
        "Last Name": last_name_entry.get().strip(),
        "Suffix (Optional)": suffix_entry.get().strip(),
        "Student Number": student_number_entry.get().strip(),
        "Course": course_entry.get().strip(),
        "Section": section_entry.get().strip(),
        "Year Level": year_level_entry.get().strip()
    }

    for field, value in student_data.items():
        if not value and field != "Middle Name (Optional)" and field != "Suffix (Optional)":
            messagebox.showerror("Input Error", f"{field} cannot be empty.")
            return

    try:
        cursor.execute("""INSERT INTO students (first_name, middle_name, last_name, suffix, student_number, course, section, year_level)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", (
            student_data["First Name"].title(),
            student_data["Middle Name (Optional)"].title() if student_data["Middle Name (Optional)"] else None,
            student_data["Last Name"].title(),
            student_data["Suffix (Optional)"].title() if student_data["Suffix (Optional)"] else None,
            student_data["Student Number"].upper(),
            student_data["Course"].upper(),
            student_data["Section"].upper(),
            student_data["Year Level"].title()
        ))
        conn.commit()
        messagebox.showinfo("Success", "Student registered successfully!")

        first_name_entry.delete(0, tk.END)
        middle_name_entry.delete(0, tk.END)
        last_name_entry.delete(0, tk.END)
        suffix_entry.delete(0, tk.END)
        student_number_entry.delete(0, tk.END)
        course_entry.delete(0, tk.END)
        section_entry.delete(0, tk.END)
        year_level_entry.delete(0, tk.END)
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Student number already registered.")

def register_professor():
    username = username_entry_reg.get().strip()
    password = password_entry_reg.get().strip()

    if not username or not password:
        messagebox.showerror("Input Error", "Please fill in both fields.")
        return

    try:
        cursor.execute("INSERT INTO professors (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        messagebox.showinfo("Success", "Professor registered successfully!")
        username_entry_reg.delete(0, tk.END)
        password_entry_reg.delete(0, tk.END)
        register_frame.pack_forget()
        login_frame.pack(fill="both", expand=True)

    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists.")

def login_professor():
    global is_professor_logged_in
    username = username_entry_log.get().strip()
    password = password_entry_log.get().strip()

    if not username or not password:
        messagebox.showerror("Input Error", "Please fill in both fields.")
        return

    cursor.execute("SELECT * FROM professors WHERE username = ?", (username,))
    professor = cursor.fetchone()

    if professor and professor[1] == password:
        messagebox.showinfo("Success", "Login successful!")
        is_professor_logged_in = True
        show_dashboard()
    else:
        messagebox.showerror("Error", "Invalid username or password.")

# Function to switch to professor registration screen
def switch_to_register():
    login_frame.pack_forget()
    register_frame.pack(fill="both", expand=True)

# Function to go back to login screen
def go_back_to_login():
    global is_professor_logged_in
    is_professor_logged_in = False
    dashboard_frame.pack_forget()
    student_registration_frame.pack_forget()
    login_frame.pack(fill="both", expand=True)

# UI for Registration and Login
frame = tk.Frame(root, bg="lightgray")
frame.place(relx=0.5, rely=0.5, anchor="center")

# Dashboard Screen UI
dashboard_frame = tk.Frame(root, bg="white")

header_frame = tk.Frame(dashboard_frame, bg="#87CEEB", height=50)
header_frame.pack(fill="x")
header_label = tk.Label(header_frame, text="ATTENDANCE MANAGEMENT SYSTEM", font=("Helvetica", 16, "bold"), bg="#87CEEB", fg="white")
header_label.pack(pady=10)

# Left menu frame for buttons
left_frame = tk.Frame(dashboard_frame, bg="lightgray", width=500, relief=tk.SUNKEN, bd=2)
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

register_label = tk.Label(
    left_frame, text="MENU", 
    font=("Helvetica", 18, "bold"), bg="lightgray"
)
register_label.pack(pady=10)
# Add a vertical line on the right side of the menu frame
left_separator = tk.Frame(dashboard_frame, bg="black", width=2)
left_separator.pack(side="left", fill="y")

# Add a container frame for the buttons to center them
menu_buttons_frame = tk.Frame( left_frame, bg="lightgray")
menu_buttons_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center buttons vertically and horizontally

dashboard_button = tk.Button(menu_buttons_frame, text="DASHBOARD", font=("Arial", 12), bg="white", command=show_dashboard)
dashboard_button.pack(fill="x", pady=10)

records_button = tk.Button(menu_buttons_frame, text="VIEW/ADD RECORDS", font=("Arial", 12), bg="white", command=show_student_registration)
records_button.pack(fill="x", pady=10)

schedule_button = tk.Button(menu_buttons_frame, text="SCHEDULE", font=("Arial", 12), bg="white")
schedule_button.pack(fill="x", pady=10)

account_button = tk.Button(menu_buttons_frame, text="ACCOUNT", font=("Arial", 12), bg="white")
account_button.pack(fill="x", pady=10)

logout_button = tk.Button(menu_buttons_frame, text="LOG OUT", font=("Arial", 12), bg="white", command=go_back_to_login)
logout_button.pack(fill="x", pady=10)

# Add a vertical line on the left side of the main content
right_separator = tk.Frame(dashboard_frame, bg="black", width=2)
right_separator.pack(side="right", fill="y")

# Add content to main content frame
content_frame = tk.Frame(dashboard_frame, bg="lightgray", width=700, height=500)
content_frame.pack(side="right", fill="both", expand=True)
content_label = tk.Label(content_frame, text="DASHBOARD", font=("Arial", 18, "bold"), bg="lightgray")
content_label.pack(pady=20)

# Professor Registration UI
register_frame = tk.Frame(frame, bg="lightgray")
register_label = tk.Label(register_frame, text="Professor Registration", font=("Helvetica", 14, "bold"), bg="lightgray")
register_label.pack(pady=10)

username_label_reg = tk.Label(register_frame, text="Username:", font=("Arial", 12), bg="lightgray")
username_label_reg.pack(pady=5)
username_entry_reg = tk.Entry(register_frame, font=("Arial", 12), width=30)
username_entry_reg.pack(pady=5)

password_label_reg = tk.Label(register_frame, text="Password:", font=("Arial", 12), bg="lightgray")
password_label_reg.pack(pady=5)
password_entry_reg = tk.Entry(register_frame, font=("Arial", 12), width=30, show="*")
password_entry_reg.pack(pady=5)

password_checkbox_var_reg = tk.BooleanVar()
password_checkbox_reg = tk.Checkbutton(register_frame, text="Show Password", variable=password_checkbox_var_reg, command=lambda: toggle_password(password_entry_reg, password_checkbox_var_reg), bg="lightgray")
password_checkbox_reg.pack(pady=5)

register_button = tk.Button(register_frame, text="Register", font=("Arial", 12), bg="#4682B4", fg="white", command=register_professor)
register_button.pack(pady=20)

back_to_login_button = tk.Button(register_frame, text="Back to Login", font=("Arial", 12), bg="#4682B4", fg="white", command=go_back_to_login)
back_to_login_button.pack(pady=10)

# Professor Login UI
login_frame = tk.Frame(frame, bg="lightgray")
login_label = tk.Label(login_frame, text="Professor Login", font=("Helvetica", 14, "bold"), bg="lightgray")
login_label.pack(pady=10)

username_label_log = tk.Label(login_frame, text="Username:", font=("Arial", 12), bg="lightgray")
username_label_log.pack(pady=5)
username_entry_log = tk.Entry(login_frame, font=("Arial", 12), width=30)
username_entry_log.pack(pady=5)

password_label_log = tk.Label(login_frame, text="Password:", font=("Arial", 12), bg="lightgray")
password_label_log.pack(pady=5)
password_entry_log = tk.Entry(login_frame, font=("Arial", 12), width=30, show="*")
password_entry_log.pack(pady=5)

password_checkbox_var_log = tk.BooleanVar()
password_checkbox_log = tk.Checkbutton(login_frame, text="Show Password", variable=password_checkbox_var_log, command=lambda: toggle_password(password_entry_log, password_checkbox_var_log), bg="lightgray")
password_checkbox_log.pack(pady=5)

login_button = tk.Button(login_frame, text="Login", font=("Arial", 12), bg="#4682B4", fg="white", command=login_professor)
login_button.pack(pady=20)

create_account_button = tk.Button(login_frame, text="Create Account", font=("Arial", 12), bg="#4682B4", fg="white", command=switch_to_register)
create_account_button.pack(pady=10)

login_frame.pack(fill="both", expand=True)

# Student Registration UI
student_registration_frame = tk.Frame(root, bg="lightgray")

# Add the student registration form
first_name_label = tk.Label(student_registration_frame, text="First Name:", font=("Arial", 12), bg="lightgray")
first_name_label.pack(pady=5)
first_name_entry = tk.Entry(student_registration_frame, font=("Arial", 12), width=30)
first_name_entry.pack(pady=5)

middle_name_label = tk.Label(student_registration_frame, text="Middle Name (Optional):", font=("Arial", 12), bg="lightgray")
middle_name_label.pack(pady=5)
middle_name_entry = tk.Entry(student_registration_frame, font=("Arial", 12), width=30)
middle_name_entry.pack(pady=5)

last_name_label = tk.Label(student_registration_frame, text="Last Name:", font=("Arial", 12), bg="lightgray")
last_name_label.pack(pady=5)
last_name_entry = tk.Entry(student_registration_frame, font=("Arial", 12), width=30)
last_name_entry.pack(pady=5)

suffix_label = tk.Label(student_registration_frame, text="Suffix (Optional):", font=("Arial", 12), bg="lightgray")
suffix_label.pack(pady=5)
suffix_entry = tk.Entry(student_registration_frame, font=("Arial", 12), width=30)
suffix_entry.pack(pady=5)

student_number_label = tk.Label(student_registration_frame, text="Student Number:", font=("Arial", 12), bg="lightgray")
student_number_label.pack(pady=5)
student_number_entry = tk.Entry(student_registration_frame, font=("Arial", 12), width=30)
student_number_entry.pack(pady=5)

course_label = tk.Label(student_registration_frame, text="Course:", font=("Arial", 12), bg="lightgray")
course_label.pack(pady=5)
course_entry = tk.Entry(student_registration_frame, font=("Arial", 12), width=30)
course_entry.pack(pady=5)

section_label = tk.Label(student_registration_frame, text="Section:", font=("Arial", 12), bg="lightgray")
section_label.pack(pady=5)
section_entry = tk.Entry(student_registration_frame, font=("Arial", 12), width=30)
section_entry.pack(pady=5)

year_level_label = tk.Label(student_registration_frame, text="Year Level:", font=("Arial", 12), bg="lightgray")
year_level_label.pack(pady=5)
year_level_entry = tk.Entry(student_registration_frame, font=("Arial", 12), width=30)
year_level_entry.pack(pady=5)

register_student_button = tk.Button(student_registration_frame, text="Register Student", font=("Arial", 12), bg="#4682B4", fg="white", command=register_student)
register_student_button.pack(pady=20)

back_to_dashboard_button = tk.Button(student_registration_frame, text="Back to Dashboard", font=("Arial", 12), bg="#4682B4", fg="white", command=show_dashboard)
back_to_dashboard_button.pack(pady=10)

# Run the Tkinter main loop
root.mainloop()

import tkinter as tk
from tkinter import messagebox
import sqlite3

# Initialize Tkinter root window
root = tk.Tk()
root.title("AMS")
root.geometry("1000x600")  # Set fixed size
root.resizable(False, False) 
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
    dashboard_frame.pack(fill="both", expand=True)
    #student_registration_frame.pack_forget()
    
'''
# Function to show student registration form
def show_student_registration():
    global is_professor_logged_in

    if not is_professor_logged_in:
        messagebox.showerror("Access Denied", "You must log in as a professor first.")
        return

    login_frame.pack_forget()
    register_frame.pack_forget()
    dashboard_frame.pack_forget()
    #student_registration_frame.pack(fill="both", expand=True)
    
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
'''
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
    #student_registration_frame.pack_forget()
    register_frame.pack_forget()
    login_frame.pack(fill="both", expand=True)

# UI for Registration and Login
frame = tk.Frame(root, bg="lightgray")
frame.place(relx=0.5, rely=0.5, anchor="center")

# Dashboard Screen UI
dashboard_frame = tk.Frame(root, bg="white")

title_label = tk.Label(
    root, text="ATTENDANCE MANAGEMENT SYSTEM", 
    font=("Helvetica", 24, "bold"), 
    bg="#4682B4", fg="white", 
    pady=10
)
title_label.pack(fill=tk.X)


left_frame = tk.Frame(dashboard_frame, bg="lightgray", width=200, relief=tk.SUNKEN, bd=2)
left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
left_frame.pack_propagate(False)  # Prevent resizing to fit contents
left_frame.config(height=600)

menu_label = tk.Label(
    left_frame, text="MENU", 
    font=("Helvetica", 18, "bold"), bg="lightgray"
)
menu_label.pack(pady=10)

# Add a container frame for the buttons to center them
menu_buttons_frame = tk.Frame( left_frame, bg="lightgray")
menu_buttons_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center buttons vertically and horizontally

dashboard_button = tk.Button(menu_buttons_frame, text="DASHBOARD", font=("Arial", 12), bg="white", command=show_dashboard)
dashboard_button.pack(fill="x", pady=10)

records_button = tk.Button(menu_buttons_frame, text="VIEW/ADD RECORDS", font=("Arial", 12), bg="white")
records_button.pack(fill="x", pady=10)

schedule_button = tk.Button(menu_buttons_frame, text="SCHEDULE", font=("Arial", 12), bg="white")
schedule_button.pack(fill="x", pady=10)

account_button = tk.Button(menu_buttons_frame, text="ACCOUNT", font=("Arial", 12), bg="white")
account_button.pack(fill="x", pady=10)

logout_button = tk.Button(menu_buttons_frame, text="LOG OUT", font=("Arial", 12), bg="white", command=go_back_to_login)
logout_button.pack(fill="x", pady=10)

# Add a vertical line on the left side of the main content
right_frame = tk.Frame(dashboard_frame, bg="lightgray", width=600, relief=tk.SUNKEN, bd=2)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

dashboard_label = tk.Label(
    right_frame, text="DASHBOARD", 
    font=("Helvetica", 18, "bold"), bg="lightgray"
)
dashboard_label.pack(pady=10)

# Professor Registration UI
register_frame = tk.Frame(root, bg="#E7E7E7")

mid_frame_register = tk.Frame(register_frame, bg="lightgray", width=400, height=400, relief=tk.SUNKEN, bd=2)
mid_frame_register.pack(fill=None, expand=False, padx=50, pady=50)
mid_frame_register.pack_propagate(False)

register_label = tk.Label(mid_frame_register, text="SIGN UP", font=("Helvetica", 20, "bold"), bg="lightgray")
register_label.pack(pady=20)

username_label_reg = tk.Label(mid_frame_register, text="Username:", font=("Arial", 12), bg="lightgray")
username_label_reg.pack(pady=5)
username_entry_reg = tk.Entry(mid_frame_register, font=("Arial", 12), width=30, bd=2)

username_entry_reg.pack(pady=10, ipady=5)

password_label_reg = tk.Label(mid_frame_register, text="Password:", font=("Arial", 12), bg="lightgray")
password_label_reg.pack(pady=5)
password_entry_reg = tk.Entry(mid_frame_register, font=("Arial", 12), width=30, show="*", bd=2)
password_entry_reg.pack(pady=5, ipady=5)

password_checkbox_var_reg = tk.BooleanVar()
password_checkbox_reg = tk.Checkbutton(mid_frame_register, text="Show Password", variable=password_checkbox_var_reg, command=lambda: toggle_password(password_entry_reg, password_checkbox_var_reg), bg="lightgray")
password_checkbox_reg.pack(pady=5)

register_button = tk.Button(mid_frame_register, text="Register", font=("Arial", 12), bg="#4682B4", fg="white", command=register_professor)
register_button.pack(pady=10)

back_to_login_button = tk.Button(mid_frame_register, text="Back to Login", font=("Arial", 12), bg="#4682B4", fg="white", command=go_back_to_login)
back_to_login_button.pack(pady=10)

# Professor Login UI
login_frame = tk.Frame(root,  bg="#E7E7E7")

mid_frame = tk.Frame(login_frame, bg="lightgray", width=400, height=400, relief=tk.SUNKEN, bd=2)
mid_frame.pack(fill=None, expand=False, padx=50, pady=50)
mid_frame.pack_propagate(False)

login_label = tk.Label(mid_frame, text="LOG IN", font=("Helvetica", 20, "bold"), bg="lightgray")
login_label.pack(pady=20)

username_label_log = tk.Label(mid_frame, text="Username:", font=("Arial", 12), bg="lightgray")
username_label_log.pack(pady=5)
username_entry_log = tk.Entry(mid_frame, font=("Arial", 12), width=30, bd=2)
username_entry_log.pack(pady=10, ipady=5)

password_label_log = tk.Label(mid_frame, text="Password:", font=("Arial", 12), bg="lightgray")
password_label_log.pack(pady=5)
password_entry_log = tk.Entry(mid_frame, font=("Arial", 12), width=30, show="*", bd=2)
password_entry_log.pack(pady=5, ipady=5)

password_checkbox_var_log = tk.BooleanVar()
password_checkbox_log = tk.Checkbutton(mid_frame, text="Show Password", variable=password_checkbox_var_log, command=lambda: toggle_password(password_entry_log, password_checkbox_var_log), bg="lightgray")
password_checkbox_log.pack(pady=5)

login_button = tk.Button(mid_frame, text="Login", font=("Arial", 12), bg="#4682B4", fg="white", command=login_professor)
login_button.pack(pady=10, ipadx=12)

create_account_button = tk.Button(mid_frame, text="Create Account", font=("Arial", 12), bg="#4682B4", fg="white", command=switch_to_register)
create_account_button.pack(pady=10)

login_frame.pack(fill="both", expand=True)

'''
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
'''
def show_dashboard_screen():
    clear_right_frame()
    dashboard_label = tk.Label(
        right_frame, text="DASHBOARD", 
        font=("Helvetica", 18, "bold"), bg="#4682B4"
        
    )
    dashboard_label.pack(pady=10)
    first_text_label = tk.Label(
        right_frame, 
        text="ALAM MO BA GIRL, HINDI KO MAINTINDIHAN ANG NARARAMDAMAN", 
        font=("Helvetica", 20), 
        bg="lightgray", 
        wraplength=400
    )
    first_text_label.pack(anchor="w", padx=10, pady=10)
def show_records_screen():
    clear_right_frame()
    records_label_frame = tk.Frame(
        right_frame, bg="black", 
        padx=10, pady=10, 
    )
    records_label_frame.pack(pady=8) 
    records_label = tk.Label(
        right_frame, text="VIEW/ADD RECORDS", 
        font=("Helvetica", 20, "bold"), bg="#91BDF5",
        padx=15, pady=15
    )
    
    records_label.pack(pady=10)
    second_text_label = tk.Label(
        right_frame, 
        text="COURSES", 
        font=("Helvetica", 20), 
        bg="lightgray", 
        wraplength=400,
        
    )
    second_text_label.pack(anchor="w", padx=5, pady=10)
    
    bsit_button = tk.Button(right_frame, text="BACHELOR OF SCIENCE IN INFORMATION TECHNOLOGY", font=("Arial", 14), bg="#4682B4", fg="white", command=yearlevel_and_section_frame)
    bsit_button.pack(pady=10, ipadx=5, ipady=21)
    bscs_button = tk.Button(right_frame, text=" BACHELOR OF SCIENCE IN COMPUTER SCIENCE ", font=("Arial", 14), bg="#4682B4", fg="white", command="")
    bscs_button.pack(pady=10, ipadx=38, ipady=20)
    
    add_course_button = tk.Button(right_frame, text="BACHELOR OF SCIENCE IN INFORMATION SYSTEM", font=("Arial", 14), bg="#4682B4", fg="white", command="")
    add_course_button.pack(pady=10, ipadx=36, ipady=20)    
    
def on_mouse_wheel(event, canvas):
    canvas.yview_scroll(-1 * (event.delta // 120), "units")

def yearlevel_and_section_frame():
    clear_right_frame()
    
    yearlevel_label = tk.Label(
        right_frame, text="VIEW/ADD RECORDS", 
        font=("Helvetica", 18, "bold"), bg="#4682B4"
    )
    yearlevel_label.pack(pady=10)

    # Scrollable frame
    canvas = tk.Canvas(right_frame, width=800, height=460)
    scrollbar = tk.Scrollbar(right_frame, orient="vertical", command=canvas.yview)
    
    scroll_frame = tk.Frame(canvas, bg="lightgray")

    scroll_frame.bind(
        "<Configure>", 
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Bind scroll event for mouse wheel
    canvas.bind_all("<MouseWheel>", lambda event: on_mouse_wheel(event, canvas))

    # Dictionary with sections for each year level
    section_names = {
        1: ["LFCA111M010", "LFCA322M011"],
        2: ["LFCA211M025", "LFCA211A005"],
        3: ["LFCA311M045", "LFCA311M046"],
        4: ["LFCA411M055", "LFCA411M056"]  # Placeholder for 4th year, update as needed
    }

    # Add year level sections inside scrollable frame
    for year in range(1, 5):  # 1st to 4th Year
        year_frame = tk.Frame(scroll_frame, bg="lightgray", width=750, height=230, relief=tk.SUNKEN, bd=2)
        year_frame.pack(fill=tk.X, padx=10, pady=10)
        year_frame.pack_propagate(False)
        
        year_label = tk.Label(
            year_frame, 
            text=f"{year}ST YEAR" if year == 1 else f"{year}ND YEAR" if year == 2 else f"{year}RD YEAR" if year == 3 else "4TH YEAR", 
            font=("Helvetica", 15, "bold"), fg="white",
            bg="gray", 
            wraplength=400,
        )
        year_label.pack(anchor="w", padx=5, pady=10)

        # Add section buttons dynamically
        for section in section_names.get(year, []):  
            section_button = tk.Button(year_frame, text=section, font=("Arial", 14), bg="#4682B4", fg="white", command="")
            section_button.pack(pady=5, ipadx=200, ipady=5)
        
        add_section_button = tk.Button(year_frame, text="ADD SECTION (+)", font=("Arial", 14), bg="#4682B4", fg="white", command="")
        add_section_button.pack(pady=5, ipadx=190, ipady=5)  
   
''' 
    courses_text_label = tk.Label(
        right_frame, 
        text="BACHELOR OF SCIENCE INFORMATION TECHNOLOGY", 
        font=("Helvetica", 20), 
        bg="#0d98ba", 
        wraplength=400,
        
    )
    courses_text_label.pack(pady=10)
'''
def show_schedule_screen():
    clear_right_frame()
    schedule_label = tk.Label(
        right_frame, text="SCHEDULE", 
        font=("Helvetica", 18, "bold"), bg="lightgray"
    )
    schedule_label.pack(pady=10)
    third_text_label = tk.Label(
        right_frame, 
        text="NAWAWALA YUNG ANGAS AT ASTA MONG MALABAN", 
        font=("Helvetica", 20), 
        bg="lightgray", 
        wraplength=400
    )
    third_text_label.pack(anchor="w", padx=10, pady=10)
def show_account_screen():
    clear_right_frame()
    account_label = tk.Label(
        right_frame, text="ACCOUNT", 
        font=("Helvetica", 18, "bold"), bg="lightgray"
    )
    account_label.pack(pady=10)
    fourth_text_label = tk.Label(
        right_frame, 
        text="TANGGAL ANG KULIT AMAT UMANGAT NA NAMAN", 
        font=("Helvetica", 20), 
        bg="lightgray", 
        wraplength=400
    )
    fourth_text_label.pack(anchor="w", padx=10, pady=10)

def clear_right_frame():
    for widget in right_frame.winfo_children():
        widget.destroy()

# Update button commands in the left menu
dashboard_button.config(command=show_dashboard_screen)
records_button.config(command=show_records_screen)
schedule_button.config(command=show_schedule_screen)
account_button.config(command=show_account_screen)
logout_button.config(command=go_back_to_login)

# Show initial Dashboard screen by default
show_dashboard_screen()

# Run the Tkinter main loop
root.mainloop()

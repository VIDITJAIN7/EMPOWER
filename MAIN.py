from pymysql import *
import tkinter as tk
from tkinter import Tk, messagebox
from tkinter import ttk, simpledialog
from tkinter import *

try:
    con1 = connect(host='localhost', user='root', password='viditjain', database='empower')
    cur1 = con1.cursor()

    def db_empower():
        # Create empmaster table
        cur1.execute('''
            CREATE TABLE IF NOT EXISTS empmaster (
                empid INT PRIMARY KEY,
                name VARCHAR(50),
                gender CHAR(1),
                doj DATE,
                aadhar INT,
                deptid INT,
                desgn VARCHAR(40),
                salary NUMERIC(7, 2),
                contact INT
            );
        ''')
        # Create sal_structure table
        cur1.execute('''
            CREATE TABLE IF NOT EXISTS sal_structure (
                empid INT,
                basic_sal NUMERIC(7, 2),
                allowances NUMERIC(7, 2),
                provident_fund NUMERIC(7, 2),
                tds NUMERIC(7, 2),
                FOREIGN KEY (empid) REFERENCES empmaster(empid)
            );
        ''')
        # Create dept table
        cur1.execute('''
            CREATE TABLE IF NOT EXISTS dept (
                deptid INT PRIMARY KEY,
                dept_name VARCHAR(40),
                dept_head INT
            );
        ''')
        # Add foreign key constraint to empmaster for deptid
        cur1.execute('''
            ALTER TABLE empmaster
            ADD CONSTRAINT FOREIGN KEY (deptid) REFERENCES dept(deptid);
        ''')
        # Add departments to the dept table
        department_data = [
            (0, 'admin', 1),
            (1, 'HR', 2),
            (2, 'sales', 3),
            (3, 'IT', 4),
            (4, 'unassigned', None)
        ]

        cur1.executemany('INSERT IGNORE INTO dept (deptid, dept_name, dept_head) VALUES (%s, %s, %s)', department_data)

        con1.commit()

    db_empower()

except MySQLError as e:
    print(e)

def open_admin_login_window():
    password = simpledialog.askstring("Admin Login", "Enter Admin Password:", show='*')
    if password == '1234abcd':
        admin_login_window = tk.Toplevel(main_window)
        admin_login_window.title('Admin Control Panel')
        admin_login_window.geometry('400x300')
        admin_login_window.configure(bg='#2e2e2e')  

        add_button = ttk.Button(admin_login_window, text='ADD', command=emp_add)
        add_button.pack(pady=10)

        delete_button = ttk.Button(admin_login_window, text='DELETE', command=emp_delete)
        delete_button.pack(pady=10)

        update_button = ttk.Button(admin_login_window, text='UPDATE', command=emp_update)
        update_button.pack(pady=10)

        filter_button = ttk.Button(admin_login_window, text='FILTER', command=emp_filter)
        filter_button.pack(pady=10)
    else:
        messagebox.showerror("Error", "Incorrect password. Access denied.")

def emp_add():
    def addrec_empmaster():
        empid = entry_empid.get()
        name = entry_name.get()
        gender = gender_var.get()
        doj = entry_doj.get()
        aadhar = entry_aadhar.get()
        selected_dept_name = combo_dept.get()
        deptid = departments[selected_dept_name]
        desgn = entry_desgn.get()
        salary = entry_salary.get()
        contact = entry_contact.get()

        try:
            cur1.execute(
                "INSERT INTO empmaster (empid, name, gender, doj, aadhar, deptid, desgn, salary, contact) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (empid, name, gender, doj, aadhar, deptid, desgn, salary, contact))
            con1.commit()
            messagebox.showinfo("Success", "Employee added successfully!")
            root.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error occurred: {str(e)}")
            con1.rollback()

    def save_changes():
        try:
            con1.commit()
            messagebox.showinfo("Success", "Changes saved successfully!")
            root.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error occurred: {str(e)}")

    def discard_changes():
        con1.rollback()
        messagebox.showinfo("Info", "Changes discarded.")
        root.destroy()
    # GUI Setup
    root = tk.Tk()
    root.title("Add Employee")
    root.configure(bg='#2e2e2e')  

    label_empid = ttk.Label(root, text="Employee ID:", foreground="white", background="#2e2e2e")
    label_empid.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

    entry_empid = ttk.Entry(root)
    entry_empid.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

    label_name = ttk.Label(root, text="Employee Name:", foreground="white", background="#2e2e2e")
    label_name.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

    entry_name = ttk.Entry(root)
    entry_name.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

    label_gender = ttk.Label(root, text="Gender:", foreground="white", background="#2e2e2e")
    label_gender.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

    gender_var = tk.StringVar()
    gender_var.set("M")

    radio_male = ttk.Radiobutton(root, text="Male", variable=gender_var, value="M", style="TRadiobutton")
    radio_male.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

    radio_female = ttk.Radiobutton(root, text="Female", variable=gender_var, value="F", style="TRadiobutton")
    radio_female.grid(row=2, column=2, padx=5, pady=5, sticky=tk.W)

    radio_other = ttk.Radiobutton(root, text="Other", variable=gender_var, value="O", style="TRadiobutton")
    radio_other.grid(row=2, column=3, padx=5, pady=5, sticky=tk.W)

    label_doj = ttk.Label(root, text="Date of Joining (YYYY-MM-DD):", foreground="white", background="#2e2e2e")
    label_doj.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)

    entry_doj = ttk.Entry(root)
    entry_doj.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

    label_aadhar = ttk.Label(root, text="Aadhar Card No.:", foreground="white", background="#2e2e2e")
    label_aadhar.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)

    entry_aadhar = ttk.Entry(root)
    entry_aadhar.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)

    label_dept = ttk.Label(root, text="Department:", foreground="white", background="#2e2e2e")
    label_dept.grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)

    departments = {"Admin": 0, "HR": 1, "Sales": 2, "IT": 3, "Unassigned": 4}
    dept_var = tk.StringVar()
    dept_var.set("Admin")

    combo_dept = ttk.Combobox(root, values=list(departments.keys()), textvariable=dept_var)
    combo_dept.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)

    label_desgn = ttk.Label(root, text="Current Designation:", foreground="white", background="#2e2e2e")
    label_desgn.grid(row=6, column=0, padx=5, pady=5, sticky=tk.W)

    entry_desgn = ttk.Entry(root)
    entry_desgn.grid(row=6, column=1, padx=5, pady=5, sticky=tk.W)

    label_salary = ttk.Label(root, text="Current Salary:", foreground="white", background="#2e2e2e")
    label_salary.grid(row=7, column=0, padx=5, pady=5, sticky=tk.W)

    entry_salary = ttk.Entry(root)
    entry_salary.grid(row=7, column=1, padx=5, pady=5, sticky=tk.W)

    label_contact = ttk.Label(root, text="Contact No.:", foreground="white", background="#2e2e2e")
    label_contact.grid(row=8, column=0, padx=5, pady=5, sticky=tk.W)

    entry_contact = ttk.Entry(root)
    entry_contact.grid(row=8, column=1, padx=5, pady=5, sticky=tk.W)

    button_add = ttk.Button(root, text="Add Employee", command=addrec_empmaster, style="TButton")
    button_add.grid(row=9, column=0, padx=5, pady=5, sticky=tk.W)

    button_save = ttk.Button(root, text="Save Changes", command=save_changes, style="TButton")
    button_save.grid(row=9, column=1, padx=5, pady=5, sticky=tk.W)

    button_discard = ttk.Button(root, text="Discard Changes", command=discard_changes, style="TButton")
    button_discard.grid(row=9, column=2, padx=5, pady=5, sticky=tk.W)

    root.mainloop()

def emp_delete():
    def delrec_empmaster():
        empid = entry_empid.get()

        try:
            cur1.execute('DELETE FROM empmaster WHERE empid = %s', (empid,))
            messagebox.showinfo("Success", "Record deleted successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error occurred: {str(e)}")

    def save_changes():
        try:
            con1.commit()
            messagebox.showinfo("Success", "Changes saved successfully!")
            root.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error occurred: {str(e)}")

    def discard_changes():
        con1.rollback()
        messagebox.showinfo("Info", "Changes discarded.")
        root.destroy()

    # GUI Setup
    root = tk.Tk()
    root.title("Delete Employee Record")
    root.configure(bg='#2e2e2e')  

    label_empid = ttk.Label(root, text="Enter Employee ID to delete:", foreground="white", background="#2e2e2e")
    label_empid.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

    entry_empid = ttk.Entry(root)
    entry_empid.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

    button_delete = ttk.Button(root, text="Delete Record", command=delrec_empmaster, style="TButton")
    button_delete.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W)

    button_save = ttk.Button(root, text="Save Changes", command=save_changes, style="TButton")
    button_save.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

    button_discard = ttk.Button(root, text="Discard Changes", command=discard_changes, style="TButton")
    button_discard.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

    root.mainloop()

def emp_update():
    def updaterec_emp():
        employee_id = entry_empid.get()
        field_to_update = field_combobox.get()
        updated_value = entry_value.get()

        update_query = f'UPDATE empmaster SET {field_to_update} = %s WHERE empid = %s'
        cur1.execute(update_query, (updated_value, employee_id))

    def save_changes():
        con1.commit()
        root.destroy()

    def discard_changes():
        con1.rollback()
        root.destroy()

    root = tk.Tk()
    root.title("Employee Record Updater")
    root.configure(bg='#2e2e2e')  

    label_empid = ttk.Label(root, text="Employee ID:", foreground="white", background="#2e2e2e")
    label_empid.grid(row=0, column=0, padx=5, pady=5)
    entry_empid = ttk.Entry(root)
    entry_empid.grid(row=0, column=1, padx=5, pady=5)

    label_field = ttk.Label(root, text="Field to update:", foreground="white", background="#2e2e2e")
    label_field.grid(row=1, column=0, padx=5, pady=5)
    fields = ['empid', 'name', 'gender', 'doj', 'aadhar', 'deptid', 'desgn', 'salary', 'contact']
    field_combobox = ttk.Combobox(root, values=fields)
    field_combobox.grid(row=1, column=1, padx=5, pady=5)

    label_value = ttk.Label(root, text="Updated value:", foreground="white", background="#2e2e2e")
    label_value.grid(row=2, column=0, padx=5, pady=5)
    entry_value = ttk.Entry(root)
    entry_value.grid(row=2, column=1, padx=5, pady=5)

    button_update = ttk.Button(root, text="Update Record", command=updaterec_emp, style="TButton")
    button_update.grid(row=3, column=0, columnspan=2, pady=10)

    button_save_changes = ttk.Button(root, text="Save Changes", command=save_changes, style="TButton")
    button_save_changes.grid(row=4, column=0, pady=10)

    button_discard_changes = ttk.Button(root, text="Discard Changes", command=discard_changes, style="TButton")
    button_discard_changes.grid(row=4, column=1, pady=10)

    root.mainloop()

def emp_filter():
    def search_emp():
        field_to_search = combo_field.get()
        term_to_search = entry_term.get()

        search_query = 'SELECT * FROM empmaster WHERE {} = %s'.format(field_to_search)
        cur1.execute(search_query, (term_to_search,))
        result = cur1.fetchall()

        for row in tree.get_children():
            tree.delete(row)

        if result:
            for row in result:
                tree.insert('', 'end', values=row)
        else:
            tree.insert('', 'end', values=("No results found.",))

    # GUI Setup
    root = tk.Tk()
    root.title("Employee Search")
    root.configure(bg='#2e2e2e')  

    label_field = ttk.Label(root, text="Select field to filter by:", foreground="white", background="#2e2e2e")
    label_field.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

    fields = ("empid", "name", "gender", "doj", "aadhar", "deptid", "desgn", "salary", "contact")
    combo_field = ttk.Combobox(root, values=fields)
    combo_field.set(fields[0])
    combo_field.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

    label_term = ttk.Label(root, text="Enter term to search:", foreground="white", background="#2e2e2e")
    label_term.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

    entry_term = ttk.Entry(root)
    entry_term.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

    button_search = ttk.Button(root, text="Search", command=search_emp, style="TButton")
    button_search.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)

    columns = ("Emp ID", "Name", "Gender", "DOJ", "Aadhar", "Dept ID", "Designation", "Salary", "Contact")
    tree = ttk.Treeview(root, columns=columns, show="headings", height=10)

    for col in columns:
        tree.heading(col, text=col)

    tree.grid(row=2, column=0, columnspan=3, pady=10, sticky="nsew")

    root.grid_rowconfigure(2, weight=1)
    root.grid_columnconfigure(0, weight=1)

    root.mainloop()

def emp_report():
    def reportgenerator_emp():
        term_to_search = entry_search.get()
        search_query = 'SELECT * FROM empmaster WHERE empid = %s'
        cur1.execute(search_query, (term_to_search,))
        result = cur1.fetchall()

        for row in tree.get_children():
            tree.delete(row)

        if result:
            for row in result:
                tree.insert('', 'end', values=row)
        else:
            tree.insert('', 'end', values=("No results found.",))

    # GUI Setup
    root = tk.Tk()
    root.title("Employee Report Generator")
    root.configure(bg="#2e2e2e")

    style = ttk.Style()
    style.configure("TButton", foreground="#2e2e2e", background="#2e2e2e")

    label_search = ttk.Label(root, text="Enter term to search:", foreground="white", background="#2e2e2e")
    label_search.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

    entry_search = ttk.Entry(root)
    entry_search.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

    button_generate_report = ttk.Button(root, text="Generate Report", command=reportgenerator_emp, style="TButton")
    button_generate_report.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)

    columns = ("Emp ID", "Name", "Gender", "DOJ", "Aadhar", "Dept ID", "Designation", "Salary", "Contact")
    tree = ttk.Treeview(root, columns=columns, show="headings", height=5)

    for col in columns:
        tree.heading(col, text=col)

    tree.grid(row=1, column=0, columnspan=3, pady=10, sticky="nsew")
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)

    root.mainloop()

# MAIN WINDOW GUI
def on_radio_button_selected():
    selected_option = radio_var.get()
    if selected_option == 1:
        open_admin_login_window()
    elif selected_option == 2:
        emp_report()

# Main Window Configuration
main_window = Tk()
main_window.title('Employee Management System')
main_window.geometry("400x200")
main_window.resizable(False, False)
main_window.configure(bg='#2e2e2e')

label_prompt = Label(main_window, text="Choose your login option", fg='white', bg='#2e2e2e')
label_prompt.pack(pady=10)

radio_var = IntVar()

admin_radio = Radiobutton(main_window, text='Admin', variable=radio_var, value=1, command=on_radio_button_selected, bg='#2e2e2e', fg='white')
admin_radio.pack(side='left', padx=10, pady=10)

employee_radio = Radiobutton(main_window, text='Employee', variable=radio_var, value=2, command=on_radio_button_selected, bg='#2e2e2e', fg='white')
employee_radio.pack(side='right', padx=10, pady=10)

main_window.mainloop()


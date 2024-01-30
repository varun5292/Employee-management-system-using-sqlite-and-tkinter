import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import deque


class EmployeeManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Management System")

        self.conn = sqlite3.connect('employee_database.db')
        self.cursor = self.conn.cursor()
        self.create_table()

        self.create_gui()
      
        self.undo_stack = deque(maxlen=10)
        self.redo_stack = deque(maxlen=10)

    def create_table(self):
        self.cursor.execute('''
            DROP TABLE IF EXISTS employees
        ''')
        self.conn.commit()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                contact_number TEXT NOT NULL,
                gmail TEXT NOT NULL,
                gender TEXT NOT NULL,
                role TEXT NOT NULL,
                experience INTEGER NOT NULL,
                salary INTEGER NOT NULL
            )
        ''')
        self.conn.commit()

    def create_gui(self):

        self.label_name = tk.Label(self.root, text="Name:")
        self.entry_name = tk.Entry(self.root)

        self.label_age = tk.Label(self.root, text="Age:")
        self.entry_age = tk.Entry(self.root)

        self.label_contact_number = tk.Label(self.root, text="Contact Number:")
        self.entry_contact_number = tk.Entry(self.root)

        self.label_gmail = tk.Label(self.root, text="Gmail:")
        self.entry_gmail = tk.Entry(self.root)

        self.label_gender = tk.Label(self.root, text="Gender:")
        self.gender_var = tk.StringVar()
        self.gender_combobox = ttk.Combobox(self.root, textvariable=self.gender_var, values=['Male', 'Female'])

        self.label_role = tk.Label(self.root, text="Role:")
        self.role_var = tk.StringVar()
        self.role_combobox = ttk.Combobox(self.root, textvariable=self.role_var,
                                      values=['Computer Programmer', 'Network Administrator', 'Web Developer',
                                              'System Analyst', 'Quality Assurance Engineer', 'Database Administrator',
                                              'PHP Developer', 'Software Test Engineer', 'Security Engineer',
                                              'Java Developer', 'Hardware Engineer', 'Front-End Developer',
                                              'Full Stack Developer', 'Python Developer', 'Mobile Developer',
                                              'Back-End Developer', 'Development Operations Engineer',
                                              'Chief Technology Officer', 'Software Architect'])

        self.label_experience = tk.Label(self.root, text="Experience:")
        self.entry_experience = tk.Entry(self.root)

        self.label_salary = tk.Label(self.root, text="Salary:")
        self.entry_salary = tk.Entry(self.root, state='readonly')

        self.label_leaves = tk.Label(self.root, text="Leaves Taken:")
        self.entry_leaves = tk.Entry(self.root)

        self.button_add = tk.Button(self.root, text="Add Employee", command=self.add_employee)
        self.button_update = tk.Button(self.root, text="Update Employee", command=self.update_employee)
        self.button_remove = tk.Button(self.root, text="Remove Employee", command=self.remove_employee)
        self.button_show_table = tk.Button(self.root, text="Show Employees", command=self.show_table)
        self.button_promote = tk.Button(self.root, text="Promote Employee", command=self.promote_employee)
        self.label_search = tk.Label(self.root, text="Search:")
        self.entry_search = tk.Entry(self.root)
        self.button_search = tk.Button(self.root, text="Search", command=self.search_employee)
        self.button_promote.grid(row=13, column=0, columnspan=2, pady=10)
        self.button_promote.grid_remove() 

        self.tree = ttk.Treeview(self.root, columns=("ID", "Name", "Age", "Contact Number", "Gmail", "Gender", "Role", "Experience", "Salary"), show="headings")

        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Age", text="Age")
        self.tree.heading("Contact Number", text="Contact Number")
        self.tree.heading("Gmail", text="Gmail")
        self.tree.heading("Gender", text="Gender")
        self.tree.heading("Role", text="Role")
        self.tree.heading("Experience", text="Experience")
        self.tree.heading("Salary", text="Salary")
        column_width = 100
        for col in ("ID", "Name", "Age", "Contact Number", "Gmail", "Gender", "Role", "Experience", "Salary"):
            self.tree.column(col, width=column_width, anchor=tk.CENTER)

        self.label_name.grid(row=0, column=0, padx=10, pady=10, sticky=tk.E)
        self.entry_name.grid(row=0, column=1, padx=10, pady=10)

        self.label_age.grid(row=1, column=0, padx=10, pady=10, sticky=tk.E)
        self.entry_age.grid(row=1, column=1, padx=10, pady=10)

        self.label_contact_number.grid(row=2, column=0, padx=10, pady=10, sticky=tk.E)
        self.entry_contact_number.grid(row=2, column=1, padx=10, pady=10)

        self.label_gmail.grid(row=3, column=0, padx=10, pady=10, sticky=tk.E)
        self.entry_gmail.grid(row=3, column=1, padx=10, pady=10)

        self.label_gender.grid(row=4, column=0, padx=10, pady=10, sticky=tk.E)
        self.gender_combobox.grid(row=4, column=1, padx=10, pady=10)

        self.label_role.grid(row=5, column=0, padx=10, pady=10, sticky=tk.E)
        self.role_combobox.grid(row=5, column=1, padx=10, pady=10)

        self.label_experience.grid(row=6, column=0, padx=10, pady=10, sticky=tk.E)
        self.entry_experience.grid(row=6, column=1, padx=10, pady=10)

        self.label_salary.grid(row=7, column=0, padx=10, pady=10, sticky=tk.E)
        self.entry_salary.grid(row=7, column=1, padx=10, pady=10)

        self.label_leaves.grid(row=8, column=0, padx=10, pady=10, sticky=tk.E)
        self.entry_leaves.grid(row=8, column=1, padx=10, pady=10)

        self.label_leaves.grid_remove()
        self.entry_leaves.grid_remove()

        self.button_add.grid(row=11, column=0, columnspan=2, pady=10)
        self.button_update.grid(row=12, column=0, columnspan=2, pady=10)
        self.button_remove.grid(row=14, column=0, columnspan=2, pady=10)

        self.tree.grid(row=0, column=2, rowspan=13, padx=10, pady=10)

        self.label_search.grid(row=9, column=0, padx=10, pady=10, sticky=tk.E)
        self.entry_search.grid(row=9, column=1, padx=10, pady=10)
        self.button_search.grid(row=15,column=0, columnspan=2, pady=10)
        self.label_sort = tk.Label(self.root, text="Sort by:")
        self.sort_var = tk.StringVar()
        self.sort_combobox = ttk.Combobox(self.root, textvariable=self.sort_var, values=["ID", "Name", "Age", "Gender", "Role", "Experience", "Salary"])
        self.sort_combobox.set("ID")  
        self.button_sort = tk.Button(self.root, text="Sort", command=self.sort_table)

        self.button_pie_chart = tk.Button(self.root, text="Gender Distribution", command=self.show_pie_chart)
        self.button_salary_bar_chart = tk.Button(self.root, text="Salary Distribution", command=self.show_salary_bar_chart)

        self.label_sort.grid(row=10, column=0, padx=10, pady=10, sticky=tk.E)
        self.sort_combobox.grid(row=10, column=1, padx=10, pady=10)
        self.button_sort.grid(row=16, column=0, columnspan=2, pady=10)

        self.button_pie_chart.grid(row=17, column=0, columnspan=2, pady=10)
        self.button_salary_bar_chart.grid(row=18, column=0, columnspan=2, pady=10)
        self.button_undo = tk.Button(self.root, text="Undo", command=self.undo)
        self.button_redo = tk.Button(self.root, text="Redo", command=self.redo)

        self.button_undo.grid(row=10, column=5, pady=10)
        self.button_redo.grid(row=11, column=5, pady=10)
        self.tree.grid(row=0, column=2, rowspan=13, padx=10, pady=10)

    def undo(self):
        if self.undo_stack:
            state = self.undo_stack.pop()
            self.redo_stack.append(self.get_current_state())
            self.load_state(state)

    def redo(self):
        if self.redo_stack:
            state = self.redo_stack.pop()
            self.undo_stack.append(self.get_current_state())
            self.load_state(state)

    def get_current_state(self):
        return {
            'tree_data': self.get_tree_data(),
            'entry_values': self.get_entry_values(),
        }

    def load_state(self, state):
        self.load_tree_data(state['tree_data'])
        self.load_entry_values(state['entry_values'])

    def get_tree_data(self):
        return [self.tree.item(item, 'values') for item in self.tree.get_children()]

    def load_tree_data(self, data):
        self.tree.delete(*self.tree.get_children())
        for row in data:
            self.tree.insert("", "end", values=row)

    def get_entry_values(self):
        return {
            'name': self.entry_name.get(),
            'age': self.entry_age.get(),
            'contact_number': self.entry_contact_number.get(),
            'gmail': self.entry_gmail.get(),
            'gender': self.gender_var.get(),
            'role': self.role_var.get(),
            'experience': self.entry_experience.get(),
            'salary': self.entry_salary.get(),
            'leaves': self.entry_leaves.get(),
        }

    def load_entry_values(self, values):
       
        self.entry_name.delete(0, tk.END)
        self.entry_name.insert(0, values['name'])

        self.entry_age.delete(0, tk.END)
        self.entry_age.insert(0, values['age'])

        self.entry_contact_number.delete(0, tk.END)
        self.entry_contact_number.insert(0, values['contact_number'])

        self.entry_gmail.delete(0, tk.END)
        self.entry_gmail.insert(0, values['gmail'])

        self.gender_var.set(values['gender'])

        self.role_var.set(values['role'])

        self.entry_experience.delete(0, tk.END)
        self.entry_experience.insert(0, values['experience'])

        self.entry_salary.delete(0, tk.END)
        self.entry_salary.insert(0, values['salary'])

        self.entry_leaves.delete(0, tk.END)
        self.entry_leaves.insert(0, values['leaves'])

    def search_employee(self):
        search_term = self.entry_search.get().lower()
        self.tree.delete(*self.tree.get_children())
        self.cursor.execute("""
            SELECT * FROM employees
            WHERE LOWER(name) LIKE ? OR 
                contact_number LIKE ? OR 
                LOWER(gender) LIKE ? OR 
                LOWER(role) LIKE ?""",
            ('%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%'))

        for row in self.cursor.fetchall():
            self.tree.insert("", "end", values=row)


    def sort_table(self):
        column = self.sort_var.get()
        order = "ASC"  
        if column == "Salary":
            column = "salary"
        else:
            column = column.lower()  

        if column not in ["id", "name", "age", "contact_number", "gmail", "gender", "role", "experience", "salary"]:
            messagebox.showerror("Error", "Invalid column for sorting.")
            return

        if column != "id":  
            order = "DESC" if messagebox.askyesno("Sort Descending", f"Do you want to sort {column} in descending order?") else "ASC"

        self.tree.delete(*self.tree.get_children())
        self.cursor.execute(f"SELECT * FROM employees ORDER BY {column} {order}")
        for row in self.cursor.fetchall():
            self.tree.insert("", "end", values=row)


    def show_pie_chart(self):
        self.cursor.execute("SELECT gender, COUNT(*) FROM employees GROUP BY gender")
        data = self.cursor.fetchall()

        labels = [entry[0] for entry in data]
        values = [entry[1] for entry in data]

        fig, ax = plt.subplots()
        ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  
        plt.title("Gender Distribution")
        plt.show()

    def show_salary_bar_chart(self):
        self.cursor.execute("SELECT role, AVG(salary) FROM employees GROUP BY role")
        data = self.cursor.fetchall()

        labels = [entry[0] for entry in data]
        values = [entry[1] for entry in data]

        fig, ax = plt.subplots()
        ax.bar(labels, values, color='blue')
        ax.set_ylabel('Average Salary')
        ax.set_xlabel('Roles')

        plt.title("Average Salary Distribution by Role")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

    def add_employee(self):
        self.label_leaves.grid_remove()
        self.entry_leaves.grid_remove()

        name = self.entry_name.get()
        age = int(self.entry_age.get())
        contact_number = self.entry_contact_number.get()
        gmail = self.entry_gmail.get()
        gender = self.gender_var.get()
        role = self.role_var.get()
        experience = int(self.entry_experience.get())
        salary = self.calculate_salary(experience)

        if not contact_number.isdigit() or len(contact_number) != 10:
            messagebox.showerror("Error", "Invalid Contact Number. Please enter a 10-digit number.")
            
            return
        
        if not gmail.endswith("@gmail.com"):
            messagebox.showerror("Error", "Invalid Gmail address. Please enter a valid Gmail address.")
            return

        self.cursor.execute("INSERT INTO employees (name, age, contact_number, gmail, gender, role, experience, salary) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                            (name, age, contact_number, gmail, gender, role, experience, salary))
        self.conn.commit()

        messagebox.showinfo("Success", "Employee hired successfully!")
        self.show_table()
        self.undo_stack.append(self.get_current_state())
        self.redo_stack.clear()

    def update_employee(self):
        self.label_leaves.grid()
        self.entry_leaves.grid()

        selected_item = self.tree.selection()
        if selected_item:
            name = self.entry_name.get()
            age = int(self.entry_age.get())
            contact_number = self.entry_contact_number.get()
            gmail = self.entry_gmail.get()
            gender = self.gender_var.get()
            role = self.role_var.get()
            experience = int(self.entry_experience.get())
            salary = self.calculate_salary(experience)

            leaves_taken_str = self.entry_leaves.get()
            leaves_taken = int(leaves_taken_str) if leaves_taken_str else 0

            if leaves_taken > 7:
                reduction_amount = 500  
                salary -= reduction_amount

           
            if not contact_number.isdigit() or len(contact_number) != 10:
                messagebox.showerror("Error", "Invalid Contact Number. Please enter a 10-digit number.")
                return

            if not gmail.endswith("@gmail.com"):
                messagebox.showerror("Error", "Invalid Gmail address. Please enter a valid Gmail address.")
                return

            employee_id = self.tree.item(selected_item)['values'][0]

            self.cursor.execute("UPDATE employees SET name=?, age=?, contact_number=?, gmail=?, gender=?, role=?, experience=?, salary=? WHERE id=?",
                                (name, age, contact_number, gmail, gender, role, experience, salary, employee_id))
            self.conn.commit()

          
            self.button_promote.grid()

            messagebox.showinfo("Success", "Employee updated successfully!")
            self.show_table()
        else:
            messagebox.showerror("Error", "Please select an employee to update.")
            self.undo_stack.append(self.get_current_state())
            self.redo_stack.clear()

    def remove_employee(self):
        selected_item = self.tree.selection()
        if selected_item:
            employee_id = self.tree.item(selected_item)['values'][0]
            self.cursor.execute("DELETE FROM employees WHERE id=?", (employee_id,))
            self.conn.commit()

            messagebox.showinfo("Success", "Employee removed successfully!")
            self.show_table()
        else:
            messagebox.showerror("Error", "Please select an employee to remove.")
            self.undo_stack.append(self.get_current_state())
            self.redo_stack.clear()

    def calculate_salary(self, experience):
        base_salary = 30000  
        return max(base_salary, 50000 * experience)


    def show_table(self):
        self.tree.delete(*self.tree.get_children())
        self.cursor.execute("SELECT * FROM employees")
        for row in self.cursor.fetchall():
            self.tree.insert("", "end", values=row)
            self.undo_stack.append(self.get_current_state())
            self.redo_stack.clear()

    def promote_employee(self):
        selected_item = self.tree.selection()
        if selected_item:
          
            employee_id = self.tree.item(selected_item)['values'][0]
            name = self.tree.item(selected_item)['values'][1]
            current_salary = self.tree.item(selected_item)['values'][8]

           
            new_salary = int(current_salary * 1.1)

           
            self.cursor.execute("UPDATE employees SET salary=? WHERE id=?", (new_salary, employee_id))
            self.conn.commit()

            self.show_table()

            messagebox.showinfo("Success", f"{name}'s salary has been promoted successfully!")
        else:
            messagebox.showerror("Error", "Please select an employee to promote.")
            self.undo_stack.append(self.get_current_state())
            self.redo_stack.clear()

if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeeManagementSystem(root)
    root.mainloop()
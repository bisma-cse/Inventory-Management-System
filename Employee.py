from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import mysql.connector

class employeeClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System")
        self.root.config(bg="white")
        self.root.focus_force()

        #===================================================
        #==All Variables
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        self.var_emp_id = StringVar()
        self.var_gender = StringVar()
        self.var_contact = StringVar()
        self.var_name = StringVar()
        self.var_dob = StringVar()
        self.var_doj = StringVar()
        self.var_email = StringVar()
        self.var_password = StringVar()
        self.var_usertype = StringVar()
        self.var_salary = StringVar()

        #=====SearchFrame======
        SearchFrame = LabelFrame(self.root, text="Search Employee", bg="White", font=("goudy old style", 12, "bold"), bd=2, relief=RIDGE, fg="#05536B")
        SearchFrame.place(x=250, y=20, width=600, height=70)
        
        #===Option====
        cmb_search = ttk.Combobox(SearchFrame, textvariable=self.var_searchby, values=("Select","Email","Name","Contact"), state='readonly', justify=CENTER, font=("goudy old style", 12))
        cmb_search.place(x=10, y=10, width=150)
        cmb_search.current(0)

        txt_search = Entry(SearchFrame, textvariable=self.var_searchtxt, font=("goudy old style", 12), bg="white")
        txt_search.place(x=180, y=10, width=200)
        
        btn_search = Button(SearchFrame, text="🔍 Search", command=self.search, font=("goudy old style", 12, "bold"), bg="#3498DB", fg="white", cursor="hand2", activebackground="#2980B9")
        btn_search.place(x=400, y=10, width=150, height=25)

        #===title===
        title = Label(self.root, text="Employee Details", font=("goudy old style", 15, "bold"), fg="white", bg="#05536B")
        title.place(x=50, y=100, width=1000)

        #====Content=====
        #====Row1======
        lbl_empid = Label(self.root, text="Emp ID:", font=("goudy old style", 15), bg="white", fg="#05536B")
        lbl_empid.place(x=50, y=150)
        
        lbl_gender = Label(self.root, text="Gender:", font=("goudy old style", 15), bg="white", fg="#05536B")
        lbl_gender.place(x=400, y=150)
        
        lbl_contact = Label(self.root, text="Contact:", font=("goudy old style", 15), bg="white", fg="#05536B")
        lbl_contact.place(x=750, y=150)
        
        txt_empid = Entry(self.root, textvariable=self.var_emp_id, font=("goudy old style", 15), bg="lightyellow", fg="#05536B")
        txt_empid.place(x=150, y=150, width=180)
        
        cmb_gender = ttk.Combobox(self.root, textvariable=self.var_gender, values=("Select","Male","Female","Other"), state='readonly', justify=CENTER, font=("goudy old style", 12))
        cmb_gender.place(x=500, y=150, width=180)
        cmb_gender.current(0)
        
        txt_contact = Entry(self.root, textvariable=self.var_contact, font=("goudy old style", 15), bg="lightyellow", fg="#05536B")
        txt_contact.place(x=850, y=150, width=180)

        #===Row2====
        lbl_name = Label(self.root, text="Name:", font=("goudy old style", 15), bg="white", fg="#05536B")
        lbl_name.place(x=50, y=190)
        
        lbl_dob = Label(self.root, text="D.O.B:", font=("goudy old style", 15), bg="white", fg="#05536B")
        lbl_dob.place(x=400, y=190)
        
        lbl_doj = Label(self.root, text="D.O.J:", font=("goudy old style", 15), bg="white", fg="#05536B")
        lbl_doj.place(x=750, y=190)
        
        txt_name = Entry(self.root, textvariable=self.var_name, font=("goudy old style", 15), bg="lightyellow", fg="#05536B")
        txt_name.place(x=150, y=190, width=180)
        
        txt_dob = Entry(self.root, textvariable=self.var_dob, font=("goudy old style", 12), bg="lightyellow", fg="#05536B")
        txt_dob.place(x=500, y=190, width=180)
        
        txt_doj = Entry(self.root, textvariable=self.var_doj, font=("goudy old style", 15), bg="lightyellow", fg="#05536B")
        txt_doj.place(x=850, y=190, width=180)

        #===Row3====
        lbl_email = Label(self.root, text="Email:", font=("goudy old style", 15), bg="white", fg="#05536B")
        lbl_email.place(x=50, y=230)
        
        lbl_password = Label(self.root, text="Password:", font=("goudy old style", 15), bg="white", fg="#05536B")
        lbl_password.place(x=400, y=230)
        
        lbl_utype = Label(self.root, text="User-Type:", font=("goudy old style", 15), bg="white", fg="#05536B")
        lbl_utype.place(x=750, y=230)
        
        txt_email = Entry(self.root, textvariable=self.var_email, font=("goudy old style", 15), bg="lightyellow", fg="#05536B")
        txt_email.place(x=150, y=230, width=180)
        
        txt_password = Entry(self.root, textvariable=self.var_password, font=("goudy old style", 12), bg="lightyellow", fg="#05536B", show="*")
        txt_password.place(x=500, y=230, width=180)
        
        cmb_utype = ttk.Combobox(self.root, textvariable=self.var_usertype, values=("Select","Admin","Employee"), state='readonly', justify=CENTER, font=("goudy old style", 12))
        cmb_utype.place(x=850, y=230, width=180)
        cmb_utype.current(0)

        #===Row4====
        lbl_address = Label(self.root, text="Address:", font=("goudy old style", 15), bg="white", fg="#05536B")
        lbl_address.place(x=50, y=270)
        
        lbl_salary = Label(self.root, text="Salary:", font=("goudy old style", 15), bg="white", fg="#05536B")
        lbl_salary.place(x=750, y=270)
        
        self.txt_address = Text(self.root, font=("goudy old style", 15), bg="lightyellow", fg="#05536B", height=1)
        self.txt_address.place(x=150, y=270, width=580, height=28)
        
        txt_salary = Entry(self.root, textvariable=self.var_salary, font=("goudy old style", 12), bg="lightyellow", fg="#05536B")
        txt_salary.place(x=850, y=270, width=180)
        
        #===Colorful Buttons===
        btn_add = Button(self.root, text="💾 Save", command=self.add, font=("goudy old style", 12, "bold"), bg="#2ECC71", fg="white", cursor="hand2", activebackground="#27AE60", bd=0, padx=10)
        btn_add.place(x=100, y=320, width="120", height="35")
        
        btn_update = Button(self.root, text="✏️ Update", command=self.update, font=("goudy old style", 12, "bold"), bg="#3498DB", fg="white", cursor="hand2", activebackground="#2980B9", bd=0, padx=10)
        btn_update.place(x=350, y=320, width="120", height="35")
        
        btn_delete = Button(self.root, text="🗑️ Delete", command=self.delete, font=("goudy old style", 12, "bold"), bg="#E74C3C", fg="white", cursor="hand2", activebackground="#C0392B", bd=0, padx=10)
        btn_delete.place(x=600, y=320, width="120", height="35")
        
        btn_clear = Button(self.root, text="🔄 Clear", command=self.clear, font=("goudy old style", 12, "bold"), bg="#95A5A6", fg="white", cursor="hand2", activebackground="#7F8C8D", bd=0, padx=10)
        btn_clear.place(x=850, y=320, width="120", height="35")

        #===   Employee Details====
        emp_frame = Frame(self.root, bd=3, relief=RIDGE)
        emp_frame.place(x=0, y=360, relwidth=1, height=140)

        scrolly = Scrollbar(emp_frame, orient=VERTICAL)
        scrollx = Scrollbar(emp_frame, orient=HORIZONTAL)

        self.EmployeeTable = ttk.Treeview(emp_frame, columns=("eid","name","email","gender","contact","dob","doj","password","usertype","address","salary"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.EmployeeTable.xview)
        scrolly.config(command=self.EmployeeTable.yview)

        self.EmployeeTable.heading("eid", text="Emp-ID")
        self.EmployeeTable.heading("name", text="Name")
        self.EmployeeTable.heading("email", text="Email")
        self.EmployeeTable.heading("gender", text="Gender")
        self.EmployeeTable.heading("contact", text="Contact")
        self.EmployeeTable.heading("dob", text="D.O.B")
        self.EmployeeTable.heading("doj", text="D.O.J")
        self.EmployeeTable.heading("password", text="Password")
        self.EmployeeTable.heading("usertype", text="U-Type")
        self.EmployeeTable.heading("address", text="Address")
        self.EmployeeTable.heading("salary", text="Salary")

        self.EmployeeTable["show"] = "headings"
        
        # Set column widths
        self.EmployeeTable.column("eid", width=90)
        self.EmployeeTable.column("name", width=100)
        self.EmployeeTable.column("email", width=120)
        self.EmployeeTable.column("gender", width=80)
        self.EmployeeTable.column("contact", width=100)
        self.EmployeeTable.column("dob", width=90)
        self.EmployeeTable.column("doj", width=90)
        self.EmployeeTable.column("password", width=100)
        self.EmployeeTable.column("usertype", width=80)
        self.EmployeeTable.column("address", width=150)
        self.EmployeeTable.column("salary", width=90)
        
        self.EmployeeTable.pack(fill=BOTH, expand=1)
        
        # Bind selection event
        self.EmployeeTable.bind("<<TreeviewSelect>>", self.select_data)
        
        # Load initial data
        self.show()

    #=================================================================
    def add(self):
        con = None
        try:
            con = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="ims")
            cur = con.cursor()
            
            if self.var_emp_id.get() == "":
                messagebox.showerror("Error", "Employee ID is required", parent=self.root)
                return
            
            # Check if employee ID already exists
            cur.execute("SELECT * FROM employee WHERE eid=%s", (self.var_emp_id.get(),))
            row = cur.fetchone()
            if row is not None:
                messagebox.showerror("Error", "This Emp_ID is already assigned, try a different one", parent=self.root)
            else:
                cur.execute("""INSERT INTO employee (eid, name, email, gender, contact, dob, doj, password, usertype, address, salary) 
                              VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                             (
                                self.var_emp_id.get(),
                                self.var_name.get(),
                                self.var_email.get(),
                                self.var_gender.get(),
                                self.var_contact.get(),
                                self.var_dob.get(),
                                self.var_doj.get(),
                                self.var_password.get(),
                                self.var_usertype.get(),
                                self.txt_address.get("1.0", END).strip(),
                                self.var_salary.get()
                             ))
                con.commit()
                messagebox.showinfo("Success", "Employee added successfully", parent=self.root)
                self.show()
                self.clear()
                
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            if con and con.is_connected():
                con.close()

    #=================================================================
    def update(self):
        con = None
        try:
            con = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="ims")
            cur = con.cursor()
            
            if self.var_emp_id.get() == "":
                messagebox.showerror("Error", "Employee ID is required", parent=self.root)
                return
            
            cur.execute("""UPDATE employee SET name=%s, email=%s, gender=%s, contact=%s, dob=%s, doj=%s, 
                          password=%s, usertype=%s, address=%s, salary=%s WHERE eid=%s""",
                         (
                            self.var_name.get(),
                            self.var_email.get(),
                            self.var_gender.get(),
                            self.var_contact.get(),
                            self.var_dob.get(),
                            self.var_doj.get(),
                            self.var_password.get(),
                            self.var_usertype.get(),
                            self.txt_address.get("1.0", END).strip(),
                            self.var_salary.get(),
                            self.var_emp_id.get()
                         ))
            con.commit()
            messagebox.showinfo("Success", "Employee updated successfully", parent=self.root)
            self.show()
            self.clear()
            
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            if con and con.is_connected():
                con.close()

    #=================================================================
    def delete(self):
        con = None
        try:
            con = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="ims")
            cur = con.cursor()
            
            if self.var_emp_id.get() == "":
                messagebox.showerror("Error", "Employee ID is required", parent=self.root)
                return
            
            # Confirm deletion
            if messagebox.askyesno("Confirm", "Are you sure you want to delete this employee?", parent=self.root):
                cur.execute("DELETE FROM employee WHERE eid=%s", (self.var_emp_id.get(),))
                con.commit()
                messagebox.showinfo("Success", "Employee deleted successfully", parent=self.root)
                self.show()
                self.clear()
            
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            if con and con.is_connected():
                con.close()

    #=================================================================
    def clear(self):
        self.var_emp_id.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.var_gender.set("Select")
        self.var_contact.set("")
        self.var_dob.set("")
        self.var_doj.set("")
        self.var_password.set("")
        self.var_usertype.set("Select")
        self.txt_address.delete("1.0", END)
        self.var_salary.set("")
        self.var_searchby.set("Select")
        self.var_searchtxt.set("")

    #=================================================================
    def show(self):
        con = None
        try:
            con = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="ims")
            cur = con.cursor()
            
            # Clear existing data in treeview
            for item in self.EmployeeTable.get_children():
                self.EmployeeTable.delete(item)
            
            # Fetch all employees
            cur.execute("SELECT * FROM employee")
            rows = cur.fetchall()
            for row in rows:
                self.EmployeeTable.insert('', END, values=row)
                
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            if con and con.is_connected():
                con.close()

    #=================================================================
    def search(self):
        con = None
        try:
            con = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="ims")
            cur = con.cursor()
            
            search_by = self.var_searchby.get()
            search_txt = self.var_searchtxt.get()
            
            if search_by == "Select" or search_txt == "":
                messagebox.showerror("Error", "Please select search criteria and enter search text", parent=self.root)
                return
            
            # Clear existing data
            for item in self.EmployeeTable.get_children():
                self.EmployeeTable.delete(item)
            
            # Search based on criteria
            if search_by == "Email":
                cur.execute("SELECT * FROM employee WHERE email LIKE %s", (f"%{search_txt}%",))
            elif search_by == "Name":
                cur.execute("SELECT * FROM employee WHERE name LIKE %s", (f"%{search_txt}%",))
            elif search_by == "Contact":
                cur.execute("SELECT * FROM employee WHERE contact LIKE %s", (f"%{search_txt}%",))
            
            rows = cur.fetchall()
            if len(rows) == 0:
                messagebox.showinfo("Info", "No employee found", parent=self.root)
            else:
                for row in rows:
                    self.EmployeeTable.insert('', END, values=row)
                    
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            if con and con.is_connected():
                con.close()

    #=================================================================
    def select_data(self, event):
        try:
            # Get selected item
            selected = self.EmployeeTable.focus()
            if selected:
                values = self.EmployeeTable.item(selected, 'values')
                
                # Set values to entry fields
                self.var_emp_id.set(values[0])
                self.var_name.set(values[1])
                self.var_email.set(values[2])
                self.var_gender.set(values[3])
                self.var_contact.set(values[4])
                self.var_dob.set(values[5])
                self.var_doj.set(values[6])
                self.var_password.set(values[7])
                self.var_usertype.set(values[8])
                self.txt_address.delete("1.0", END)
                self.txt_address.insert("1.0", values[9])
                self.var_salary.set(values[10])
                
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)


# Database setup script (run once)
def setup_database():
    try:
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="")
        cur = con.cursor()
        
        # Create database if not exists
        cur.execute("CREATE DATABASE IF NOT EXISTS ims")
        cur.execute("USE ims")
        
        # Create employee table if not exists
        cur.execute("""CREATE TABLE IF NOT EXISTS employee (
            eid VARCHAR(50) PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100),
            gender VARCHAR(10),
            contact VARCHAR(15),
            dob DATE,
            doj DATE,
            password VARCHAR(50),
            usertype VARCHAR(20),
            address TEXT,
            salary DECIMAL(10,2)
        )""")
        
        con.close()
        print("Database setup completed successfully!")
        
    except Exception as ex:
        print(f"Database setup error: {ex}")


if __name__ == "__main__":
    # Setup database first
    setup_database()
    
    # Run the application
    root = Tk()
    obj = employeeClass(root)
    root.mainloop()
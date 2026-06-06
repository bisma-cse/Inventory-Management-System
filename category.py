from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime

class categoryClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Category Management System")
        self.root.config(bg="white")
        self.root.focus_force()

        # ==================== Variables ====================
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        self.var_cat_id = StringVar()
        self.var_name = StringVar()
        self.var_description = StringVar()
        self.var_status = StringVar()

        # ==================== Search Frame ====================
        SearchFrame = LabelFrame(self.root, text="Search Category", 
                                 bg="White", font=("goudy old style", 12, "bold"), 
                                 bd=2, relief=RIDGE, fg="#05536B")
        SearchFrame.place(x=250, y=20, width=600, height=70)
        
        # Search options
        cmb_search = ttk.Combobox(SearchFrame, textvariable=self.var_searchby, 
                                  values=("Select", "Category ID", "Name"), 
                                  state='readonly', justify=CENTER, 
                                  font=("goudy old style", 12))
        cmb_search.place(x=10, y=10, width=150)
        cmb_search.current(0)

        txt_search = Entry(SearchFrame, textvariable=self.var_searchtxt, 
                          font=("goudy old style", 12), bg="white")
        txt_search.place(x=180, y=10, width=200)
        
        btn_search = Button(SearchFrame, text="🔍 Search", command=self.search, 
                           font=("goudy old style", 12, "bold"), bg="#3498DB", 
                           fg="white", cursor="hand2", activebackground="#2980B9", bd=0)
        btn_search.place(x=400, y=10, width=150, height=25)

        # ==================== Title ====================
        title = Label(self.root, text="Category Details", 
                     font=("goudy old style", 15, "bold"), 
                     fg="white", bg="#05536B")
        title.place(x=50, y=100, width=1000)

        # ==================== Content Frame ====================
        # Row 1 - Category ID and Name
        lbl_cat_id = Label(self.root, text="Category ID:", 
                          font=("goudy old style", 15), bg="white", fg="#05536B")
        lbl_cat_id.place(x=50, y=150)
        
        lbl_name = Label(self.root, text="Name:", 
                        font=("goudy old style", 15), bg="white", fg="#05536B")
        lbl_name.place(x=400, y=150)
        
        lbl_status = Label(self.root, text="Status:", 
                          font=("goudy old style", 15), bg="white", fg="#05536B")
        lbl_status.place(x=750, y=150)
        
        txt_cat_id = Entry(self.root, textvariable=self.var_cat_id, 
                          font=("goudy old style", 15), bg="lightyellow", fg="#05536B")
        txt_cat_id.place(x=150, y=150, width=180)
        
        txt_name = Entry(self.root, textvariable=self.var_name, 
                        font=("goudy old style", 15), bg="lightyellow", fg="#05536B")
        txt_name.place(x=500, y=150, width=180)
        
        cmb_status = ttk.Combobox(self.root, textvariable=self.var_status, 
                                  values=("Select", "Active", "Inactive"), 
                                  state='readonly', justify=CENTER, 
                                  font=("goudy old style", 12))
        cmb_status.place(x=850, y=150, width=180)
        cmb_status.current(0)

        # Row 2 - Description
        lbl_description = Label(self.root, text="Description:", 
                               font=("goudy old style", 15), bg="white", fg="#05536B")
        lbl_description.place(x=50, y=200)
        
        self.txt_description = Text(self.root, font=("goudy old style", 15), 
                                    bg="lightyellow", fg="#05536B", height=4)
        self.txt_description.place(x=150, y=200, width=880, height=80)

        # ==================== Colorful Buttons ====================
        btn_add = Button(self.root, text="💾 Save", command=self.add, 
                        font=("goudy old style", 12, "bold"), bg="#2ECC71", 
                        fg="white", cursor="hand2", activebackground="#27AE60", bd=0, padx=10)
        btn_add.place(x=100, y=300, width="120", height="35")
        
        btn_update = Button(self.root, text="✏️ Update", command=self.update, 
                           font=("goudy old style", 12, "bold"), bg="#3498DB", 
                           fg="white", cursor="hand2", activebackground="#2980B9", bd=0, padx=10)
        btn_update.place(x=350, y=300, width="120", height="35")
        
        btn_delete = Button(self.root, text="🗑️ Delete", command=self.delete, 
                           font=("goudy old style", 12, "bold"), bg="#E74C3C", 
                           fg="white", cursor="hand2", activebackground="#C0392B", bd=0, padx=10)
        btn_delete.place(x=600, y=300, width="120", height="35")
        
        btn_clear = Button(self.root, text="🔄 Clear", command=self.clear, 
                          font=("goudy old style", 12, "bold"), bg="#95A5A6", 
                          fg="white", cursor="hand2", activebackground="#7F8C8D", bd=0, padx=10)
        btn_clear.place(x=850, y=300, width="120", height="35")

        # ==================== Category Details Table ====================
        cat_frame = Frame(self.root, bd=3, relief=RIDGE)
        cat_frame.place(x=0, y=350, relwidth=1, height=150)

        scrolly = Scrollbar(cat_frame, orient=VERTICAL)
        scrollx = Scrollbar(cat_frame, orient=HORIZONTAL)

        self.CategoryTable = ttk.Treeview(cat_frame, 
                                          columns=("cid", "name", "description", "status", "created_date"), 
                                          yscrollcommand=scrolly.set, 
                                          xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.CategoryTable.xview)
        scrolly.config(command=self.CategoryTable.yview)

        # Define headings
        self.CategoryTable.heading("cid", text="Category ID")
        self.CategoryTable.heading("name", text="Name")
        self.CategoryTable.heading("description", text="Description")
        self.CategoryTable.heading("status", text="Status")
        self.CategoryTable.heading("created_date", text="Created Date")

        self.CategoryTable["show"] = "headings"
        
        # Set column widths
        self.CategoryTable.column("cid", width=100)
        self.CategoryTable.column("name", width=150)
        self.CategoryTable.column("description", width=400)
        self.CategoryTable.column("status", width=100)
        self.CategoryTable.column("created_date", width=120)
        
        self.CategoryTable.pack(fill=BOTH, expand=1)
        
        # Bind selection event
        self.CategoryTable.bind("<<TreeviewSelect>>", self.select_data)
        
        # Load initial data
        self.show()

    # ==================== Database Operations ====================
    
    def add(self):
        con = None
        try:
            con = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="ims")
            cur = con.cursor()
            
            if self.var_cat_id.get() == "":
                messagebox.showerror("Error", "Category ID is required", parent=self.root)
                return
            
            if self.var_name.get() == "":
                messagebox.showerror("Error", "Category Name is required", parent=self.root)
                return
            
            if self.var_status.get() == "Select":
                messagebox.showerror("Error", "Please select status", parent=self.root)
                return
            
            # Check if category ID already exists
            cur.execute("SELECT * FROM category WHERE cid=%s", (self.var_cat_id.get(),))
            row = cur.fetchone()
            if row is not None:
                messagebox.showerror("Error", "This Category ID is already assigned", parent=self.root)
            else:
                cur.execute("""INSERT INTO category (cid, name, description, status, created_date) 
                              VALUES (%s, %s, %s, %s, %s)""",
                             (
                                self.var_cat_id.get(),
                                self.var_name.get(),
                                self.txt_description.get("1.0", END).strip(),
                                self.var_status.get(),
                                datetime.now().date()
                             ))
                con.commit()
                messagebox.showinfo("Success", "Category added successfully", parent=self.root)
                self.show()
                self.clear()
                
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            if con and con.is_connected():
                con.close()

    def update(self):
        con = None
        try:
            con = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="ims")
            cur = con.cursor()
            
            if self.var_cat_id.get() == "":
                messagebox.showerror("Error", "Category ID is required", parent=self.root)
                return
            
            if self.var_status.get() == "Select":
                messagebox.showerror("Error", "Please select status", parent=self.root)
                return
            
            cur.execute("""UPDATE category SET name=%s, description=%s, status=%s WHERE cid=%s""",
                         (
                            self.var_name.get(),
                            self.txt_description.get("1.0", END).strip(),
                            self.var_status.get(),
                            self.var_cat_id.get()
                         ))
            con.commit()
            messagebox.showinfo("Success", "Category updated successfully", parent=self.root)
            self.show()
            self.clear()
            
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            if con and con.is_connected():
                con.close()

    def delete(self):
        con = None
        try:
            con = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="ims")
            cur = con.cursor()
            
            if self.var_cat_id.get() == "":
                messagebox.showerror("Error", "Please select a category to delete", parent=self.root)
                return
            
            # Confirm deletion
            if messagebox.askyesno("Confirm", "Are you sure you want to delete this category?\nThis action cannot be undone!", parent=self.root):
                cur.execute("DELETE FROM category WHERE cid=%s", (self.var_cat_id.get(),))
                con.commit()
                messagebox.showinfo("Success", "Category deleted successfully", parent=self.root)
                self.show()
                self.clear()
            
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            if con and con.is_connected():
                con.close()

    def clear(self):
        """Clear all input fields"""
        self.var_cat_id.set("")
        self.var_name.set("")
        self.txt_description.delete("1.0", END)
        self.var_status.set("Select")
        self.var_searchby.set("Select")
        self.var_searchtxt.set("")

    def show(self):
        """Display all categories in the table"""
        con = None
        try:
            con = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="ims")
            cur = con.cursor()
            
            # Clear existing data
            for item in self.CategoryTable.get_children():
                self.CategoryTable.delete(item)
            
            # Fetch all categories
            cur.execute("SELECT cid, name, description, status, created_date FROM category ORDER BY created_date DESC")
            rows = cur.fetchall()
            for row in rows:
                self.CategoryTable.insert('', END, values=row)
                
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            if con and con.is_connected():
                con.close()

    def search(self):
        """Search for categories based on criteria"""
        con = None
        try:
            con = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="ims")
            cur = con.cursor()
            
            search_by = self.var_searchby.get()
            search_txt = self.var_searchtxt.get().strip()
            
            if search_by == "Select":
                messagebox.showerror("Error", "Please select search criteria", parent=self.root)
                return
            
            if search_txt == "":
                messagebox.showerror("Error", "Please enter search text", parent=self.root)
                return
            
            # Clear existing data
            for item in self.CategoryTable.get_children():
                self.CategoryTable.delete(item)
            
            # Search based on criteria
            if search_by == "Category ID":
                query = "SELECT cid, name, description, status, created_date FROM category WHERE cid LIKE %s ORDER BY created_date DESC"
                cur.execute(query, (f"%{search_txt}%",))
            elif search_by == "Name":
                query = "SELECT cid, name, description, status, created_date FROM category WHERE name LIKE %s ORDER BY created_date DESC"
                cur.execute(query, (f"%{search_txt}%",))
            else:
                messagebox.showerror("Error", "Invalid search criteria", parent=self.root)
                return
            
            rows = cur.fetchall()
            
            if len(rows) == 0:
                messagebox.showinfo("Info", f"No category found with {search_by}: '{search_txt}'", parent=self.root)
                self.show()
            else:
                for row in rows:
                    self.CategoryTable.insert('', END, values=row)
                    
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            if con and con.is_connected():
                con.close()

    def select_data(self, event):
        """Load selected category data into input fields"""
        try:
            # Get selected item
            selected = self.CategoryTable.focus()
            if selected:
                values = self.CategoryTable.item(selected, 'values')
                
                # Set values to entry fields
                self.var_cat_id.set(values[0])
                self.var_name.set(values[1])
                self.txt_description.delete("1.0", END)
                self.txt_description.insert("1.0", values[2])
                self.var_status.set(values[3])
                
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)


# Database setup function
def setup_category_database():
    """Create category table if not exists"""
    try:
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="")
        cur = con.cursor()
        
        # Create database if not exists
        cur.execute("CREATE DATABASE IF NOT EXISTS ims")
        cur.execute("USE ims")
        
        # Create category table
        cur.execute("""CREATE TABLE IF NOT EXISTS category (
            cid VARCHAR(50) PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            description TEXT,
            status VARCHAR(20) DEFAULT 'Active',
            created_date DATE,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )""")
        
        con.close()
        print("Category table setup completed successfully!")
        
    except Exception as ex:
        print(f"Database setup error: {ex}")


if __name__ == "__main__":
    # Setup database
    setup_category_database()
    
    # Run the application
    root = Tk()
    obj = categoryClass(root)
    root.mainloop()
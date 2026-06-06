from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime

class productClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1200x650+200+100")
        self.root.title("Product Management System")
        self.root.config(bg="white")
        self.root.focus_force()

        # ==================== Variables ====================
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        self.var_product_id = StringVar()
        self.var_name = StringVar()
        self.var_price = StringVar()
        self.var_cost = StringVar()
        self.var_quantity = StringVar()
        self.var_description = StringVar()
        self.var_reorder_level = StringVar()
        self.var_unit = StringVar()
        self.var_status = StringVar()
        self.var_category_id = StringVar()
        self.var_supplier_id = StringVar()

        # ==================== Search Frame ====================
        SearchFrame = LabelFrame(self.root, text="Search Product", 
                                 bg="White", font=("goudy old style", 12, "bold"), 
                                 bd=2, relief=RIDGE, fg="#05536B")
        SearchFrame.place(x=250, y=20, width=600, height=70)
        
        # Search options
        cmb_search = ttk.Combobox(SearchFrame, textvariable=self.var_searchby, 
                                  values=("Select", "Product ID", "Name", "Category", "Supplier"), 
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
        title = Label(self.root, text="Product Details", 
                     font=("goudy old style", 15, "bold"), 
                     fg="white", bg="#05536B")
        title.place(x=50, y=100, width=1100)

        # ==================== Content Frame ====================
        # Row 1 - Product ID and Name
        lbl_product_id = Label(self.root, text="Product ID *:", 
                               font=("goudy old style", 13), bg="white", fg="#05536B")
        lbl_product_id.place(x=50, y=150)
        
        lbl_name = Label(self.root, text="Name *:", 
                        font=("goudy old style", 13), bg="white", fg="#05536B")
        lbl_name.place(x=400, y=150)
        
        lbl_unit = Label(self.root, text="Unit:", 
                        font=("goudy old style", 13), bg="white", fg="#05536B")
        lbl_unit.place(x=750, y=150)
        
        txt_product_id = Entry(self.root, textvariable=self.var_product_id, 
                              font=("goudy old style", 13), bg="lightyellow", width=18)
        txt_product_id.place(x=170, y=150, width=180)
        
        txt_name = Entry(self.root, textvariable=self.var_name, 
                        font=("goudy old style", 13), bg="lightyellow", width=18)
        txt_name.place(x=520, y=150, width=180)
        
        cmb_unit = ttk.Combobox(self.root, textvariable=self.var_unit, 
                               values=("Select", "Pcs", "Kg", "Gram", "Liter", "Meter", "Dozen", "Box", "Pack"), 
                               state='readonly', font=("goudy old style", 12), width=16)
        cmb_unit.place(x=850, y=150, width=180)
        cmb_unit.current(0)

        # Row 2 - Price and Cost
        lbl_price = Label(self.root, text="Price (Rs):", 
                         font=("goudy old style", 13), bg="white", fg="#05536B")
        lbl_price.place(x=50, y=190)
        
        lbl_cost = Label(self.root, text="Cost (Rs):", 
                        font=("goudy old style", 13), bg="white", fg="#05536B")
        lbl_cost.place(x=400, y=190)
        
        lbl_quantity = Label(self.root, text="Quantity:", 
                            font=("goudy old style", 13), bg="white", fg="#05536B")
        lbl_quantity.place(x=750, y=190)
        
        txt_price = Entry(self.root, textvariable=self.var_price, 
                         font=("goudy old style", 13), bg="lightyellow", width=18)
        txt_price.place(x=170, y=190, width=180)
        
        txt_cost = Entry(self.root, textvariable=self.var_cost, 
                        font=("goudy old style", 13), bg="lightyellow", width=18)
        txt_cost.place(x=520, y=190, width=180)
        
        txt_quantity = Entry(self.root, textvariable=self.var_quantity, 
                            font=("goudy old style", 13), bg="lightyellow", width=18)
        txt_quantity.place(x=850, y=190, width=180)

        # Row 3 - Category and Supplier
        lbl_category = Label(self.root, text="Category *:", 
                            font=("goudy old style", 13), bg="white", fg="#05536B")
        lbl_category.place(x=50, y=230)
        
        lbl_supplier = Label(self.root, text="Supplier *:", 
                            font=("goudy old style", 13), bg="white", fg="#05536B")
        lbl_supplier.place(x=400, y=230)
        
        lbl_reorder = Label(self.root, text="Reorder Level:", 
                           font=("goudy old style", 13), bg="white", fg="#05536B")
        lbl_reorder.place(x=750, y=230)
        
        # Category Combobox
        self.cmb_category = ttk.Combobox(self.root, textvariable=self.var_category_id, 
                                        state='readonly', font=("goudy old style", 12), width=16)
        self.cmb_category.place(x=170, y=230, width=180)
        self.load_categories()
        
        # Supplier Combobox
        self.cmb_supplier = ttk.Combobox(self.root, textvariable=self.var_supplier_id, 
                                        state='readonly', font=("goudy old style", 12), width=16)
        self.cmb_supplier.place(x=520, y=230, width=180)
        self.load_suppliers()
        
        txt_reorder = Entry(self.root, textvariable=self.var_reorder_level, 
                           font=("goudy old style", 13), bg="lightyellow", width=18)
        txt_reorder.place(x=850, y=230, width=180)

        # Row 4 - Status and Description
        lbl_status = Label(self.root, text="Status:", 
                          font=("goudy old style", 13), bg="white", fg="#05536B")
        lbl_status.place(x=50, y=270)
        
        cmb_status = ttk.Combobox(self.root, textvariable=self.var_status, 
                                  values=("Select", "Active", "Inactive"), 
                                  state='readonly', font=("goudy old style", 12), width=16)
        cmb_status.place(x=170, y=270, width=180)
        cmb_status.current(0)
        
        lbl_description = Label(self.root, text="Description:", 
                               font=("goudy old style", 13), bg="white", fg="#05536B")
        lbl_description.place(x=400, y=270)
        
        self.txt_description = Text(self.root, font=("goudy old style", 13), 
                                    bg="lightyellow", height=3, width=50)
        self.txt_description.place(x=520, y=270, width=510, height=60)

        # ==================== Colorful Buttons ====================
        btn_add = Button(self.root, text="💾 Save", command=self.add, 
                        font=("goudy old style", 12, "bold"), bg="#2ECC71", 
                        fg="white", cursor="hand2", activebackground="#27AE60", bd=0, padx=10)
        btn_add.place(x=100, y=350, width="120", height="35")
        
        btn_update = Button(self.root, text="✏️ Update", command=self.update, 
                           font=("goudy old style", 12, "bold"), bg="#3498DB", 
                           fg="white", cursor="hand2", activebackground="#2980B9", bd=0, padx=10)
        btn_update.place(x=350, y=350, width="120", height="35")
        
        btn_delete = Button(self.root, text="🗑️ Delete", command=self.delete, 
                           font=("goudy old style", 12, "bold"), bg="#E74C3C", 
                           fg="white", cursor="hand2", activebackground="#C0392B", bd=0, padx=10)
        btn_delete.place(x=600, y=350, width="120", height="35")
        
        btn_clear = Button(self.root, text="🔄 Clear", command=self.clear, 
                          font=("goudy old style", 12, "bold"), bg="#95A5A6", 
                          fg="white", cursor="hand2", activebackground="#7F8C8D", bd=0, padx=10)
        btn_clear.place(x=850, y=350, width="120", height="35")

        # ==================== Product Details Table ====================
        product_frame = Frame(self.root, bd=3, relief=RIDGE)
        product_frame.place(x=0, y=400, relwidth=1, height=250)

        scrolly = Scrollbar(product_frame, orient=VERTICAL)
        scrollx = Scrollbar(product_frame, orient=HORIZONTAL)

        self.ProductTable = ttk.Treeview(product_frame, 
                                          columns=("pid", "name", "price", "cost", "quantity", 
                                                  "unit", "category", "supplier", "reorder_level", 
                                                  "status", "description", "created_date"), 
                                          yscrollcommand=scrolly.set, 
                                          xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.ProductTable.xview)
        scrolly.config(command=self.ProductTable.yview)

        # Define headings
        self.ProductTable.heading("pid", text="Product ID")
        self.ProductTable.heading("name", text="Name")
        self.ProductTable.heading("price", text="Price (Rs)")
        self.ProductTable.heading("cost", text="Cost (Rs)")
        self.ProductTable.heading("quantity", text="Quantity")
        self.ProductTable.heading("unit", text="Unit")
        self.ProductTable.heading("category", text="Category")
        self.ProductTable.heading("supplier", text="Supplier")
        self.ProductTable.heading("reorder_level", text="Reorder Level")
        self.ProductTable.heading("status", text="Status")
        self.ProductTable.heading("description", text="Description")
        self.ProductTable.heading("created_date", text="Created Date")

        self.ProductTable["show"] = "headings"
        
        # Set column widths
        self.ProductTable.column("pid", width=100)
        self.ProductTable.column("name", width=150)
        self.ProductTable.column("price", width=100)
        self.ProductTable.column("cost", width=100)
        self.ProductTable.column("quantity", width=80)
        self.ProductTable.column("unit", width=80)
        self.ProductTable.column("category", width=120)
        self.ProductTable.column("supplier", width=120)
        self.ProductTable.column("reorder_level", width=100)
        self.ProductTable.column("status", width=80)
        self.ProductTable.column("description", width=200)
        self.ProductTable.column("created_date", width=120)
        
        self.ProductTable.pack(fill=BOTH, expand=1)
        
        # Bind selection event
        self.ProductTable.bind("<<TreeviewSelect>>", self.select_data)
        
        # Load initial data
        self.show()

    # ==================== Helper Functions ====================
    
    def load_categories(self):
        """Load categories into combobox"""
        try:
            con = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="ims")
            cur = con.cursor()
            cur.execute("SELECT cid, name FROM category WHERE status='Active'")
            rows = cur.fetchall()
            categories = []
            for row in rows:
                categories.append(f"{row[0]} - {row[1]}")
            self.cmb_category['values'] = categories
            con.close()
        except:
            self.cmb_category['values'] = []
    
    def load_suppliers(self):
        """Load suppliers into combobox"""
        try:
            con = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="ims")
            cur = con.cursor()
            cur.execute("SELECT sid, name FROM supplier WHERE status='Active'")
            rows = cur.fetchall()
            suppliers = []
            for row in rows:
                suppliers.append(f"{row[0]} - {row[1]}")
            self.cmb_supplier['values'] = suppliers
            con.close()
        except:
            self.cmb_supplier['values'] = []

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
            
            if self.var_product_id.get() == "":
                messagebox.showerror("Error", "Product ID is required", parent=self.root)
                return
            
            if self.var_name.get() == "":
                messagebox.showerror("Error", "Product Name is required", parent=self.root)
                return
            
            if self.var_category_id.get() == "" or self.var_category_id.get() == "Select":
                messagebox.showerror("Error", "Please select a category", parent=self.root)
                return
            
            if self.var_supplier_id.get() == "" or self.var_supplier_id.get() == "Select":
                messagebox.showerror("Error", "Please select a supplier", parent=self.root)
                return
            
            if self.var_status.get() == "Select":
                messagebox.showerror("Error", "Please select status", parent=self.root)
                return
            
            # Extract IDs from combobox selections
            category_id = self.var_category_id.get().split(" - ")[0]
            supplier_id = self.var_supplier_id.get().split(" - ")[0]
            
            # Check if product ID already exists
            cur.execute("SELECT * FROM product WHERE pid=%s", (self.var_product_id.get(),))
            row = cur.fetchone()
            if row is not None:
                messagebox.showerror("Error", "This Product ID is already assigned", parent=self.root)
            else:
                cur.execute("""INSERT INTO product (pid, name, price, cost, quantity, unit, 
                              category_id, supplier_id, reorder_level, status, description, created_date) 
                              VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                             (
                                self.var_product_id.get(),
                                self.var_name.get(),
                                float(self.var_price.get()) if self.var_price.get() else 0,
                                float(self.var_cost.get()) if self.var_cost.get() else 0,
                                int(self.var_quantity.get()) if self.var_quantity.get() else 0,
                                self.var_unit.get(),
                                category_id,
                                supplier_id,
                                int(self.var_reorder_level.get()) if self.var_reorder_level.get() else 5,
                                self.var_status.get(),
                                self.txt_description.get("1.0", END).strip(),
                                datetime.now().date()
                             ))
                con.commit()
                messagebox.showinfo("Success", "Product added successfully", parent=self.root)
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
            
            if self.var_product_id.get() == "":
                messagebox.showerror("Error", "Product ID is required", parent=self.root)
                return
            
            if self.var_status.get() == "Select":
                messagebox.showerror("Error", "Please select status", parent=self.root)
                return
            
            # Extract IDs from combobox selections
            category_id = self.var_category_id.get().split(" - ")[0] if self.var_category_id.get() else ""
            supplier_id = self.var_supplier_id.get().split(" - ")[0] if self.var_supplier_id.get() else ""
            
            cur.execute("""UPDATE product SET name=%s, price=%s, cost=%s, quantity=%s, unit=%s,
                          category_id=%s, supplier_id=%s, reorder_level=%s, status=%s, description=%s 
                          WHERE pid=%s""",
                         (
                            self.var_name.get(),
                            float(self.var_price.get()) if self.var_price.get() else 0,
                            float(self.var_cost.get()) if self.var_cost.get() else 0,
                            int(self.var_quantity.get()) if self.var_quantity.get() else 0,
                            self.var_unit.get(),
                            category_id,
                            supplier_id,
                            int(self.var_reorder_level.get()) if self.var_reorder_level.get() else 5,
                            self.var_status.get(),
                            self.txt_description.get("1.0", END).strip(),
                            self.var_product_id.get()
                         ))
            con.commit()
            messagebox.showinfo("Success", "Product updated successfully", parent=self.root)
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
            
            if self.var_product_id.get() == "":
                messagebox.showerror("Error", "Please select a product to delete", parent=self.root)
                return
            
            # Confirm deletion
            if messagebox.askyesno("Confirm", "Are you sure you want to delete this product?\nThis action cannot be undone!", parent=self.root):
                cur.execute("DELETE FROM product WHERE pid=%s", (self.var_product_id.get(),))
                con.commit()
                messagebox.showinfo("Success", "Product deleted successfully", parent=self.root)
                self.show()
                self.clear()
            
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            if con and con.is_connected():
                con.close()

    def clear(self):
        """Clear all input fields"""
        self.var_product_id.set("")
        self.var_name.set("")
        self.var_price.set("")
        self.var_cost.set("")
        self.var_quantity.set("")
        self.var_unit.set("Select")
        self.var_category_id.set("")
        self.var_supplier_id.set("")
        self.var_reorder_level.set("")
        self.var_status.set("Select")
        self.txt_description.delete("1.0", END)
        self.var_searchby.set("Select")
        self.var_searchtxt.set("")
        self.load_categories()
        self.load_suppliers()

    def show(self):
        """Display all products in the table"""
        con = None
        try:
            con = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="ims")
            cur = con.cursor()
            
            # Clear existing data
            for item in self.ProductTable.get_children():
                self.ProductTable.delete(item)
            
            # Fetch all products with category and supplier names
            cur.execute("""SELECT p.pid, p.name, p.price, p.cost, p.quantity, p.unit, 
                          c.name, s.name, p.reorder_level, p.status, p.description, p.created_date 
                          FROM product p
                          LEFT JOIN category c ON p.category_id = c.cid
                          LEFT JOIN supplier s ON p.supplier_id = s.sid
                          ORDER BY p.created_date DESC""")
            rows = cur.fetchall()
            for row in rows:
                # Format price and cost with Rs symbol
                values = list(row)
                if values[2]:
                    values[2] = f"Rs {float(values[2]):,.2f}"
                if values[3]:
                    values[3] = f"Rs {float(values[3]):,.2f}"
                self.ProductTable.insert('', END, values=tuple(values))
                
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            if con and con.is_connected():
                con.close()

    def search(self):
        """Search for products based on criteria"""
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
            for item in self.ProductTable.get_children():
                self.ProductTable.delete(item)
            
            # Search based on criteria
            if search_by == "Product ID":
                query = """SELECT p.pid, p.name, p.price, p.cost, p.quantity, p.unit, 
                          c.name, s.name, p.reorder_level, p.status, p.description, p.created_date 
                          FROM product p
                          LEFT JOIN category c ON p.category_id = c.cid
                          LEFT JOIN supplier s ON p.supplier_id = s.sid
                          WHERE p.pid LIKE %s ORDER BY p.created_date DESC"""
                cur.execute(query, (f"%{search_txt}%",))
            elif search_by == "Name":
                query = """SELECT p.pid, p.name, p.price, p.cost, p.quantity, p.unit, 
                          c.name, s.name, p.reorder_level, p.status, p.description, p.created_date 
                          FROM product p
                          LEFT JOIN category c ON p.category_id = c.cid
                          LEFT JOIN supplier s ON p.supplier_id = s.sid
                          WHERE p.name LIKE %s ORDER BY p.created_date DESC"""
                cur.execute(query, (f"%{search_txt}%",))
            elif search_by == "Category":
                query = """SELECT p.pid, p.name, p.price, p.cost, p.quantity, p.unit, 
                          c.name, s.name, p.reorder_level, p.status, p.description, p.created_date 
                          FROM product p
                          LEFT JOIN category c ON p.category_id = c.cid
                          LEFT JOIN supplier s ON p.supplier_id = s.sid
                          WHERE c.name LIKE %s ORDER BY p.created_date DESC"""
                cur.execute(query, (f"%{search_txt}%",))
            elif search_by == "Supplier":
                query = """SELECT p.pid, p.name, p.price, p.cost, p.quantity, p.unit, 
                          c.name, s.name, p.reorder_level, p.status, p.description, p.created_date 
                          FROM product p
                          LEFT JOIN category c ON p.category_id = c.cid
                          LEFT JOIN supplier s ON p.supplier_id = s.sid
                          WHERE s.name LIKE %s ORDER BY p.created_date DESC"""
                cur.execute(query, (f"%{search_txt}%",))
            else:
                messagebox.showerror("Error", "Invalid search criteria", parent=self.root)
                return
            
            rows = cur.fetchall()
            
            if len(rows) == 0:
                messagebox.showinfo("Info", f"No product found with {search_by}: '{search_txt}'", parent=self.root)
                self.show()
            else:
                for row in rows:
                    values = list(row)
                    if values[2]:
                        values[2] = f"Rs {float(values[2]):,.2f}"
                    if values[3]:
                        values[3] = f"Rs {float(values[3]):,.2f}"
                    self.ProductTable.insert('', END, values=tuple(values))
                    
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            if con and con.is_connected():
                con.close()

    def select_data(self, event):
        """Load selected product data into input fields"""
        try:
            # Get selected item
            selected = self.ProductTable.focus()
            if selected:
                values = self.ProductTable.item(selected, 'values')
                
                # Set values to entry fields
                self.var_product_id.set(values[0])
                self.var_name.set(values[1])
                # Remove Rs symbol and commas from price
                price_value = values[2].replace("Rs ", "").replace(",", "") if values[2] else ""
                self.var_price.set(price_value)
                cost_value = values[3].replace("Rs ", "").replace(",", "") if values[3] else ""
                self.var_cost.set(cost_value)
                self.var_quantity.set(values[4])
                self.var_unit.set(values[5])
                
                # Set category (need to find the ID from name)
                category_name = values[6]
                if category_name:
                    # Load categories to get the ID
                    self.load_categories()
                    for cat in self.cmb_category['values']:
                        if category_name in cat:
                            self.var_category_id.set(cat)
                            break
                
                # Set supplier
                supplier_name = values[7]
                if supplier_name:
                    self.load_suppliers()
                    for sup in self.cmb_supplier['values']:
                        if supplier_name in sup:
                            self.var_supplier_id.set(sup)
                            break
                
                self.var_reorder_level.set(values[8])
                self.var_status.set(values[9])
                self.txt_description.delete("1.0", END)
                self.txt_description.insert("1.0", values[10])
                
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)


# Database setup function
def setup_product_database():
    """Create product table if not exists"""
    try:
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="")
        cur = con.cursor()
        
        # Create database if not exists
        cur.execute("CREATE DATABASE IF NOT EXISTS ims")
        cur.execute("USE ims")
        
        # Create product table
        cur.execute("""CREATE TABLE IF NOT EXISTS product (
            pid VARCHAR(50) PRIMARY KEY,
            name VARCHAR(200) NOT NULL,
            price DECIMAL(10,2) DEFAULT 0,
            cost DECIMAL(10,2) DEFAULT 0,
            quantity INT DEFAULT 0,
            unit VARCHAR(20),
            category_id VARCHAR(50),
            supplier_id VARCHAR(50),
            reorder_level INT DEFAULT 5,
            status VARCHAR(20) DEFAULT 'Active',
            description TEXT,
            created_date DATE,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES category(cid) ON DELETE SET NULL,
            FOREIGN KEY (supplier_id) REFERENCES supplier(sid) ON DELETE SET NULL
        )""")
        
        con.close()
        print("Product table setup completed successfully!")
        
    except Exception as ex:
        print(f"Database setup error: {ex}")


if __name__ == "__main__":
    # Setup database
    setup_product_database()
    
    # Run the application
    root = Tk()
    obj = productClass(root)
    root.mainloop()
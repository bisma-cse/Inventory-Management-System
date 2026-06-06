from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime

class supplierClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Supplier Management System")
        self.root.config(bg="#F5F6FA")
        self.root.focus_force()
        
        # Make window resizable and scrollable
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Create main container with scrollbar
        self.main_container = Frame(self.root, bg="#F5F6FA")
        self.main_container.grid(row=0, column=0, sticky="nsew")
        
        # Create canvas for scrolling
        self.canvas = Canvas(self.main_container, bg="#F5F6FA", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.main_container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas, bg="#F5F6FA")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=self.main_container.winfo_width())
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Bind resize event
        self.canvas.bind('<Configure>', self.on_canvas_configure)
        
        # Pack scrollbar and canvas
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Enable mouse wheel scrolling
        self.bind_mousewheel()

        # ==================== Variables ====================
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        self.var_supplier_id = StringVar()
        self.var_name = StringVar()
        self.var_contact = StringVar()
        self.var_email = StringVar()
        self.var_phone = StringVar()
        self.var_mobile = StringVar()
        self.var_company = StringVar()
        self.var_website = StringVar()
        self.var_credit_limit = StringVar()
        self.var_payment_terms = StringVar()
        self.var_status = StringVar()

        # ==================== Title Bar ====================
        title_bar = Frame(self.scrollable_frame, bg="#2C3E50", height=60)
        title_bar.pack(fill=X)
        title_bar.pack_propagate(False)
        
        title = Label(title_bar, text="🏢 SUPPLIER MANAGEMENT SYSTEM", 
                     font=("Segoe UI", 20, "bold"), 
                     fg="white", bg="#2C3E50")
        title.pack(pady=12)
        
        # Subtitle
        subtitle = Label(title_bar, text="Manage your suppliers efficiently", 
                        font=("Segoe UI", 10), 
                        fg="#BDC3C7", bg="#2C3E50")
        subtitle.pack()

        # ==================== Main Content Frame ====================
        main_frame = Frame(self.scrollable_frame, bg="#F5F6FA")
        main_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

        # ==================== Left Frame - Supplier Details ====================
        left_frame = LabelFrame(main_frame, text="📝 Supplier Information", 
                                font=("Segoe UI", 12, "bold"), 
                                bg="white", fg="#2C3E50", bd=2, relief=RIDGE)
        left_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 10))

        # Row 1 - Supplier ID and Name
        lbl_supplier_id = Label(left_frame, text="Supplier ID *:", 
                                font=("Segoe UI", 11), bg="white", fg="#2C3E50")
        lbl_supplier_id.grid(row=0, column=0, padx=20, pady=15, sticky="w")
        
        txt_supplier_id = Entry(left_frame, textvariable=self.var_supplier_id, 
                                font=("Segoe UI", 11), bg="#FEF9E6", 
                                relief=SOLID, bd=1, width=20)
        txt_supplier_id.grid(row=0, column=1, padx=10, pady=15, sticky="w")
        
        lbl_name = Label(left_frame, text="Name *:", 
                        font=("Segoe UI", 11), bg="white", fg="#2C3E50")
        lbl_name.grid(row=0, column=2, padx=20, pady=15, sticky="w")
        
        txt_name = Entry(left_frame, textvariable=self.var_name, 
                        font=("Segoe UI", 11), bg="#FEF9E6",
                        relief=SOLID, bd=1, width=20)
        txt_name.grid(row=0, column=3, padx=10, pady=15, sticky="w")

        # Row 2 - Company and Contact Person
        lbl_company = Label(left_frame, text="Company Name:", 
                           font=("Segoe UI", 11), bg="white", fg="#2C3E50")
        lbl_company.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        
        txt_company = Entry(left_frame, textvariable=self.var_company, 
                           font=("Segoe UI", 11), bg="#FEF9E6",
                           relief=SOLID, bd=1, width=20)
        txt_company.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        
        lbl_contact = Label(left_frame, text="Contact Person:", 
                           font=("Segoe UI", 11), bg="white", fg="#2C3E50")
        lbl_contact.grid(row=1, column=2, padx=20, pady=10, sticky="w")
        
        txt_contact = Entry(left_frame, textvariable=self.var_contact, 
                           font=("Segoe UI", 11), bg="#FEF9E6",
                           relief=SOLID, bd=1, width=20)
        txt_contact.grid(row=1, column=3, padx=10, pady=10, sticky="w")

        # Row 3 - Email and Phone
        lbl_email = Label(left_frame, text="Email:", 
                         font=("Segoe UI", 11), bg="white", fg="#2C3E50")
        lbl_email.grid(row=2, column=0, padx=20, pady=10, sticky="w")
        
        txt_email = Entry(left_frame, textvariable=self.var_email, 
                         font=("Segoe UI", 11), bg="#FEF9E6",
                         relief=SOLID, bd=1, width=20)
        txt_email.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        
        lbl_phone = Label(left_frame, text="Phone:", 
                         font=("Segoe UI", 11), bg="white", fg="#2C3E50")
        lbl_phone.grid(row=2, column=2, padx=20, pady=10, sticky="w")
        
        txt_phone = Entry(left_frame, textvariable=self.var_phone, 
                         font=("Segoe UI", 11), bg="#FEF9E6",
                         relief=SOLID, bd=1, width=20)
        txt_phone.grid(row=2, column=3, padx=10, pady=10, sticky="w")

        # Row 4 - Mobile and Website
        lbl_mobile = Label(left_frame, text="Mobile:", 
                          font=("Segoe UI", 11), bg="white", fg="#2C3E50")
        lbl_mobile.grid(row=3, column=0, padx=20, pady=10, sticky="w")
        
        txt_mobile = Entry(left_frame, textvariable=self.var_mobile, 
                          font=("Segoe UI", 11), bg="#FEF9E6",
                          relief=SOLID, bd=1, width=20)
        txt_mobile.grid(row=3, column=1, padx=10, pady=10, sticky="w")
        
        lbl_website = Label(left_frame, text="Website:", 
                           font=("Segoe UI", 11), bg="white", fg="#2C3E50")
        lbl_website.grid(row=3, column=2, padx=20, pady=10, sticky="w")
        
        txt_website = Entry(left_frame, textvariable=self.var_website, 
                           font=("Segoe UI", 11), bg="#FEF9E6",
                           relief=SOLID, bd=1, width=20)
        txt_website.grid(row=3, column=3, padx=10, pady=10, sticky="w")

        # Row 5 - Credit Limit (in Rs) and Status
        lbl_credit = Label(left_frame, text="Credit Limit (Rs):", 
                          font=("Segoe UI", 11), bg="white", fg="#2C3E50")
        lbl_credit.grid(row=4, column=0, padx=20, pady=10, sticky="w")
        
        txt_credit = Entry(left_frame, textvariable=self.var_credit_limit, 
                          font=("Segoe UI", 11), bg="#FEF9E6",
                          relief=SOLID, bd=1, width=20)
        txt_credit.grid(row=4, column=1, padx=10, pady=10, sticky="w")
        
        lbl_status = Label(left_frame, text="Status:", 
                          font=("Segoe UI", 11), bg="white", fg="#2C3E50")
        lbl_status.grid(row=4, column=2, padx=20, pady=10, sticky="w")
        
        cmb_status = ttk.Combobox(left_frame, textvariable=self.var_status, 
                                  values=("🟢 Active", "🔴 Inactive"), 
                                  state='readonly', font=("Segoe UI", 11), width=18)
        cmb_status.grid(row=4, column=3, padx=10, pady=10, sticky="w")
        cmb_status.current(0)

        # Row 6 - Payment Terms
        lbl_payment = Label(left_frame, text="Payment Terms *:", 
                           font=("Segoe UI", 11), bg="white", fg="#2C3E50")
        lbl_payment.grid(row=5, column=0, padx=20, pady=10, sticky="w")
        
        cmb_payment = ttk.Combobox(left_frame, textvariable=self.var_payment_terms, 
                                   values=(
                                       "Cash on Delivery (COD)",
                                       "Advance Payment",
                                       "Letter of Credit (LC)",
                                       "Weekly Payment",
                                       "Monthly Payment",
                                       "Quarterly Payment",
                                       "Half-Yearly Payment",
                                       "Yearly Payment"
                                   ), 
                                   state='readonly', font=("Segoe UI", 11), width=35)
        cmb_payment.grid(row=5, column=1, columnspan=3, padx=10, pady=10, sticky="w")
        cmb_payment.current(0)

        # Row 7 - Address
        lbl_address = Label(left_frame, text="Address:", 
                           font=("Segoe UI", 11), bg="white", fg="#2C3E50")
        lbl_address.grid(row=6, column=0, padx=20, pady=10, sticky="nw")
        
        self.txt_address = Text(left_frame, font=("Segoe UI", 11), 
                                bg="#FEF9E6", height=4, width=55,
                                relief=SOLID, bd=1)
        self.txt_address.grid(row=6, column=1, columnspan=3, padx=10, pady=10, sticky="w")

        # ==================== Right Frame - Buttons ====================
        right_frame = LabelFrame(main_frame, text="⚡ Actions", 
                                 font=("Segoe UI", 12, "bold"), 
                                 bg="white", fg="#2C3E50", bd=2, relief=RIDGE)
        right_frame.pack(side=RIGHT, fill=Y, padx=(10, 0))

        # Statistics Panel
        stats_frame = Frame(right_frame, bg="#ECF0F1", bd=1, relief=RIDGE)
        stats_frame.pack(pady=15, padx=15, fill=X)
        
        self.total_suppliers_label = Label(stats_frame, text="Total Suppliers: 0", 
                                          font=("Segoe UI", 13, "bold"), 
                                          bg="#ECF0F1", fg="#2C3E50")
        self.total_suppliers_label.pack(pady=10)
        
        self.active_suppliers_label = Label(stats_frame, text="Active: 0", 
                                           font=("Segoe UI", 11), 
                                           bg="#ECF0F1", fg="#27AE60")
        self.active_suppliers_label.pack(pady=5)
        
        self.inactive_suppliers_label = Label(stats_frame, text="Inactive: 0", 
                                             font=("Segoe UI", 11), 
                                             bg="#ECF0F1", fg="#E74C3C")
        self.inactive_suppliers_label.pack(pady=5)

        # Action Buttons
        btn_add = Button(right_frame, text="➕ Add Supplier", command=self.add,
                        font=("Segoe UI", 12, "bold"), bg="#2ECC71", 
                        fg="white", cursor="hand2", width=20, height=2,
                        relief=RAISED, bd=2)
        btn_add.pack(pady=10, padx=15)
        
        btn_update = Button(right_frame, text="✏️ Update Supplier", command=self.update,
                           font=("Segoe UI", 12, "bold"), bg="#3498DB", 
                           fg="white", cursor="hand2", width=20, height=2,
                           relief=RAISED, bd=2)
        btn_update.pack(pady=10, padx=15)
        
        btn_delete = Button(right_frame, text="🗑️ Delete Supplier", command=self.delete,
                           font=("Segoe UI", 12, "bold"), bg="#E74C3C", 
                           fg="white", cursor="hand2", width=20, height=2,
                           relief=RAISED, bd=2)
        btn_delete.pack(pady=10, padx=15)
        
        btn_clear = Button(right_frame, text="🔄 Clear All", command=self.clear,
                          font=("Segoe UI", 12, "bold"), bg="#95A5A6", 
                          fg="white", cursor="hand2", width=20, height=2,
                          relief=RAISED, bd=2)
        btn_clear.pack(pady=10, padx=15)
        
        btn_refresh = Button(right_frame, text="🔄 Refresh", command=self.show,
                            font=("Segoe UI", 12, "bold"), bg="#3498DB", 
                            fg="white", cursor="hand2", width=20, height=2,
                            relief=RAISED, bd=2)
        btn_refresh.pack(pady=10, padx=15)
        
        # Quick Info Panel
        info_frame = Frame(right_frame, bg="#FFF3E0", bd=2, relief=RIDGE)
        info_frame.pack(pady=15, padx=15, fill=X)
        
        info_label = Label(info_frame, text="💡 Quick Tips:", 
                          font=("Segoe UI", 10, "bold"), 
                          bg="#FFF3E0", fg="#E67E22")
        info_label.pack(pady=5)
        
        tip_label = Label(info_frame, 
                         text="• Click on any row to load data\n• Fields with * are required\n• Use Refresh button to update list", 
                         font=("Segoe UI", 9), bg="#FFF3E0", fg="#2C3E50", justify=LEFT)
        tip_label.pack(pady=5)

        # ==================== Supplier Table Frame ====================
        table_frame = LabelFrame(self.scrollable_frame, text="📋 Supplier List", 
                                 font=("Segoe UI", 12, "bold"), 
                                 bg="white", fg="#2C3E50", bd=2, relief=RIDGE)
        table_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

        # Scrollbars
        scrolly = Scrollbar(table_frame, orient=VERTICAL)
        scrollx = Scrollbar(table_frame, orient=HORIZONTAL)

        # Treeview
        self.SupplierTable = ttk.Treeview(table_frame, 
                                          columns=("sid", "name", "company", "email", 
                                                  "phone", "mobile", "contact", "status", 
                                                  "credit_limit", "payment_terms", "address"),
                                          yscrollcommand=scrolly.set, 
                                          xscrollcommand=scrollx.set,
                                          height=8)
        
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.SupplierTable.xview)
        scrolly.config(command=self.SupplierTable.yview)

        # Define headings
        self.SupplierTable.heading("sid", text="Supplier ID")
        self.SupplierTable.heading("name", text="Name")
        self.SupplierTable.heading("company", text="Company")
        self.SupplierTable.heading("email", text="Email")
        self.SupplierTable.heading("phone", text="Phone")
        self.SupplierTable.heading("mobile", text="Mobile")
        self.SupplierTable.heading("contact", text="Contact Person")
        self.SupplierTable.heading("status", text="Status")
        self.SupplierTable.heading("credit_limit", text="Credit Limit (Rs:)")
        self.SupplierTable.heading("payment_terms", text="Payment Terms")
        self.SupplierTable.heading("address", text="Address")

        self.SupplierTable["show"] = "headings"
        
        # Set column widths
        self.SupplierTable.column("sid", width=100)
        self.SupplierTable.column("name", width=120)
        self.SupplierTable.column("company", width=120)
        self.SupplierTable.column("email", width=150)
        self.SupplierTable.column("phone", width=100)
        self.SupplierTable.column("mobile", width=100)
        self.SupplierTable.column("contact", width=120)
        self.SupplierTable.column("status", width=80)
        self.SupplierTable.column("credit_limit", width=100)
        self.SupplierTable.column("payment_terms", width=120)
        self.SupplierTable.column("address", width=200)
        
        self.SupplierTable.pack(fill=BOTH, expand=1, padx=10, pady=10)
        
        # Bind selection event
        self.SupplierTable.bind("<<TreeviewSelect>>", self.select_data)
        
        # Load initial data
        self.show()
        self.update_stats()
        
        # Footer
        footer = Frame(self.scrollable_frame, bg="#2C3E50", height=40)
        footer.pack(fill=X, side=BOTTOM)
        footer.pack_propagate(False)
        
        footer_text = Label(footer, text="© 2024 Inventory Management System", 
                           font=("Segoe UI", 9), bg="#2C3E50", fg="#BDC3C7")
        footer_text.pack(pady=10)

    def on_canvas_configure(self, event):
        """Handle canvas resize"""
        self.canvas.itemconfig(1, width=event.width)
        
    def bind_mousewheel(self):
        """Bind mouse wheel for scrolling"""
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)
        
    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        if event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units")
        elif event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")
    
    def update_stats(self):
        """Update statistics display"""
        try:
            con = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="ims")
            cur = con.cursor()
            
            # Total suppliers
            cur.execute("SELECT COUNT(*) FROM supplier")
            total = cur.fetchone()[0]
            self.total_suppliers_label.config(text=f"Total Suppliers: {total}")
            
            # Active suppliers
            cur.execute("SELECT COUNT(*) FROM supplier WHERE status='Active'")
            active = cur.fetchone()[0]
            self.active_suppliers_label.config(text=f"🟢 Active: {active}")
            
            # Inactive suppliers
            cur.execute("SELECT COUNT(*) FROM supplier WHERE status='Inactive'")
            inactive = cur.fetchone()[0]
            self.inactive_suppliers_label.config(text=f"🔴 Inactive: {inactive}")
            
            con.close()
        except:
            pass
    
    def add(self):
        con = None
        try:
            con = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="ims")
            cur = con.cursor()
            
            if self.var_supplier_id.get() == "":
                messagebox.showerror("Error", "Supplier ID is required", parent=self.root)
                return
            
            if self.var_name.get() == "":
                messagebox.showerror("Error", "Supplier Name is required", parent=self.root)
                return
            
            # Check if supplier ID already exists
            cur.execute("SELECT * FROM supplier WHERE sid=%s", (self.var_supplier_id.get(),))
            row = cur.fetchone()
            if row is not None:
                messagebox.showerror("Error", "This Supplier ID is already assigned", parent=self.root)
            else:
                # Clean status value
                status = self.var_status.get().replace("🟢 ", "").replace("🔴 ", "")
                
                cur.execute("""INSERT INTO supplier (sid, name, company, email, phone, mobile, contact_person, 
                              status, credit_limit, payment_terms, address, created_date, website) 
                              VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                             (
                                self.var_supplier_id.get(),
                                self.var_name.get(),
                                self.var_company.get(),
                                self.var_email.get(),
                                self.var_phone.get(),
                                self.var_mobile.get(),
                                self.var_contact.get(),
                                status,
                                float(self.var_credit_limit.get()) if self.var_credit_limit.get() else 0,
                                self.var_payment_terms.get(),
                                self.txt_address.get("1.0", END).strip(),
                                datetime.now().date(),
                                self.var_website.get()
                             ))
                con.commit()
                messagebox.showinfo("Success", "Supplier added successfully", parent=self.root)
                self.show()
                self.update_stats()
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
            
            if self.var_supplier_id.get() == "":
                messagebox.showerror("Error", "Supplier ID is required", parent=self.root)
                return
            
            # Clean status value
            status = self.var_status.get().replace("🟢 ", "").replace("🔴 ", "")
            
            cur.execute("""UPDATE supplier SET name=%s, company=%s, email=%s, phone=%s, mobile=%s,
                          contact_person=%s, status=%s, credit_limit=%s, 
                          payment_terms=%s, address=%s, website=%s WHERE sid=%s""",
                         (
                            self.var_name.get(),
                            self.var_company.get(),
                            self.var_email.get(),
                            self.var_phone.get(),
                            self.var_mobile.get(),
                            self.var_contact.get(),
                            status,
                            float(self.var_credit_limit.get()) if self.var_credit_limit.get() else 0,
                            self.var_payment_terms.get(),
                            self.txt_address.get("1.0", END).strip(),
                            self.var_website.get(),
                            self.var_supplier_id.get()
                         ))
            con.commit()
            messagebox.showinfo("Success", "Supplier updated successfully", parent=self.root)
            self.show()
            self.update_stats()
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
            
            if self.var_supplier_id.get() == "":
                messagebox.showerror("Error", "Please select a supplier to delete", parent=self.root)
                return
            
            # Confirm deletion
            if messagebox.askyesno("Confirm", f"Are you sure you want to delete supplier {self.var_supplier_id.get()}?\nThis action cannot be undone!", parent=self.root):
                cur.execute("DELETE FROM supplier WHERE sid=%s", (self.var_supplier_id.get(),))
                con.commit()
                messagebox.showinfo("Success", "Supplier deleted successfully", parent=self.root)
                self.show()
                self.update_stats()
                self.clear()
            
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            if con and con.is_connected():
                con.close()

    def clear(self):
        """Clear all input fields"""
        self.var_supplier_id.set("")
        self.var_name.set("")
        self.var_company.set("")
        self.var_email.set("")
        self.var_phone.set("")
        self.var_mobile.set("")
        self.var_contact.set("")
        self.var_website.set("")
        self.var_credit_limit.set("")
        self.var_payment_terms.set("Cash on Delivery (COD)")
        self.var_status.set("🟢 Active")
        self.txt_address.delete("1.0", END)

    def show(self):
        """Display all suppliers in the table"""
        con = None
        try:
            con = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="ims")
            cur = con.cursor()
            
            # Clear existing data
            for item in self.SupplierTable.get_children():
                self.SupplierTable.delete(item)
            
            # Fetch all suppliers
            cur.execute("SELECT sid, name, company, email, phone, mobile, contact_person, status, credit_limit, payment_terms, address FROM supplier ORDER BY created_date DESC")
            rows = cur.fetchall()
            for row in rows:
                # Add status icon
                status_with_icon = "🟢 " + row[7] if row[7] == "Active" else "🔴 " + row[7]
                values = list(row)
                values[7] = status_with_icon
                # Format credit limit with Rs: symbol
                if values[8]:
                    values[8] = f"Rs: {float(values[8]):,.2f}"
                else:
                    values[8] = "₹ 0.00"
                self.SupplierTable.insert('', END, values=tuple(values))
                
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            if con and con.is_connected():
                con.close()

    def select_data(self, event):
        """Load selected supplier data into input fields"""
        try:
            # Get selected item
            selected = self.SupplierTable.focus()
            if selected:
                values = self.SupplierTable.item(selected, 'values')
                
                # Set values to entry fields
                self.var_supplier_id.set(values[0])
                self.var_name.set(values[1])
                self.var_company.set(values[2])
                self.var_email.set(values[3])
                self.var_phone.set(values[4])
                self.var_mobile.set(values[5])
                self.var_contact.set(values[6])
                self.var_status.set(values[7])  # Already includes icon
                # Remove ₹ symbol and commas from credit limit
                if values[8] and values[8] != "Rs: 0.00":
                    credit_value = values[8].replace("Rs: ", "").replace(",", "")
                    self.var_credit_limit.set(credit_value)
                else:
                    self.var_credit_limit.set("")
                self.var_payment_terms.set(values[9])
                self.txt_address.delete("1.0", END)
                self.txt_address.insert("1.0", values[10])
                
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)


# Database setup function
def setup_supplier_database():
    """Create supplier table if not exists"""
    try:
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="")
        cur = con.cursor()
        
        # Create database if not exists
        cur.execute("CREATE DATABASE IF NOT EXISTS ims")
        cur.execute("USE ims")
        
        # Drop old table if exists
        cur.execute("DROP TABLE IF EXISTS supplier")
        
        # Create new supplier table
        cur.execute("""CREATE TABLE IF NOT EXISTS supplier (
            sid VARCHAR(50) PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            company VARCHAR(100),
            email VARCHAR(100),
            phone VARCHAR(20),
            mobile VARCHAR(20),
            contact_person VARCHAR(100),
            status VARCHAR(20) DEFAULT 'Active',
            credit_limit DECIMAL(10,2) DEFAULT 0,
            payment_terms VARCHAR(100),
            address TEXT,
            website VARCHAR(100),
            created_date DATE,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )""")
        
        con.close()
        print("Supplier table setup completed successfully!")
        
    except Exception as ex:
        print(f"Database setup error: {ex}")


if __name__ == "__main__":
    # Setup database
    setup_supplier_database()
    
    # Run the application
    root = Tk()
    obj = supplierClass(root)
    root.mainloop()
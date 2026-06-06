from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime

class NewSaleClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1300x750+100+50")
        self.root.title("New Sale - POS System")
        self.root.config(bg="#F5F6FA")
        self.root.focus_force()

        # ==================== Variables ====================
        self.var_invoice_no = StringVar()
        self.var_customer_name = StringVar()
        self.var_customer_phone = StringVar()
        self.var_product_id = StringVar()
        self.var_product_name = StringVar()
        self.var_price = StringVar()
        self.var_quantity = StringVar()
        self.var_discount = StringVar()
        self.var_tax = StringVar()
        self.var_payment_method = StringVar()
        self.var_search_option = StringVar(value="Product Name")
        
        self.cart_items = []
        self.current_stock = 0  # Store current stock value
        
        # ==================== Title Bar ====================
        title_bar = Frame(self.root, bg="#2C3E50", height=50)
        title_bar.pack(fill=X)
        title_bar.pack_propagate(False)
        
        title = Label(title_bar, text="🛒 POINT OF SALE SYSTEM", 
                     font=("Segoe UI", 18, "bold"), 
                     fg="white", bg="#2C3E50")
        title.pack(pady=10)
        
        # Generate Invoice Number
        self.generate_invoice_no()

        # ==================== Main Content ====================
        main_content = Frame(self.root, bg="#F5F6FA")
        main_content.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # ==================== Left Panel - Product Selection ====================
        left_panel = LabelFrame(main_content, text="📦 Product Selection", 
                                font=("Segoe UI", 11, "bold"), 
                                bg="white", fg="#2C3E50", bd=2, relief=RIDGE)
        left_panel.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 10))

        # Search Product Section
        search_frame = Frame(left_panel, bg="white", relief=GROOVE, bd=1)
        search_frame.pack(fill=X, padx=8, pady=8)
        
        Label(search_frame, text="Search:", font=("Segoe UI", 10), 
              bg="white", fg="#2C3E50").pack(side=LEFT, padx=5)
        
        # Search option radio buttons
        Radiobutton(search_frame, text="ID", variable=self.var_search_option, 
                   value="Product ID", bg="white", font=("Segoe UI", 9),
                   command=self.on_search_option_change).pack(side=LEFT, padx=2)
        Radiobutton(search_frame, text="Name", variable=self.var_search_option, 
                   value="Product Name", bg="white", font=("Segoe UI", 9),
                   command=self.on_search_option_change).pack(side=LEFT, padx=2)
        
        # Product Combobox
        self.cmb_products = ttk.Combobox(search_frame, textvariable=self.var_product_id,
                                         font=("Segoe UI", 10), width=25)
        self.cmb_products.pack(side=LEFT, padx=5)
        self.cmb_products.bind('<<ComboboxSelected>>', self.on_product_select)
        
        btn_find = Button(search_frame, text="Load", command=self.load_selected_product,
                         font=("Segoe UI", 9), bg="#3498DB", 
                         fg="white", cursor="hand2", bd=0, padx=12, pady=3)
        btn_find.pack(side=LEFT, padx=2)

        # Product Information Display
        info_frame = LabelFrame(left_panel, text="Product Information", 
                               font=("Segoe UI", 10, "bold"), 
                               bg="white", fg="#2C3E50", bd=2, relief=RIDGE)
        info_frame.pack(fill=X, padx=8, pady=8)
        
        details_frame = Frame(info_frame, bg="white")
        details_frame.pack(padx=10, pady=10)
        
        # Row 1
        Label(details_frame, text="Product ID:", font=("Segoe UI", 10), 
              bg="white", width=12, anchor='w').grid(row=0, column=0, pady=5, padx=5)
        self.lbl_pid = Label(details_frame, text="", font=("Segoe UI", 10, "bold"), 
                             bg="white", fg="#05536B", width=15, anchor='w')
        self.lbl_pid.grid(row=0, column=1, pady=5, padx=5)
        
        Label(details_frame, text="Name:", font=("Segoe UI", 10), 
              bg="white", width=12, anchor='w').grid(row=0, column=2, pady=5, padx=5)
        self.lbl_name = Label(details_frame, text="", font=("Segoe UI", 10, "bold"), 
                              bg="white", fg="#05536B", width=20, anchor='w')
        self.lbl_name.grid(row=0, column=3, pady=5, padx=5)
        
        # Row 2
        Label(details_frame, text="Price (Rs):", font=("Segoe UI", 10), 
              bg="white", width=12, anchor='w').grid(row=1, column=0, pady=5, padx=5)
        self.lbl_price = Label(details_frame, text="", font=("Segoe UI", 10, "bold"), 
                               bg="white", fg="#2ECC71", width=15, anchor='w')
        self.lbl_price.grid(row=1, column=1, pady=5, padx=5)
        
        Label(details_frame, text="Stock:", font=("Segoe UI", 10), 
              bg="white", width=12, anchor='w').grid(row=1, column=2, pady=5, padx=5)
        self.lbl_stock = Label(details_frame, text="", font=("Segoe UI", 10, "bold"), 
                               bg="white", fg="#E74C3C", width=10, anchor='w')
        self.lbl_stock.grid(row=1, column=3, pady=5, padx=5)
        
        # Row 3
        Label(details_frame, text="Unit:", font=("Segoe UI", 10), 
              bg="white", width=12, anchor='w').grid(row=2, column=0, pady=5, padx=5)
        self.lbl_unit = Label(details_frame, text="", font=("Segoe UI", 10), 
                              bg="white", fg="#2C3E50", width=15, anchor='w')
        self.lbl_unit.grid(row=2, column=1, pady=5, padx=5)
        
        Label(details_frame, text="Quantity:", font=("Segoe UI", 10, "bold"), 
              bg="white", fg="#E74C3C", width=12, anchor='w').grid(row=2, column=2, pady=5, padx=5)
        self.txt_quantity = Entry(details_frame, font=("Segoe UI", 10), bg="#FEF9E6", width=15)
        self.txt_quantity.grid(row=2, column=3, pady=5, padx=5)
        
        # Add to Cart Button
        btn_add = Button(left_panel, text="➕ ADD TO CART", command=self.add_to_cart,
                        font=("Segoe UI", 11, "bold"), bg="#2ECC71", 
                        fg="white", cursor="hand2", bd=0, pady=8)
        btn_add.pack(pady=8, padx=8, fill=X)

        # Customer Information
        customer_frame = LabelFrame(left_panel, text="Customer Information", 
                                   font=("Segoe UI", 10, "bold"), 
                                   bg="white", fg="#2C3E50", bd=2, relief=RIDGE)
        customer_frame.pack(fill=X, padx=8, pady=8)
        
        cust_frame = Frame(customer_frame, bg="white")
        cust_frame.pack(padx=10, pady=10)
        
        Label(cust_frame, text="Name *:", font=("Segoe UI", 10), 
              bg="white", width=10, anchor='w').grid(row=0, column=0, pady=5, padx=5)
        txt_customer = Entry(cust_frame, textvariable=self.var_customer_name, 
                            font=("Segoe UI", 10), bg="#FEF9E6", width=22)
        txt_customer.grid(row=0, column=1, pady=5, padx=5)
        
        Label(cust_frame, text="Phone:", font=("Segoe UI", 10), 
              bg="white", width=10, anchor='w').grid(row=0, column=2, pady=5, padx=5)
        txt_phone = Entry(cust_frame, textvariable=self.var_customer_phone, 
                         font=("Segoe UI", 10), bg="#FEF9E6", width=18)
        txt_phone.grid(row=0, column=3, pady=5, padx=5)

        # ==================== Right Panel - Cart ====================
        right_panel = LabelFrame(main_content, text="Shopping Cart", 
                                 font=("Segoe UI", 11, "bold"), 
                                 bg="white", fg="#2C3E50", bd=2, relief=RIDGE)
        right_panel.pack(side=RIGHT, fill=BOTH, expand=True)

        # Cart Table
        cart_frame = Frame(right_panel, bg="white")
        cart_frame.pack(fill=BOTH, expand=True, padx=8, pady=8)

        columns = ("pid", "name", "price", "qty", "total")
        self.CartTable = ttk.Treeview(cart_frame, columns=columns, show="headings", height=10)
        
        self.CartTable.heading("pid", text="ID")
        self.CartTable.heading("name", text="Product Name")
        self.CartTable.heading("price", text="Price")
        self.CartTable.heading("qty", text="Qty")
        self.CartTable.heading("total", text="Total")
        
        self.CartTable.column("pid", width=70)
        self.CartTable.column("name", width=180)
        self.CartTable.column("price", width=90)
        self.CartTable.column("qty", width=60)
        self.CartTable.column("total", width=100)
        
        scrollbar_cart = ttk.Scrollbar(cart_frame, orient=VERTICAL, command=self.CartTable.yview)
        self.CartTable.configure(yscrollcommand=scrollbar_cart.set)
        
        self.CartTable.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar_cart.pack(side=RIGHT, fill=Y)

        # Cart Action Buttons
        cart_btn_frame = Frame(right_panel, bg="white")
        cart_btn_frame.pack(fill=X, padx=8, pady=5)
        
        Button(cart_btn_frame, text="Remove", command=self.remove_from_cart,
              font=("Segoe UI", 9), bg="#E74C3C", fg="white", 
              cursor="hand2", bd=0, padx=15, pady=5).pack(side=LEFT, padx=5)
        
        Button(cart_btn_frame, text="Clear Cart", command=self.clear_cart,
              font=("Segoe UI", 9), bg="#95A5A6", fg="white", 
              cursor="hand2", bd=0, padx=15, pady=5).pack(side=LEFT, padx=5)

        # Bill Summary
        summary_frame = LabelFrame(right_panel, text="Bill Summary", 
                                  font=("Segoe UI", 10, "bold"), 
                                  bg="#ECF0F1", fg="#2C3E50", bd=2, relief=RIDGE)
        summary_frame.pack(fill=X, padx=8, pady=8)
        
        summary_inner = Frame(summary_frame, bg="#ECF0F1")
        summary_inner.pack(padx=15, pady=10)
        
        # Subtotal
        Label(summary_inner, text="Subtotal:", font=("Segoe UI", 11), 
              bg="#ECF0F1", width=12, anchor='w').grid(row=0, column=0, pady=5, padx=5)
        self.lbl_subtotal = Label(summary_inner, text="Rs 0.00", font=("Segoe UI", 11, "bold"), 
                                  bg="#ECF0F1", fg="#2C3E50", width=15, anchor='w')
        self.lbl_subtotal.grid(row=0, column=1, pady=5, padx=5)
        
        # Discount
        Label(summary_inner, text="Discount (%):", font=("Segoe UI", 10), 
              bg="#ECF0F1", width=12, anchor='w').grid(row=1, column=0, pady=5, padx=5)
        self.txt_discount = Entry(summary_inner, textvariable=self.var_discount, 
                                  font=("Segoe UI", 10), bg="white", width=12)
        self.txt_discount.grid(row=1, column=1, pady=5, padx=5)
        self.txt_discount.bind('<KeyRelease>', self.calculate_total)
        
        # Tax
        Label(summary_inner, text="Tax (%):", font=("Segoe UI", 10), 
              bg="#ECF0F1", width=12, anchor='w').grid(row=2, column=0, pady=5, padx=5)
        self.txt_tax = Entry(summary_inner, textvariable=self.var_tax, 
                             font=("Segoe UI", 10), bg="white", width=12)
        self.txt_tax.grid(row=2, column=1, pady=5, padx=5)
        self.txt_tax.bind('<KeyRelease>', self.calculate_total)
        
        # Grand Total
        Label(summary_inner, text="Grand Total:", font=("Segoe UI", 12, "bold"), 
              bg="#ECF0F1", fg="#E74C3C", width=12, anchor='w').grid(row=3, column=0, pady=8, padx=5)
        self.lbl_grand_total = Label(summary_inner, text="Rs 0.00", font=("Segoe UI", 12, "bold"), 
                                     bg="#ECF0F1", fg="#E74C3C", width=15, anchor='w')
        self.lbl_grand_total.grid(row=3, column=1, pady=8, padx=5)

        # Payment Section
        payment_frame = LabelFrame(right_panel, text="Payment Details", 
                                  font=("Segoe UI", 10, "bold"), 
                                  bg="white", fg="#2C3E50", bd=2, relief=RIDGE)
        payment_frame.pack(fill=X, padx=8, pady=8)
        
        payment_inner = Frame(payment_frame, bg="white")
        payment_inner.pack(padx=15, pady=10)
        
        Label(payment_inner, text="Payment:", font=("Segoe UI", 10), 
              bg="white", width=12, anchor='w').grid(row=0, column=0, pady=5, padx=5)
        
        self.cmb_payment = ttk.Combobox(payment_inner, textvariable=self.var_payment_method, 
                                        values=("Select", "Cash", "Credit Card", "Debit Card", 
                                               "Bank Transfer", "Mobile Payment"), 
                                        state='readonly', font=("Segoe UI", 10), width=16)
        self.cmb_payment.grid(row=0, column=1, pady=5, padx=5)
        self.cmb_payment.current(0)
        
        Label(payment_inner, text="Invoice No:", font=("Segoe UI", 10), 
              bg="white", width=12, anchor='w').grid(row=0, column=2, pady=5, padx=5)
        
        lbl_invoice = Label(payment_inner, textvariable=self.var_invoice_no, 
                           font=("Segoe UI", 10, "bold"), bg="#FEF9E6", 
                           fg="#05536B", width=18, relief=SUNKEN, bd=1)
        lbl_invoice.grid(row=0, column=3, pady=5, padx=5)

        # Action Buttons
        action_frame = Frame(payment_inner, bg="white")
        action_frame.grid(row=1, column=0, columnspan=4, pady=10)
        
        Button(action_frame, text="Complete Sale", command=self.complete_sale,
              font=("Segoe UI", 10, "bold"), bg="#2ECC71", fg="white", 
              cursor="hand2", bd=0, padx=15, pady=6).pack(side=LEFT, padx=5)
        
        Button(action_frame, text="Print", command=self.print_preview,
              font=("Segoe UI", 10, "bold"), bg="#9B59B6", fg="white", 
              cursor="hand2", bd=0, padx=15, pady=6).pack(side=LEFT, padx=5)
        
        Button(action_frame, text="New Sale", command=self.new_sale,
              font=("Segoe UI", 10, "bold"), bg="#F39C12", fg="white", 
              cursor="hand2", bd=0, padx=15, pady=6).pack(side=LEFT, padx=5)
        
        Button(action_frame, text="Close", command=self.close_window,
              font=("Segoe UI", 10, "bold"), bg="#E74C3C", fg="white", 
              cursor="hand2", bd=0, padx=15, pady=6).pack(side=LEFT, padx=5)

        # ==================== Status Bar ====================
        status_bar = Frame(self.root, bg="#2C3E50", height=30)
        status_bar.pack(fill=X, side=BOTTOM)
        status_bar.pack_propagate(False)
        
        self.status_label = Label(status_bar, text="Ready for new sale", 
                                  font=("Segoe UI", 9), bg="#2C3E50", fg="#BDC3C7")
        self.status_label.pack(side=LEFT, padx=10, pady=5)

        # Keyboard shortcuts
        self.root.bind('<F5>', lambda e: self.new_sale())
        self.root.bind('<F6>', lambda e: self.print_preview())
        self.root.bind('<Return>', lambda e: self.add_to_cart())
        self.txt_quantity.bind('<Return>', lambda e: self.add_to_cart())
        txt_customer.bind('<Return>', lambda e: self.cmb_payment.focus())
        
        # Load Products
        self.load_products()
        
        # Focus on product search
        self.cmb_products.focus()

    # ==================== All Functions ====================
    
    def update_status(self, message):
        """Update status bar message"""
        try:
            self.status_label.config(text=f"{message} | Invoice: {self.var_invoice_no.get()}")
            self.root.update_idletasks()
        except:
            pass
    
    def close_window(self):
        """Close the window"""
        if messagebox.askyesno("Confirm", "Are you sure you want to close?"):
            self.root.destroy()
    
    def load_products(self):
        """Load all products into combobox"""
        try:
            self.update_status("Loading products...")
            conn = mysql.connector.connect(
                host="localhost", user="root", password="", database="ims")
            cursor = conn.cursor()
            
            search_option = self.var_search_option.get()
            if search_option == "Product ID":
                cursor.execute("SELECT pid, name FROM product WHERE status='Active' ORDER BY pid")
            else:
                cursor.execute("SELECT pid, name FROM product WHERE status='Active' ORDER BY name")
            
            products = cursor.fetchall()
            product_list = [f"{p[0]} - {p[1]}" for p in products]
            self.cmb_products['values'] = product_list
            
            conn.close()
            self.update_status(f"Ready - {len(products)} products loaded")
        except Exception as ex:
            print(f"Error loading products: {ex}")
            self.update_status("Error loading products")
            self.cmb_products['values'] = []
    
    def on_search_option_change(self, event=None):
        """When search option changes, update combobox display"""
        self.cmb_products.set('')
        self.clear_product_info()
        self.load_products()
    
    def on_product_select(self, event=None):
        """When product is selected from combobox, load its details"""
        selected = self.cmb_products.get()
        if selected:
            product_id = selected.split(' - ')[0]
            self.load_product_by_id(product_id)
    
    def load_selected_product(self):
        """Load selected product from combobox"""
        selected = self.cmb_products.get()
        if selected:
            product_id = selected.split(' - ')[0]
            self.load_product_by_id(product_id)
        else:
            messagebox.showerror("Error", "Please select a product")
    
    def load_product_by_id(self, product_id):
        """Load product details by ID"""
        try:
            conn = mysql.connector.connect(
                host="localhost", user="root", password="", database="ims")
            cursor = conn.cursor()
            
            query = """SELECT pid, name, price, quantity, unit FROM product 
                      WHERE pid = %s AND status='Active'"""
            cursor.execute(query, (product_id,))
            row = cursor.fetchone()
            
            if row:
                self.lbl_pid.config(text=row[0])
                self.lbl_name.config(text=row[1])
                self.lbl_price.config(text=f"Rs {row[2]:,.2f}")
                self.lbl_stock.config(text=str(row[3]))
                self.current_stock = row[3]  # Store stock value
                self.lbl_unit.config(text=row[4])
                self.var_product_id.set(row[0])
                self.var_product_name.set(row[1])
                self.var_price.set(str(row[2]))
                self.txt_quantity.focus()
                self.update_status(f"Loaded: {row[1]}")
            else:
                messagebox.showinfo("Info", "Product not found!")
                self.clear_product_info()
            
            conn.close()
        except Exception as ex:
            messagebox.showerror("Error", f"Error: {str(ex)}")
    
    def generate_invoice_no(self):
        """Generate unique invoice number"""
        invoice_no = f"INV-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        self.var_invoice_no.set(invoice_no)
        return invoice_no
    
    def clear_product_info(self):
        """Clear product information display"""
        self.lbl_pid.config(text="")
        self.lbl_name.config(text="")
        self.lbl_price.config(text="")
        self.lbl_stock.config(text="")
        self.lbl_unit.config(text="")
        self.var_product_id.set("")
        self.var_product_name.set("")
        self.var_price.set("")
        self.current_stock = 0
        self.txt_quantity.delete(0, END)
    
    def add_to_cart(self):
        """Add selected product to cart - FIXED VERSION"""
        try:
            # Check if product is selected
            if not self.var_product_id.get():
                messagebox.showerror("Error", "Please select a product first")
                self.cmb_products.focus()
                return
            
            # Check quantity
            qty_str = self.txt_quantity.get().strip()
            if not qty_str:
                messagebox.showerror("Error", "Please enter quantity")
                self.txt_quantity.focus()
                return
            
            # Validate quantity
            try:
                qty = int(qty_str)
            except ValueError:
                messagebox.showerror("Error", "Invalid quantity! Please enter a valid number")
                self.txt_quantity.focus()
                return
            
            # Get stock from stored variable or label
            stock = self.current_stock
            if stock == 0:
                stock_text = self.lbl_stock.cget('text')
                if stock_text:
                    try:
                        stock = int(stock_text)
                    except:
                        stock = 0
            
            # Validate quantity range
            if qty <= 0:
                messagebox.showerror("Error", "Quantity must be greater than 0")
                self.txt_quantity.focus()
                return
            
            if qty > stock:
                messagebox.showerror("Error", f"Insufficient stock! Available: {stock}")
                self.txt_quantity.focus()
                return
            
            # Get product details
            product_id = self.var_product_id.get()
            product_name = self.var_product_name.get()
            price = float(self.var_price.get())
            
            # Check if product already in cart
            found = False
            for i, item in enumerate(self.cart_items):
                if item['pid'] == product_id:
                    new_qty = item['qty'] + qty
                    if new_qty > stock:
                        messagebox.showerror("Error", f"Cannot add more! Available stock: {stock}")
                        return
                    # Update existing item
                    self.cart_items[i]['qty'] = new_qty
                    self.cart_items[i]['total'] = new_qty * price
                    found = True
                    self.update_cart_display()
                    self.clear_product_info()
                    self.cmb_products.set('')
                    messagebox.showinfo("Success", f"Updated: {product_name} x{new_qty}")
                    self.update_status(f"Updated: {product_name} x{new_qty}")
                    return
            
            # Add new item to cart if not found
            if not found:
                cart_item = {
                    'pid': product_id,
                    'name': product_name,
                    'price': price,
                    'qty': qty,
                    'total': qty * price
                }
                self.cart_items.append(cart_item)
                self.update_cart_display()
                self.clear_product_info()
                self.cmb_products.set('')
                messagebox.showinfo("Success", f"Added: {product_name} x{qty}")
                self.update_status(f"Added: {product_name} x{qty}")
            
            self.cmb_products.focus()
            
        except Exception as ex:
            messagebox.showerror("Error", f"Error adding to cart: {str(ex)}")
    
    def update_cart_display(self):
        """Update cart table display"""
        # Clear existing items
        for item in self.CartTable.get_children():
            self.CartTable.delete(item)
        
        subtotal = 0
        for item in self.cart_items:
            self.CartTable.insert('', END, values=(
                item['pid'], 
                item['name'], 
                f"{item['price']:,.2f}", 
                item['qty'], 
                f"{item['total']:,.2f}"
            ))
            subtotal += item['total']
        
        self.lbl_subtotal.config(text=f"Rs {subtotal:,.2f}")
        self.calculate_total()
        self.update_status(f"Cart: {len(self.cart_items)} items, Rs {subtotal:,.2f}")
    
    def calculate_total(self, event=None):
        """Calculate grand total after discount and tax"""
        try:
            subtotal_text = self.lbl_subtotal.cget('text').replace("Rs ", "").replace(",", "")
            subtotal = float(subtotal_text) if subtotal_text else 0
            
            discount_percent = float(self.var_discount.get()) if self.var_discount.get() else 0
            tax_percent = float(self.var_tax.get()) if self.var_tax.get() else 0
            
            discount_amount = subtotal * (discount_percent / 100)
            tax_amount = (subtotal - discount_amount) * (tax_percent / 100)
            grand_total = subtotal - discount_amount + tax_amount
            
            self.lbl_grand_total.config(text=f"Rs {grand_total:,.2f}")
        except:
            pass
    
    def remove_from_cart(self):
        """Remove selected item from cart"""
        selected = self.CartTable.selection()
        if selected:
            values = self.CartTable.item(selected[0], 'values')
            if values:
                pid = values[0]
                for i, item in enumerate(self.cart_items):
                    if item['pid'] == pid:
                        del self.cart_items[i]
                        break
                self.update_cart_display()
                messagebox.showinfo("Success", "Item removed from cart")
                self.update_status("Item removed")
        else:
            messagebox.showerror("Error", "Please select an item to remove")
    
    def clear_cart(self):
        """Clear entire cart"""
        if self.cart_items:
            if messagebox.askyesno("Confirm", "Clear cart?"):
                self.cart_items = []
                self.update_cart_display()
                messagebox.showinfo("Success", "Cart cleared")
                self.update_status("Cart cleared")
    
    def complete_sale(self):
        """Complete the sale and save to database"""
        conn = None
        try:
            if not self.cart_items:
                messagebox.showerror("Error", "Cart is empty")
                return
            
            if not self.var_customer_name.get().strip():
                messagebox.showerror("Error", "Please enter customer name")
                return
            
            if self.var_payment_method.get() == "Select":
                messagebox.showerror("Error", "Please select payment method")
                return
            
            self.update_status("Processing sale...")
            
            conn = mysql.connector.connect(
                host="localhost", user="root", password="", database="ims")
            cursor = conn.cursor()
            
            grand_total_text = self.lbl_grand_total.cget('text').replace("Rs ", "").replace(",", "")
            grand_total = float(grand_total_text) if grand_total_text else 0
            
            discount_percent = float(self.var_discount.get()) if self.var_discount.get() else 0
            tax_percent = float(self.var_tax.get()) if self.var_tax.get() else 0
            
            # Insert into sales table
            cursor.execute("""INSERT INTO sales (invoice_no, sale_date, customer_name, customer_phone, 
                          total_amount, payment_method, discount_percent, tax_percent, created_by) 
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                        (self.var_invoice_no.get(), datetime.now(), self.var_customer_name.get(),
                         self.var_customer_phone.get(), grand_total, self.var_payment_method.get(),
                         discount_percent, tax_percent, "Cashier"))
            
            # Insert sale items and update stock
            for item in self.cart_items:
                cursor.execute("""INSERT INTO sale_items (invoice_no, product_id, quantity, price, total) 
                              VALUES (%s, %s, %s, %s, %s)""",
                            (self.var_invoice_no.get(), item['pid'], item['qty'], 
                             item['price'], item['total']))
                
                cursor.execute("UPDATE product SET quantity = quantity - %s WHERE pid = %s",
                           (item['qty'], item['pid']))
            
            conn.commit()
            
            self.update_status(f"Sale completed! Invoice: {self.var_invoice_no.get()}")
            
            result = messagebox.askyesno("Success", 
                f"Sale completed!\nInvoice: {self.var_invoice_no.get()}\nTotal: {self.lbl_grand_total.cget('text')}\n\nPrint invoice?")
            
            if result:
                self.print_invoice()
            
            self.new_sale()
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {str(err)}")
            if conn:
                conn.rollback()
            self.update_status("Sale failed")
        except Exception as ex:
            messagebox.showerror("Error", f"Error: {str(ex)}")
            if conn:
                conn.rollback()
            self.update_status("Sale failed")
        finally:
            if conn and conn.is_connected():
                conn.close()
    
    def print_preview(self):
        """Show print preview"""
        if not self.cart_items:
            messagebox.showerror("Error", "No items to print")
            return
        self.print_invoice()
    
    def print_invoice(self):
        """Display invoice in a new window"""
        invoice_win = Toplevel(self.root)
        invoice_win.title(f"Invoice - {self.var_invoice_no.get()}")
        invoice_win.geometry("500x600+350+100")
        invoice_win.config(bg="white")
        
        invoice_win.transient(self.root)
        invoice_win.grab_set()
        
        text_area = Text(invoice_win, font=("Courier", 10), wrap=WORD)
        text_area.pack(fill=BOTH, expand=True, padx=15, pady=15)
        
        # Calculate totals
        subtotal = sum(item['total'] for item in self.cart_items)
        discount_percent = float(self.var_discount.get()) if self.var_discount.get() else 0
        tax_percent = float(self.var_tax.get()) if self.var_tax.get() else 0
        discount_amount = subtotal * (discount_percent / 100)
        tax_amount = (subtotal - discount_amount) * (tax_percent / 100)
        grand_total = subtotal - discount_amount + tax_amount
        
        invoice_text = f"""
{'='*48}
                  INVOICE
{'='*48}

Invoice: {self.var_invoice_no.get()}
Date: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}
Customer: {self.var_customer_name.get()}
Phone: {self.var_customer_phone.get()}

{'='*48}
Items:
{'-'*48}
"""
        for item in self.cart_items:
            invoice_text += f"{item['name'][:25]:25} x{item['qty']:2} = Rs {item['total']:,.2f}\n"
        
        invoice_text += f"""
{'-'*48}
Subtotal: {' ' * 32} Rs {subtotal:,.2f}
Discount ({discount_percent:.0f}%): {' ' * 25} -Rs {discount_amount:,.2f}
Tax ({tax_percent:.0f}%): {' ' * 32} +Rs {tax_amount:,.2f}
{'='*48}
GRAND TOTAL: {' ' * 30} Rs {grand_total:,.2f}
{'='*48}

Payment: {self.var_payment_method.get()}

      Thank you for shopping with us!
{'='*48}
"""
        text_area.insert(1.0, invoice_text)
        text_area.config(state='disabled')
        
        Button(invoice_win, text="Close", command=invoice_win.destroy,
              font=("Segoe UI", 10), bg="#3498DB", fg="white", 
              cursor="hand2", padx=20, pady=5).pack(pady=10)
    
    def new_sale(self):
        """Reset all fields for new sale"""
        self.cart_items = []
        self.update_cart_display()
        self.clear_product_info()
        self.cmb_products.set('')
        self.var_customer_name.set("")
        self.var_customer_phone.set("")
        self.var_discount.set("")
        self.var_tax.set("")
        self.var_payment_method.set("Select")
        self.generate_invoice_no()
        self.lbl_subtotal.config(text="Rs 0.00")
        self.lbl_grand_total.config(text="Rs 0.00")
        self.load_products()
        self.update_status("Ready for new sale")
        self.cmb_products.focus()
        messagebox.showinfo("Success", "Ready for new sale")


# Database setup function
def setup_sales_tables():
    """Create sales tables if not exists"""
    try:
        conn = mysql.connector.connect(
            host="localhost", user="root", password="")
        cursor = conn.cursor()
        
        cursor.execute("CREATE DATABASE IF NOT EXISTS ims")
        cursor.execute("USE ims")
        
        # Create sales table
        cursor.execute("""CREATE TABLE IF NOT EXISTS sales (
            invoice_no VARCHAR(50) PRIMARY KEY,
            sale_date DATETIME,
            customer_name VARCHAR(100),
            customer_phone VARCHAR(20),
            total_amount DECIMAL(10,2),
            payment_method VARCHAR(50),
            discount_percent DECIMAL(5,2) DEFAULT 0,
            tax_percent DECIMAL(5,2) DEFAULT 0,
            created_by VARCHAR(50),
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")
        
        # Create sale_items table
        cursor.execute("""CREATE TABLE IF NOT EXISTS sale_items (
            id INT AUTO_INCREMENT PRIMARY KEY,
            invoice_no VARCHAR(50),
            product_id VARCHAR(50),
            quantity INT,
            price DECIMAL(10,2),
            total DECIMAL(10,2),
            FOREIGN KEY (invoice_no) REFERENCES sales(invoice_no) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES product(pid) ON DELETE SET NULL
        )""")
        
        conn.close()
        print("Sales tables setup completed!")
        
    except Exception as ex:
        print(f"Setup error: {ex}")


if __name__ == "__main__":
    setup_sales_tables()
    root = Tk()
    obj = NewSaleClass(root)
    root.mainloop()
from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime

class SalesHistoryClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1300x700+100+50")
        self.root.title("Sales History")
        self.root.config(bg="#F5F6FA")
        self.root.focus_force()

        # ==================== Variables ====================
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()
        self.var_from_date = StringVar()
        self.var_to_date = StringVar()
        
        # ==================== Title Bar ====================
        title_bar = Frame(self.root, bg="#2C3E50", height=50)
        title_bar.pack(fill=X)
        
        title = Label(title_bar, text="📊 SALES HISTORY - VIEW ALL TRANSACTIONS", 
                     font=("Segoe UI", 16, "bold"), 
                     fg="white", bg="#2C3E50")
        title.pack(pady=10)

        # ==================== Search Panel ====================
        search_panel = LabelFrame(self.root, text="🔍 Search Sales", 
                                  font=("Segoe UI", 11, "bold"), 
                                  bg="white", fg="#2C3E50", bd=2, relief=RIDGE)
        search_panel.pack(fill=X, padx=10, pady=10)

        # Row 1 - Search by
        row1 = Frame(search_panel, bg="white")
        row1.pack(fill=X, padx=10, pady=10)
        
        Label(row1, text="Search By:", font=("Segoe UI", 10), 
              bg="white", fg="#2C3E50").pack(side=LEFT, padx=5)
        
        cmb_search = ttk.Combobox(row1, textvariable=self.var_searchby, 
                                  values=("Select", "Invoice No", "Customer Name", "Customer Phone"), 
                                  state='readonly', font=("Segoe UI", 10), width=15)
        cmb_search.pack(side=LEFT, padx=5)
        cmb_search.current(0)
        
        Label(row1, text="Search Text:", font=("Segoe UI", 10), 
              bg="white", fg="#2C3E50").pack(side=LEFT, padx=5)
        
        txt_search = Entry(row1, textvariable=self.var_searchtxt, 
                          font=("Segoe UI", 10), bg="white", width=20)
        txt_search.pack(side=LEFT, padx=5)
        
        btn_search = Button(row1, text="🔍 Search", command=self.search_sales,
                           font=("Segoe UI", 9, "bold"), bg="#3498DB", 
                           fg="white", cursor="hand2", bd=0, padx=15, pady=5)
        btn_search.pack(side=LEFT, padx=5)
        
        btn_refresh = Button(row1, text="🔄 Refresh", command=self.load_sales,
                            font=("Segoe UI", 9, "bold"), bg="#2ECC71", 
                            fg="white", cursor="hand2", bd=0, padx=15, pady=5)
        btn_refresh.pack(side=LEFT, padx=5)

        # Row 2 - Date Range
        row2 = Frame(search_panel, bg="white")
        row2.pack(fill=X, padx=10, pady=10)
        
        Label(row2, text="From Date:", font=("Segoe UI", 10), 
              bg="white", fg="#2C3E50").pack(side=LEFT, padx=5)
        
        txt_from = Entry(row2, textvariable=self.var_from_date, 
                        font=("Segoe UI", 10), bg="#FEF9E6", width=15)
        txt_from.pack(side=LEFT, padx=5)
        
        Label(row2, text="(YYYY-MM-DD)", font=("Segoe UI", 8), 
              bg="white", fg="#7F8C8D").pack(side=LEFT, padx=2)
        
        Label(row2, text="To Date:", font=("Segoe UI", 10), 
              bg="white", fg="#2C3E50").pack(side=LEFT, padx=5)
        
        txt_to = Entry(row2, textvariable=self.var_to_date, 
                      font=("Segoe UI", 10), bg="#FEF9E6", width=15)
        txt_to.pack(side=LEFT, padx=5)
        
        Label(row2, text="(YYYY-MM-DD)", font=("Segoe UI", 8), 
              bg="white", fg="#7F8C8D").pack(side=LEFT, padx=2)
        
        btn_date_filter = Button(row2, text="📅 Filter by Date", command=self.filter_by_date,
                                font=("Segoe UI", 9, "bold"), bg="#9B59B6", 
                                fg="white", cursor="hand2", bd=0, padx=15, pady=5)
        btn_date_filter.pack(side=LEFT, padx=10)
        
        btn_clear_date = Button(row2, text="Clear Date", command=self.clear_date_filter,
                               font=("Segoe UI", 9, "bold"), bg="#95A5A6", 
                               fg="white", cursor="hand2", bd=0, padx=15, pady=5)
        btn_clear_date.pack(side=LEFT, padx=5)

        # ==================== Summary Cards ====================
        summary_frame = Frame(self.root, bg="#F5F6FA")
        summary_frame.pack(fill=X, padx=10, pady=10)
        
        # Total Sales Card
        card1 = Frame(summary_frame, bg="white", relief=RIDGE, bd=2)
        card1.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)
        
        Label(card1, text="💰 Total Sales", font=("Segoe UI", 11, "bold"), 
              bg="white", fg="#2C3E50").pack(pady=10)
        self.lbl_total_sales = Label(card1, text="Rs 0", font=("Segoe UI", 18, "bold"), 
                                     bg="white", fg="#2ECC71")
        self.lbl_total_sales.pack(pady=10)
        
        # Total Transactions Card
        card2 = Frame(summary_frame, bg="white", relief=RIDGE, bd=2)
        card2.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)
        
        Label(card2, text="📊 Total Transactions", font=("Segoe UI", 11, "bold"), 
              bg="white", fg="#2C3E50").pack(pady=10)
        self.lbl_total_trans = Label(card2, text="0", font=("Segoe UI", 18, "bold"), 
                                     bg="white", fg="#3498DB")
        self.lbl_total_trans.pack(pady=10)
        
        # Average Sale Card
        card3 = Frame(summary_frame, bg="white", relief=RIDGE, bd=2)
        card3.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)
        
        Label(card3, text="📈 Average Sale", font=("Segoe UI", 11, "bold"), 
              bg="white", fg="#2C3E50").pack(pady=10)
        self.lbl_avg_sale = Label(card3, text="Rs 0", font=("Segoe UI", 18, "bold"), 
                                  bg="white", fg="#F39C12")
        self.lbl_avg_sale.pack(pady=10)

        # ==================== Sales Table ====================
        table_frame = LabelFrame(self.root, text="📋 Sales Records", 
                                 font=("Segoe UI", 11, "bold"), 
                                 bg="white", fg="#2C3E50", bd=2, relief=RIDGE)
        table_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Create Treeview with scrollbars
        columns = ("invoice_no", "date", "customer_name", "customer_phone", 
                  "total_amount", "payment_method", "discount", "tax", "created_by")
        
        self.SalesTable = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)
        
        # Define headings
        self.SalesTable.heading("invoice_no", text="Invoice No")
        self.SalesTable.heading("date", text="Date & Time")
        self.SalesTable.heading("customer_name", text="Customer Name")
        self.SalesTable.heading("customer_phone", text="Phone")
        self.SalesTable.heading("total_amount", text="Total (Rs)")
        self.SalesTable.heading("payment_method", text="Payment Method")
        self.SalesTable.heading("discount", text="Discount %")
        self.SalesTable.heading("tax", text="Tax %")
        self.SalesTable.heading("created_by", text="Processed By")
        
        # Set column widths
        self.SalesTable.column("invoice_no", width=140)
        self.SalesTable.column("date", width=150)
        self.SalesTable.column("customer_name", width=180)
        self.SalesTable.column("customer_phone", width=100)
        self.SalesTable.column("total_amount", width=100)
        self.SalesTable.column("payment_method", width=120)
        self.SalesTable.column("discount", width=80)
        self.SalesTable.column("tax", width=80)
        self.SalesTable.column("created_by", width=120)
        
        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient=VERTICAL, command=self.SalesTable.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient=HORIZONTAL, command=self.SalesTable.xview)
        self.SalesTable.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        self.SalesTable.pack(side=LEFT, fill=BOTH, expand=True)
        v_scrollbar.pack(side=RIGHT, fill=Y)
        h_scrollbar.pack(side=BOTTOM, fill=X)
        
        # Bind selection event
        self.SalesTable.bind("<<TreeviewSelect>>", self.on_select_sale)

        # ==================== Bottom Buttons ====================
        bottom_frame = Frame(self.root, bg="#F5F6FA")
        bottom_frame.pack(fill=X, padx=10, pady=10)
        
        btn_view_details = Button(bottom_frame, text="📄 View Invoice Details", command=self.view_invoice_details,
                                 font=("Segoe UI", 10, "bold"), bg="#3498DB", 
                                 fg="white", cursor="hand2", bd=0, padx=20, pady=8)
        btn_view_details.pack(side=LEFT, padx=5)
        
        btn_print_invoice = Button(bottom_frame, text="🖨️ Print Invoice", command=self.print_selected_invoice,
                                  font=("Segoe UI", 10, "bold"), bg="#9B59B6", 
                                  fg="white", cursor="hand2", bd=0, padx=20, pady=8)
        btn_print_invoice.pack(side=LEFT, padx=5)
        
        btn_export = Button(bottom_frame, text="📎 Export to Excel", command=self.export_to_excel,
                           font=("Segoe UI", 10, "bold"), bg="#2ECC71", 
                           fg="white", cursor="hand2", bd=0, padx=20, pady=8)
        btn_export.pack(side=LEFT, padx=5)
        
        btn_delete = Button(bottom_frame, text="🗑️ Delete Record", command=self.delete_record,
                           font=("Segoe UI", 10, "bold"), bg="#E74C3C", 
                           fg="white", cursor="hand2", bd=0, padx=20, pady=8)
        btn_delete.pack(side=LEFT, padx=5)
        
        btn_close = Button(bottom_frame, text="❌ Close", command=self.root.destroy,
                          font=("Segoe UI", 10, "bold"), bg="#95A5A6", 
                          fg="white", cursor="hand2", bd=0, padx=20, pady=8)
        btn_close.pack(side=RIGHT, padx=5)

        # Load initial data
        self.load_sales()
        self.update_summary()

    # ==================== Functions ====================
    
    def load_sales(self):
        """Load all sales from database"""
        try:
            conn = mysql.connector.connect(
                host="localhost", user="root", password="", database="ims")
            cursor = conn.cursor()
            
            # Clear existing data
            for item in self.SalesTable.get_children():
                self.SalesTable.delete(item)
            
            # Fetch all sales
            query = """SELECT invoice_no, DATE_FORMAT(sale_date, '%Y-%m-%d %H:%i:%s'), 
                              customer_name, customer_phone, total_amount, 
                              payment_method, discount_percent, tax_percent, created_by 
                      FROM sales ORDER BY sale_date DESC"""
            cursor.execute(query)
            rows = cursor.fetchall()
            
            for row in rows:
                formatted_amount = f"Rs {row[4]:,.2f}" if row[4] else "Rs 0.00"
                values = list(row)
                values[4] = formatted_amount
                self.SalesTable.insert('', END, values=tuple(values))
            
            conn.close()
            self.update_summary()
            
        except Exception as ex:
            messagebox.showerror("Error", f"Error loading sales: {str(ex)}")
    
    def update_summary(self):
        """Update summary cards"""
        try:
            conn = mysql.connector.connect(
                host="localhost", user="root", password="", database="ims")
            cursor = conn.cursor()
            
            # Total sales amount
            cursor.execute("SELECT SUM(total_amount) FROM sales")
            total = cursor.fetchone()[0] or 0
            self.lbl_total_sales.config(text=f"Rs {total:,.2f}")
            
            # Total transactions
            cursor.execute("SELECT COUNT(*) FROM sales")
            count = cursor.fetchone()[0] or 0
            self.lbl_total_trans.config(text=str(count))
            
            # Average sale
            avg = total / count if count > 0 else 0
            self.lbl_avg_sale.config(text=f"Rs {avg:,.2f}")
            
            conn.close()
        except Exception as ex:
            print(f"Error updating summary: {ex}")
    
    def search_sales(self):
        """Search sales based on criteria"""
        try:
            search_by = self.var_searchby.get()
            search_txt = self.var_searchtxt.get().strip()
            
            if search_by == "Select":
                messagebox.showerror("Error", "Please select search criteria")
                return
            
            if not search_txt:
                messagebox.showerror("Error", "Please enter search text")
                return
            
            conn = mysql.connector.connect(
                host="localhost", user="root", password="", database="ims")
            cursor = conn.cursor()
            
            # Clear existing data
            for item in self.SalesTable.get_children():
                self.SalesTable.delete(item)
            
            # Search based on criteria
            if search_by == "Invoice No":
                query = """SELECT invoice_no, DATE_FORMAT(sale_date, '%Y-%m-%d %H:%i:%s'), 
                                  customer_name, customer_phone, total_amount, 
                                  payment_method, discount_percent, tax_percent, created_by 
                          FROM sales WHERE invoice_no LIKE %s ORDER BY sale_date DESC"""
                cursor.execute(query, (f"%{search_txt}%",))
            elif search_by == "Customer Name":
                query = """SELECT invoice_no, DATE_FORMAT(sale_date, '%Y-%m-%d %H:%i:%s'), 
                                  customer_name, customer_phone, total_amount, 
                                  payment_method, discount_percent, tax_percent, created_by 
                          FROM sales WHERE customer_name LIKE %s ORDER BY sale_date DESC"""
                cursor.execute(query, (f"%{search_txt}%",))
            elif search_by == "Customer Phone":
                query = """SELECT invoice_no, DATE_FORMAT(sale_date, '%Y-%m-%d %H:%i:%s'), 
                                  customer_name, customer_phone, total_amount, 
                                  payment_method, discount_percent, tax_percent, created_by 
                          FROM sales WHERE customer_phone LIKE %s ORDER BY sale_date DESC"""
                cursor.execute(query, (f"%{search_txt}%",))
            
            rows = cursor.fetchall()
            
            if len(rows) == 0:
                messagebox.showinfo("Info", f"No sales found with {search_by}: '{search_txt}'")
                self.load_sales()
            else:
                for row in rows:
                    formatted_amount = f"Rs {row[4]:,.2f}" if row[4] else "Rs 0.00"
                    values = list(row)
                    values[4] = formatted_amount
                    self.SalesTable.insert('', END, values=tuple(values))
            
            conn.close()
            
        except Exception as ex:
            messagebox.showerror("Error", f"Error searching sales: {str(ex)}")
    
    def filter_by_date(self):
        """Filter sales by date range"""
        try:
            from_date = self.var_from_date.get().strip()
            to_date = self.var_to_date.get().strip()
            
            if not from_date or not to_date:
                messagebox.showerror("Error", "Please enter both from and to dates")
                return
            
            conn = mysql.connector.connect(
                host="localhost", user="root", password="", database="ims")
            cursor = conn.cursor()
            
            # Clear existing data
            for item in self.SalesTable.get_children():
                self.SalesTable.delete(item)
            
            query = """SELECT invoice_no, DATE_FORMAT(sale_date, '%Y-%m-%d %H:%i:%s'), 
                              customer_name, customer_phone, total_amount, 
                              payment_method, discount_percent, tax_percent, created_by 
                      FROM sales WHERE DATE(sale_date) BETWEEN %s AND %s 
                      ORDER BY sale_date DESC"""
            cursor.execute(query, (from_date, to_date))
            rows = cursor.fetchall()
            
            if len(rows) == 0:
                messagebox.showinfo("Info", f"No sales found between {from_date} and {to_date}")
                self.load_sales()
            else:
                for row in rows:
                    formatted_amount = f"Rs {row[4]:,.2f}" if row[4] else "Rs 0.00"
                    values = list(row)
                    values[4] = formatted_amount
                    self.SalesTable.insert('', END, values=tuple(values))
            
            conn.close()
            
        except Exception as ex:
            messagebox.showerror("Error", f"Error filtering by date: {str(ex)}")
    
    def clear_date_filter(self):
        """Clear date filter and show all sales"""
        self.var_from_date.set("")
        self.var_to_date.set("")
        self.var_searchby.set("Select")
        self.var_searchtxt.set("")
        self.load_sales()
    
    def on_select_sale(self, event):
        """Handle selection of a sale record"""
        selected = self.SalesTable.focus()
        if selected:
            values = self.SalesTable.item(selected, 'values')
            self.selected_invoice = values[0]
    
    def view_invoice_details(self):
        """View detailed invoice for selected sale"""
        selected = self.SalesTable.focus()
        if not selected:
            messagebox.showerror("Error", "Please select a sale record first")
            return
        
        values = self.SalesTable.item(selected, 'values')
        invoice_no = values[0]
        self.show_invoice_details(invoice_no)
    
    def show_invoice_details(self, invoice_no):
        """Show complete invoice details in a new window"""
        try:
            conn = mysql.connector.connect(
                host="localhost", user="root", password="", database="ims")
            cursor = conn.cursor()
            
            # Get sale details
            cursor.execute("""SELECT invoice_no, sale_date, customer_name, customer_phone, 
                              total_amount, payment_method, discount_percent, tax_percent, created_by 
                              FROM sales WHERE invoice_no = %s""", (invoice_no,))
            sale = cursor.fetchone()
            
            # Get sale items
            cursor.execute("""SELECT p.name, si.quantity, si.price, si.total 
                              FROM sale_items si
                              JOIN product p ON si.product_id = p.pid
                              WHERE si.invoice_no = %s""", (invoice_no,))
            items = cursor.fetchall()
            
            conn.close()
            
            # Create invoice window
            invoice_win = Toplevel(self.root)
            invoice_win.title(f"Invoice Details - {invoice_no}")
            invoice_win.geometry("550x700+350+100")
            invoice_win.config(bg="white")
            
            text_area = Text(invoice_win, font=("Courier", 10), wrap=WORD)
            text_area.pack(fill=BOTH, expand=True, padx=20, pady=20)
            
            invoice_text = f"""
{'='*55}
                    INVOICE DETAILS
{'='*55}

Invoice No: {sale[0]}
Date: {sale[1].strftime('%Y-%m-%d %H:%M:%S') if isinstance(sale[1], datetime) else sale[1]}
Customer: {sale[2]}
Phone: {sale[3]}

{'='*55}
Items:
{'-'*55}
"""
            subtotal = 0
            for item in items:
                invoice_text += f"{item[0]:35} x{item[1]:3} = Rs {item[3]:,.2f}\n"
                subtotal += item[3]
            
            discount_percent = sale[6] or 0
            tax_percent = sale[7] or 0
            discount_amount = subtotal * (discount_percent / 100)
            tax_amount = (subtotal - discount_amount) * (tax_percent / 100)
            
            invoice_text += f"""
{'-'*55}
Subtotal: {' ' * 35} Rs {subtotal:,.2f}
Discount ({discount_percent:.0f}%): {' ' * 28} -Rs {discount_amount:,.2f}
Tax ({tax_percent:.0f}%): {' ' * 35} +Rs {tax_amount:,.2f}
{'='*55}
GRAND TOTAL: {' ' * 33} Rs {sale[4]:,.2f}
{'='*55}

Payment Method: {sale[5]}
Processed By: {sale[8]}

         Thank you for shopping with us!
{'='*55}
"""
            text_area.insert(1.0, invoice_text)
            text_area.config(state='disabled')
            
            btn_close = Button(invoice_win, text="Close", command=invoice_win.destroy,
                              font=("Segoe UI", 10), bg="#3498DB", fg="white", 
                              cursor="hand2", padx=20, pady=5)
            btn_close.pack(pady=10)
            
        except Exception as ex:
            messagebox.showerror("Error", f"Error loading invoice: {str(ex)}")
    
    def print_selected_invoice(self):
        """Print selected invoice"""
        selected = self.SalesTable.focus()
        if not selected:
            messagebox.showerror("Error", "Please select a sale record first")
            return
        
        values = self.SalesTable.item(selected, 'values')
        invoice_no = values[0]
        self.show_invoice_details(invoice_no)
    
    def export_to_excel(self):
        """Export sales data to Excel/CSV"""
        try:
            import csv
            from datetime import datetime
            
            filename = f"sales_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                
                # Write headers
                headers = ["Invoice No", "Date", "Customer Name", "Customer Phone", 
                          "Total Amount", "Payment Method", "Discount %", "Tax %", "Processed By"]
                writer.writerow(headers)
                
                # Write data
                for item in self.SalesTable.get_children():
                    values = self.SalesTable.item(item, 'values')
                    writer.writerow(values)
            
            messagebox.showinfo("Success", f"Data exported to {filename}")
            
        except Exception as ex:
            messagebox.showerror("Error", f"Error exporting data: {str(ex)}")
    
    def delete_record(self):
        """Delete selected sale record"""
        selected = self.SalesTable.focus()
        if not selected:
            messagebox.showerror("Error", "Please select a sale record to delete")
            return
        
        values = self.SalesTable.item(selected, 'values')
        invoice_no = values[0]
        
        if messagebox.askyesno("Confirm", f"Are you sure you want to delete invoice {invoice_no}?\nThis action cannot be undone!"):
            try:
                conn = mysql.connector.connect(
                    host="localhost", user="root", password="", database="ims")
                cursor = conn.cursor()
                
                # Delete sale items first (due to foreign key)
                cursor.execute("DELETE FROM sale_items WHERE invoice_no = %s", (invoice_no,))
                # Delete sale record
                cursor.execute("DELETE FROM sales WHERE invoice_no = %s", (invoice_no,))
                
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Success", "Sale record deleted successfully!")
                self.load_sales()
                
            except Exception as ex:
                messagebox.showerror("Error", f"Error deleting record: {str(ex)}")


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
    obj = SalesHistoryClass(root)
    root.mainloop()
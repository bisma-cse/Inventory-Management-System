from tkinter import *
from tkinter import ttk, messagebox
from tkinter import font as tkfont
from PIL import Image, ImageTk
from Employee import employeeClass
from supplier import supplierClass
from category import categoryClass
from product import productClass
from sales import NewSaleClass
from SalesHistoryClass import SalesHistoryClass
import datetime

class IMS:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+0+0")
        self.root.title("Inventory Management System")
        self.root.config(bg="#F5F6FA")
        
        # Make window resizable
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
        
        # ==================== Modern Header ====================
        self.create_header()
        
        # ==================== Statistics Cards ====================
        self.create_stats_cards()
        
        # ==================== Main Content Area with Sidebar ====================
        self.create_main_layout()
        
        # ==================== Footer ====================
        self.create_footer()
        
        # ==================== Update Clock ====================
        self.update_clock()
        
        # ==================== Load Initial Statistics ====================
        self.update_statistics()
        
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
            
    def create_header(self):
        """Create modern header without logo"""
        header_frame = Frame(self.scrollable_frame, bg="#2C3E50", height=100)
        header_frame.pack(fill=X)
        header_frame.pack_propagate(False)
        
        # Left section - Title
        title_container = Frame(header_frame, bg="#2C3E50")
        title_container.place(x=30, y=20)
        
        title_label = Label(title_container,
                           text="INVENTORY MANAGEMENT SYSTEM",
                           font=("Segoe UI", 28, "bold"),
                           bg="#2C3E50",
                           fg="white")
        title_label.pack()
        
        subtitle = Label(title_container,
                        text="Efficient Stock Management Solution",
                        font=("Segoe UI", 10),
                        bg="#2C3E50",
                        fg="#BDC3C7")
        subtitle.pack()
        
        # Right section - Logout and Clock
        right_container = Frame(header_frame, bg="#2C3E50")
        right_container.place(relx=1, x=-30, y=20, anchor="ne")
        
        # Logout Button
        logout_btn = Button(right_container,
                           text="Close",
                           font=("Segoe UI", 11, "bold"),
                           bg="#E74C3C",
                           fg="white",
                           bd=0,
                           padx=20,
                           pady=8,
                           cursor="hand2",
                           activebackground="#C0392B",
                           activeforeground="white",
                           command=self.logout)
        logout_btn.pack(side=RIGHT, padx=(0, 20))
        
        # Clock Frame
        self.clock_frame = Frame(right_container, bg="#34495E", padx=15, pady=8)
        self.clock_frame.pack(side=RIGHT)
        
        self.date_label = Label(self.clock_frame,
                               text="",
                               font=("Segoe UI", 10),
                               bg="#34495E",
                               fg="white")
        self.date_label.pack(side=LEFT)
        
        self.time_label = Label(self.clock_frame,
                               text="",
                               font=("Segoe UI", 11, "bold"),
                               bg="#34495E",
                               fg="#3498DB")
        self.time_label.pack(side=LEFT, padx=(10,0))
        
    def create_stats_cards(self):
        """Create modern statistics cards"""
        # Stats container
        self.stats_container = Frame(self.scrollable_frame, bg="#F5F6FA")
        self.stats_container.pack(pady=30, padx=20, fill=X)
        
        # Card data
        stats = [
            {"title": "Total Employees", "icon": "👥", "color": "#3498DB", "value": "0", "key": "employees"},
            {"title": "Total Suppliers", "icon": "🤝", "color": "#2ECC71", "value": "0", "key": "suppliers"},
            {"title": "Total Categories", "icon": "📁", "color": "#E74C3C", "value": "0", "key": "categories"},
            {"title": "Total Products", "icon": "📦", "color": "#F39C12", "value": "0", "key": "products"},
            {"title": "Total Sales", "icon": "💰", "color": "#9B59B6", "value": "0", "key": "sales"}
        ]
        
        self.stats_labels = {}
        
        # Create responsive grid
        for i, stat in enumerate(stats):
            card = Frame(self.stats_container,
                        bg="white",
                        relief=FLAT,
                        bd=0,
                        highlightbackground="#E0E0E0",
                        highlightthickness=1)
            
            # Calculate column position
            row = i // 3
            col = i % 3
            
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            # Configure grid weights
            self.stats_container.grid_columnconfigure(col, weight=1)
            
            # Card content
            icon_label = Label(card,
                              text=stat["icon"],
                              font=("Segoe UI Emoji", 32),
                              bg="white",
                              fg=stat["color"])
            icon_label.pack(pady=(20,10))
            
            title_label = Label(card,
                               text=stat["title"],
                               font=("Segoe UI", 12),
                               bg="white",
                               fg="#7F8C8D")
            title_label.pack()
            
            value_label = Label(card,
                               text=stat["value"],
                               font=("Segoe UI", 24, "bold"),
                               bg="white",
                               fg="#2C3E50")
            value_label.pack(pady=(5,20))
            
            self.stats_labels[stat["key"]] = value_label
    
    def create_main_layout(self):
        """Create main layout with sidebar and content"""
        main_layout = Frame(self.scrollable_frame, bg="#F5F6FA")
        main_layout.pack(fill=BOTH, expand=True, padx=20, pady=(0,20))
        
        # Create sidebar
        self.create_sidebar(main_layout)
        
        # Create content area
        self.create_content_area(main_layout)
        
    def create_sidebar(self, parent):
        """Create modern sidebar menu"""
        sidebar = Frame(parent, bg="white", width=280, relief=FLAT, bd=0)
        sidebar.pack(side=LEFT, fill=Y, padx=(0,20))
        sidebar.pack_propagate(False)
        
        # Menu Header
        menu_header = Label(sidebar,
                           text="📋 MENU",
                           font=("Segoe UI", 16, "bold"),
                           bg="white",
                           fg="#2C3E50")
        menu_header.pack(pady=(25,20))
        
        # Menu Items
        menu_items = [
            {"name": "Dashboard", "icon": "🏠", "command": self.refresh_dashboard, "color": "#3498DB"},
            {"name": "Employee Management", "icon": "👥", "command": self.open_employee, "color": "#3498DB"},
            {"name": "Supplier Management", "icon": "🤝", "command": self.open_supplier, "color": "#2ECC71"},
            {"name": "Category Management", "icon": "📁", "command": self.open_category, "color": "#E74C3C"},
            {"name": "Product Management", "icon": "📦", "command": self.open_product, "color": "#F39C12"},
            {"name": "New Sale", "icon": "💰", "command": self.open_new_sale, "color": "#9B59B6"},
            {"name": "Sales History", "icon": "📊", "command": self.open_sales_history, "color": "#E67E22"}
        ]
        
        self.menu_buttons = []
        
        for item in menu_items:
            btn_frame = Frame(sidebar, bg="white")
            btn_frame.pack(fill=X, padx=15, pady=5)
            
            btn = Button(btn_frame,
                        text=f"  {item['icon']}  {item['name']}",
                        font=("Segoe UI", 11),
                        bg="white",
                        fg="#2C3E50",
                        bd=0,
                        anchor="w",
                        padx=15,
                        pady=12,
                        cursor="hand2",
                        command=item["command"])
            btn.pack(fill=X)
            
            # Hover effect
            btn.bind("<Enter>", lambda e, b=btn, c=item['color']: self.on_menu_enter(e, b, c))
            btn.bind("<Leave>", lambda e, b=btn: self.on_menu_leave(e, b))
            
            self.menu_buttons.append(btn)
        
        # Separator
        separator = Frame(sidebar, bg="#E0E0E0", height=1)
        separator.pack(fill=X, padx=20, pady=20)
        
        # Exit Button
        exit_btn = Button(sidebar,
                         text="  ❌  Exit Application",
                         font=("Segoe UI", 11, "bold"),
                         bg="#E74C3C",
                         fg="white",
                         bd=0,
                         anchor="w",
                         padx=15,
                         pady=12,
                         cursor="hand2",
                         command=self.root.quit)
        exit_btn.pack(fill=X, padx=15, pady=5)
        
    def create_content_area(self, parent):
        """Create main content area"""
        content_frame = Frame(parent, bg="#F5F6FA")
        content_frame.pack(side=RIGHT, fill=BOTH, expand=True)
        
        # Welcome Card
        welcome_card = Frame(content_frame,
                            bg="white",
                            relief=FLAT,
                            bd=0,
                            highlightbackground="#E0E0E0",
                            highlightthickness=1)
        welcome_card.pack(fill=X, pady=(0,20))
        
        welcome_text = Label(welcome_card,
                            text="Welcome Back! 👋",
                            font=("Segoe UI", 24, "bold"),
                            bg="white",
                            fg="#2C3E50")
        welcome_text.pack(pady=(30,10))
        
        welcome_subtext = Label(welcome_card,
                               text="Manage your inventory efficiently with our smart system",
                               font=("Segoe UI", 12),
                               bg="white",
                               fg="#7F8C8D")
        welcome_subtext.pack(pady=(0,30))
        
        # Quick Actions Section
        actions_frame = Frame(content_frame, bg="#F5F6FA")
        actions_frame.pack(fill=X, pady=(0,20))
        
        actions_title = Label(actions_frame,
                             text="Quick Actions",
                             font=("Segoe UI", 16, "bold"),
                             bg="#F5F6FA",
                             fg="#2C3E50")
        actions_title.pack(anchor=W, pady=(0,15))
        
        # Action buttons
        actions = [
            {"name": "Add Employee", "icon": "👤", "color": "#3498DB", "command": self.open_employee},
            {"name": "Add Supplier", "icon": "🤝", "color": "#2ECC71", "command": self.open_supplier},
            {"name": "Add Category", "icon": "📁", "color": "#E74C3C", "command": self.open_category},
            {"name": "Add Product", "icon": "📦", "color": "#F39C12", "command": self.open_product},
            {"name": "New Sale", "icon": "💰", "color": "#9B59B6", "command": self.open_new_sale},
            {"name": "Sales History", "icon": "📊", "color": "#E67E22", "command": self.open_sales_history}
        ]
        
        actions_container = Frame(actions_frame, bg="#F5F6FA")
        actions_container.pack(fill=X)
        
        for i, action in enumerate(actions):
            action_btn = Button(actions_container,
                               text=f"{action['icon']} {action['name']}",
                               font=("Segoe UI", 10, "bold"),
                               bg=action["color"],
                               fg="white",
                               bd=0,
                               padx=15,
                               pady=10,
                               cursor="hand2",
                               command=action["command"])
            action_btn.pack(side=LEFT, padx=5)
            
            # Hover effect for action buttons
            action_btn.bind("<Enter>", lambda e, b=action_btn, c=action['color']: self.on_action_enter(e, b, c))
            action_btn.bind("<Leave>", lambda e, b=action_btn, c=action['color']: self.on_action_leave(e, b, c))
        
        # Recent Activity Section
        activity_frame = Frame(content_frame, bg="#F5F6FA")
        activity_frame.pack(fill=BOTH, expand=True)
        
        activity_title = Label(activity_frame,
                              text="Recent Activity",
                              font=("Segoe UI", 16, "bold"),
                              bg="#F5F6FA",
                              fg="#2C3E50")
        activity_title.pack(anchor=W, pady=(0,15))
        
        # Activity Cards
        activities = [
            {"title": "System Ready", "description": "Inventory Management System is ready to use", "time": "Just now", "color": "#2ECC71"},
            {"title": "Quick Tip", "description": "Use the sidebar menu to access different modules", "time": "", "color": "#3498DB"},
            {"title": "Getting Started", "description": "Start by adding employees, suppliers, categories, and products", "time": "", "color": "#9B59B6"}
        ]
        
        for activity in activities:
            activity_card = Frame(activity_frame,
                                 bg="white",
                                 relief=FLAT,
                                 bd=0,
                                 highlightbackground="#E0E0E0",
                                 highlightthickness=1)
            activity_card.pack(fill=X, pady=5)
            
            # Color indicator
            indicator = Frame(activity_card, bg=activity["color"], width=5)
            indicator.pack(side=LEFT, fill=Y)
            
            content = Frame(activity_card, bg="white", padx=15, pady=10)
            content.pack(side=LEFT, fill=BOTH, expand=True)
            
            title = Label(content,
                         text=activity["title"],
                         font=("Segoe UI", 12, "bold"),
                         bg="white",
                         fg="#2C3E50")
            title.pack(anchor=W)
            
            description = Label(content,
                              text=activity["description"],
                              font=("Segoe UI", 10),
                              bg="white",
                              fg="#7F8C8D")
            description.pack(anchor=W)
            
            if activity["time"]:
                time_label = Label(content,
                                 text=activity["time"],
                                 font=("Segoe UI", 9),
                                 bg="white",
                                 fg="#BDC3C7")
                time_label.pack(anchor=W, pady=(5,0))
    
    def create_footer(self):
        """Create modern footer"""
        footer = Frame(self.scrollable_frame, bg="#2C3E50", height=50)
        footer.pack(side=BOTTOM, fill=X)
        footer.pack_propagate(False)
        
        footer_text = Label(footer,
                           text="© 2024 Inventory Management System | Developed by Bisma Amir | Contact: 0313-3459699",
                           font=("Segoe UI", 9),
                           bg="#2C3E50",
                           fg="#BDC3C7")
        footer_text.pack(pady=15)
    
    def update_clock(self):
        """Update clock display"""
        now = datetime.datetime.now()
        current_date = now.strftime("%d-%m-%Y")
        current_time = now.strftime("%H:%M:%S")
        
        self.date_label.config(text=current_date)
        self.time_label.config(text=current_time)
        
        self.root.after(1000, self.update_clock)
    
    def update_statistics(self):
        """Update statistics from database"""
        try:
            import mysql.connector
            con = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="ims"
            )
            cur = con.cursor()
            
            # Get employee count
            cur.execute("SELECT COUNT(*) FROM employee")
            emp_count = cur.fetchone()[0]
            self.stats_labels["employees"].config(text=str(emp_count))
            
            # Get supplier count
            cur.execute("SELECT COUNT(*) FROM supplier")
            sup_count = cur.fetchone()[0]
            self.stats_labels["suppliers"].config(text=str(sup_count))
            
            # Get category count
            cur.execute("SELECT COUNT(*) FROM category")
            cat_count = cur.fetchone()[0]
            self.stats_labels["categories"].config(text=str(cat_count))
            
            # Get product count
            cur.execute("SELECT COUNT(*) FROM product")
            pro_count = cur.fetchone()[0]
            self.stats_labels["products"].config(text=str(pro_count))
            
            # Get sales count
            cur.execute("SELECT COUNT(*) FROM sales")
            sales_count = cur.fetchone()[0]
            self.stats_labels["sales"].config(text=str(sales_count))
            
            con.close()
        except Exception as e:
            print(f"Error updating statistics: {e}")
            pass
    
    def on_menu_enter(self, event, button, color):
        """Menu hover effect"""
        button.config(bg=color, fg="white")
    
    def on_menu_leave(self, event, button):
        """Menu leave effect"""
        button.config(bg="white", fg="#2C3E50")
    
    def on_action_enter(self, event, button, color):
        """Action button hover effect"""
        button.config(bg=self.darken_color(color))
    
    def on_action_leave(self, event, button, color):
        """Action button leave effect"""
        button.config(bg=color)
    
    def darken_color(self, color):
        """Darken color for hover effect"""
        colors = {
            "#3498DB": "#2980B9",
            "#F39C12": "#E67E22",
            "#2ECC71": "#27AE60",
            "#9B59B6": "#8E44AD",
            "#E74C3C": "#C0392B",
            "#E67E22": "#D35400"
        }
        return colors.get(color, color)
    
    def logout(self):
        """Logout functionality"""
        if messagebox.askyesno("Close System", "Are you sure you want to Close System?"):
            self.root.destroy()
    
    def refresh_dashboard(self):
        """Refresh dashboard statistics"""
        self.update_statistics()
        messagebox.showinfo("Success", "Dashboard refreshed successfully!")
    
    def open_employee(self):
        """Open employee management window"""
        try:
            self.new_win = Toplevel(self.root)
            self.new_win.title("Employee Management System")
            self.new_win.geometry("1100x550+220+130")
            self.new_win.config(bg="#F5F6FA")
            self.new_obj = employeeClass(self.new_win)
            self.center_window(self.new_win)
            self.new_win.protocol("WM_DELETE_WINDOW", lambda: self.on_child_close(self.new_win))
        except Exception as e:
            messagebox.showerror("Error", f"Could not open Employee Management: {str(e)}")
    
    def open_supplier(self):
        """Open supplier management window"""
        try:
            self.new_win = Toplevel(self.root)
            self.new_win.title("Supplier Management System")
            self.new_win.geometry("1100x550+220+130")
            self.new_win.config(bg="#F5F6FA")
            self.new_obj = supplierClass(self.new_win)
            self.center_window(self.new_win)
            self.new_win.protocol("WM_DELETE_WINDOW", lambda: self.on_child_close(self.new_win))
        except Exception as e:
            messagebox.showerror("Error", f"Could not open Supplier Management: {str(e)}")
    
    def open_category(self):
        """Open category management window"""
        try:
            self.new_win = Toplevel(self.root)
            self.new_win.title("Category Management System")
            self.new_win.geometry("1100x500+220+130")
            self.new_win.config(bg="#F5F6FA")
            self.new_obj = categoryClass(self.new_win)
            self.center_window(self.new_win)
            self.new_win.protocol("WM_DELETE_WINDOW", lambda: self.on_child_close(self.new_win))
        except Exception as e:
            messagebox.showerror("Error", f"Could not open Category Management: {str(e)}")
    
    def open_product(self):
        """Open product management window"""
        try:
            self.new_win = Toplevel(self.root)
            self.new_win.title("Product Management System")
            self.new_win.geometry("1200x650+200+100")
            self.new_win.config(bg="#F5F6FA")
            self.new_obj = productClass(self.new_win)
            self.center_window(self.new_win)
            self.new_win.protocol("WM_DELETE_WINDOW", lambda: self.on_child_close(self.new_win))
        except Exception as e:
            messagebox.showerror("Error", f"Could not open Product Management: {str(e)}")
    
    def open_new_sale(self):
        """Open new sale window"""
        try:
            self.new_win = Toplevel(self.root)
            self.new_win.title("New Sale - POS System")
            self.new_win.geometry("1300x750+100+50")
            self.new_win.config(bg="#F5F6FA")
            self.new_obj = NewSaleClass(self.new_win)
            self.center_window(self.new_win)
            self.new_win.protocol("WM_DELETE_WINDOW", lambda: self.on_child_close(self.new_win))
        except Exception as e:
            messagebox.showerror("Error", f"Could not open New Sale: {str(e)}")
    
    def open_sales_history(self):
        """Open sales history window"""
        try:
            self.new_win = Toplevel(self.root)
            self.new_win.title("Sales History")
            self.new_win.geometry("1300x700+100+50")
            self.new_win.config(bg="#F5F6FA")
            self.new_obj = SalesHistoryClass(self.new_win)
            self.center_window(self.new_win)
            self.new_win.protocol("WM_DELETE_WINDOW", lambda: self.on_child_close(self.new_win))
        except Exception as e:
            messagebox.showerror("Error", f"Could not open Sales History: {str(e)}")
    
    def center_window(self, window):
        """Center a window on screen"""
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')
    
    def on_child_close(self, child_window):
        """Handle child window closing"""
        child_window.destroy()
        self.update_statistics()


if __name__ == "__main__":
    root = Tk()
    app = IMS(root)
    root.mainloop()
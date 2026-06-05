# 📦 Inventory Management System

A desktop-based Inventory Management System developed using Python (Tkinter) and MySQL. The application provides complete inventory control, employee management, supplier management, product tracking, category organization, and Point-of-Sale (POS) functionality.

## Features

* Employee Management
* Supplier Management
* Product Management
* Category Management
* Real-Time Stock Tracking
* Point-of-Sale (POS)
* Invoice Generation
* Sales History
* CSV Export
* Search & Filtering
* Dashboard Statistics

## Technology Stack

* Python 3
* Tkinter
* MySQL
* mysql-connector-python
* Pillow (PIL)

## System Modules

### Dashboard

* Live statistics
* Digital clock
* Navigation panel
  <img width="1352" height="730" alt="image" src="https://github.com/user-attachments/assets/d44935a8-73c9-449d-8808-7dcfb20a77a8" />
  <img width="1366" height="727" alt="image" src="https://github.com/user-attachments/assets/d4a85a47-40e9-4252-9e8a-68dbeb666ec3" />


### Employee Management

* Add, Update, Delete Employees
* Search Functionality
  <img width="1366" height="728" alt="image" src="https://github.com/user-attachments/assets/051d10b5-bc35-4ff2-8afc-1cf8480c8c8e" />


### Supplier Management

* Supplier Profiles
* Payment Terms
* Credit Limits
<img width="1363" height="731" alt="image" src="https://github.com/user-attachments/assets/f679bdc3-8b73-453b-80e7-90ae9c377386" />
<img width="1366" height="730" alt="image" src="https://github.com/user-attachments/assets/0aec95d5-e50d-4af8-a785-d3f694f76d18" />

### Product Management

* Product Inventory
* Category & Supplier Integration
* Stock Tracking
<img width="1366" height="725" alt="image" src="https://github.com/user-attachments/assets/2369b56d-4a18-4184-8fa2-3ec091829d08" />

### Point of Sale (POS)

* Shopping Cart
* Discount & Tax Calculation
* Invoice Generation
<img width="1366" height="729" alt="image" src="https://github.com/user-attachments/assets/a18d4505-cc56-4c7c-bc6c-603fd56ca93b" />

### Sales History

* Transaction Tracking
* CSV Export
* Date Range Filtering
  <img width="1366" height="730" alt="image" src="https://github.com/user-attachments/assets/249c7a95-9b23-4533-a61d-8f260ef0ae05" />


## Database Design

Main Entities:

* Employee
* Supplier
* Category
* Product
* Sales
* Sale_Items

Relationships are implemented using Primary Keys and Foreign Keys to maintain data integrity.

## Installation

1. Clone the repository

```bash
git clone https://github.com/bisma-cse/Inventory-Management-System.git
```

2. Install required packages

```bash
pip install mysql-connector-python pillow
```

3. Create the database using:

```text
create_db.py
```

4. Configure MySQL connection settings.

5. Run:

```text
IMS.py
```

## Future Improvements

* User Authentication System
* Barcode Scanner Integration
* Email Invoice Support
* Sales Analytics Dashboard
* Low Stock Notifications

## Author

Bisma Amir

B.E. Computer Systems Engineering

Sukkur IBA University

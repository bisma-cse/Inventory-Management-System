import mysql.connector
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""
)
cur = conn.cursor()
cur.execute("CREATE DATABASE IF NOT EXISTS ims")
cur.execute("USE ims")
cur.execute("""
CREATE TABLE IF NOT EXISTS employee(
    eid INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    email VARCHAR(100),
    gender VARCHAR(10),
    contact VARCHAR(15),
    dob DATE,
    doj DATE,
    password VARCHAR(100),
    usertype VARCHAR(20),
    address TEXT,
    salary DECIMAL(10,2)
)
""")
print("Table created successfully!")
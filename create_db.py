import sqlite3 as sq

def Create_db():
    conn=sq.connect(database=r'IMS.db')
    cur=conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Employee (Emp_id INTEGER PRIMARY KEY AUTOINCREMENT,Name text,Email text,Gender text,Contact text,DOB text,DOJ text,Password text,Emp_Type text,Address text,Salary text)")
    conn.commit()


    cur.execute("CREATE TABLE IF NOT EXISTS Supplier (Sup_id INTEGER PRIMARY KEY AUTOINCREMENT,Name text,Contact text,Description text)")
    conn.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS Category (Cat_id INTEGER PRIMARY KEY AUTOINCREMENT,Name text)")
    conn.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS Product (Pid INTEGER PRIMARY KEY AUTOINCREMENT,Category text,Supplier text,Name text,Price text,Quantity text,Status text)")
    conn.commit()
Create_db()
     
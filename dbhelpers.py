#!C:\Python34\python.exe
import pymysql

#
# Code to connect to the database named inventory. In my case, I have a password set up in MySQL
# If you didn't set up a password, this parameter would be blank (i.e. passwd = '')
#


def connecttodb():
    try:
        conn = pymysql.connect(host='localhost', user='root', passwd='Python', database='inventory', autocommit=True)
        return conn
    except:
        htmlhelpers.printheader('Database connect failure')
        print('Failed to open database')
        htmlhelpers.printfooter()

#
# This function creates the database tables for the project.
# Each table has a field that is the key field for each record and it is set up to auto increment
# so you don't need to worry about incrementing it as you add records. MySQL does it automatically
# for you.
#
# Also note that the create statements use the phrase IF NOT EXISTS. This phrase tells
# the MySQL statement to do nothing if the table already exists.
#


def createtables(cur):
    try:
        cur.execute('''CREATE TABLE IF NOT EXISTS inventory (InvID int(11) NOT NULL AUTO_INCREMENT,
                SKU varchar(20),
                ProductName varchar(50),
                QtyOnHand int(11),
                Cost float(8.2),
                RetailPrice float(8.2),
                PRIMARY KEY (InvID))''')
    except:
        htmlhelpers.printheader('Database connect failure')
        print('Failed on create Inventory table')
        htmlhelpers.printfooter()

    try:
        cur.execute('''CREATE TABLE IF NOT EXISTS sales (SalesID int(11) NOT NULL AUTO_INCREMENT,
                Quantity int(11),
                ProductName varchar(50),
                InvID int(11),
                CustID int(11),
                PRIMARY KEY (SalesID))''')
    except:
        htmlhelpers.printheader('Database connect failure')
        print('Failed on create Sales table')
        htmlhelpers.printfooter()

    try:
        cur.execute('''CREATE TABLE IF NOT EXISTS customer (CustID int(11) NOT NULL AUTO_INCREMENT,
                FirstName varchar(30),
                LastName varchar(30),
                PRIMARY KEY (CustID))''')
    except:
        htmlhelpers.printheader('Database connect failure')
        print('Failed on create Customer table')
        htmlhelpers.printfooter()

    try:
        cur.execute('''CREATE TABLE IF NOT EXISTS returns (ReturnID int(11) NOT NULL AUTO_INCREMENT,
                CustID int(11),
                InvID int(11),
                Quantity int(11),
                PRIMARY KEY (ReturnID))''')
    except:
        htmlhelpers.printheader('Database connect failure')
        print('Failed on create Returns table')
        htmlhelpers.printfooter()

#
# Function to do an insert into the inventory table. Values are passed into the function
# and the record is saved away.
#


def saveinventory(cur, sku, productname, qtyonhand, cost, retailprice):
    sql = '''INSERT INTO inventory (SKU, ProductName, QtyOnHand, Cost, RetailPrice)
             VALUES (%s, %s, %s, %s, %s)'''
    record = (sku, productname, qtyonhand, cost, retailprice)
    cur.execute(sql, record)

#
# Function to do an update to an inventory table record. Values are passed into the function
# and the record is saved away.
#


def updateinventory(cur, invid, sku, productname, qtyonhand, cost, retailprice):
    sql = '''UPDATE inventory set SKU=%s, ProductName=%s, QtyOnHand=%s, Cost=%s, RetailPrice=%s
             where InvID=%s'''
    record = (sku, productname, qtyonhand, cost, retailprice, invid)
    cur.execute(sql, record)












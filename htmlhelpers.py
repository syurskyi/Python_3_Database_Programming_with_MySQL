#!C:\Python34\python.exe
import dbhelpers

#
# Code to print the header of all the html pages
#


def printheader(headertitle):
    print('Content-type: text/html\n')
    print('<html>')
    print('<head><title>', headertitle, '</title></head>')
    print('<body>')

#
# Code to print the footer of all the html pages
#


def printfooter():
    print('</body>')
    print('</html>')

#
# Code to print the main menu
#


def mainmenu():
    print('''
          <h2>Main Menu</h2>
          Make a selection and hit the Continue button
          <form name="main" action="mainmenu.py" method="POST">
          <input type="radio" name="screen" value="Inventory"> Work with Inventory<br>
          <input type="radio" name="screen" value="Sale" checked> Record a Sale<br>
          <input type="radio" name="screen" value="Return"> Process a Return<br>
          <input type="radio" name="screen" value="Reports"> Generate Reports <br>
          <input type="radio" name="screen" value="Exit"> Exit System
           <br><input type="submit" value="Continue">
         </form>
''')

#
# Code to print the inventory menu/option selector
#


def inventory():
    print('''
          <h2>Inventory</h2>
          Make a selection and hit the Continue button
          <form name="main" action="mainmenu.py" method="POST">
          <input type="radio" name="screen" value="AddInventory" checked> Add Inventory<br>
          <input type="radio" name="screen" value="EditInventory"> Edit Inventory<br>
          <input type="radio" name="screen" value="DeleteInventory"> Delete An Inventory Item<br>
          <input type="radio" name="screen" value=""> Return to Main Menu <br>
          <br><input type="submit" value="Continue">
          </form>
          ''')

#
# Code to add inventory to the system. This performs two function.
# 1) It prints out the inventory input screen
# 2) It saves inputted inventory to the database and returns to the input screen
#


def addinventory(cur, formdata='', subcommand=''):
    if (subcommand == 'SaveInventory'):  # Get the data and store it away
        sku = formdata.getfirst('SKU', '') # Should do error checking on all of these
        productname = formdata.getfirst('ProductName', '')
        qtyonhand = int(formdata.getfirst('QtyOnHand', ''))
        cost =  float(formdata.getfirst('Cost', ''))
        retailprice = float(formdata.getfirst('RetailPrice', ''))
        dbhelpers.saveinventory(cur, sku, productname, qtyonhand, cost, retailprice)
        print("Data has been saved. <p> <a href='mainmenu.py'>Return to the main menu</a>")
        print("or <a href='mainmenu.py?screen=Inventory'>Return to Inventory Menu.</a>")
    else:
        print('''
              <h2>Add Inventory</h2>
              Fill out the form and click on the Save Inventory Record button to save inventory.
              <form name="main" action="mainmenu.py" method="POST">
              <table>
              <tr><td>SKU: </td><td><input type="text" name="SKU"></td></tr>
              <tr><td>Product Name: </td><td><input type="text" name="ProductName"></td></tr>
              <tr><td>Quantity on Hand: </td><td><input type="text" name="QtyOnHand"></td></tr>
              <tr><td>Wholesale Cost: </td><td><input type="text" name="Cost"></td></tr>
              <tr><td>Retail Price: </td><td><input type="text" name="RetailPrice"></td></tr>
              </table>
              <input type="hidden" name="screen" value="AddInventory">
              <input type="hidden" name="subcommand" value="SaveInventory">
              <input type="submit" value="Save Inventory Record">
              </form>
              <p><a href='mainmenu.py'>Return to the main menu</a> or
              <a href='mainmenu.py?screen=Inventory'>Return to Inventory Menu.</a>
              ''')

#
# Code to edit already entered inventory. This performs three functions
# 1) Display a list of inventory items so user can select item to edit
# 2) Display an edit screen with the current data filled in the forms.
# 3) Save the edited data back into the database
#


def editinventory(cur, formdata='', subcommand=''):
    if (subcommand == 'EditInventory'):
        record = int(formdata.getfirst('record', ''))
        sql = 'SELECT * from inventory where InvID = %s'
        cur.execute(sql, record)
        row = cur.fetchone()
        print('''
              <h2>Edit Inventory Record</h2>
              Fill out the form and click on the Save Edited Inventory button to save inventory.
              <form name="main" action="mainmenu.py" method="POST">
              <table>
              <tr><td>SKU: </td><td><input type="text" name="SKU" value="{SKU}"></td></tr>
              <tr><td>Product Name: </td><td><input type="text" name="ProductName" value="{ProductName}"></td></tr>
              <tr><td>Quantity on Hand: </td><td><input type="text" name="QtyOnHand" value="{QtyOnHand}"></td></tr>
              <tr><td>Wholesale Cost: </td><td><input type="text" name="Cost" value="{Cost}"></td></tr>
              <tr><td>Retail Price: </td><td><input type="text" name="RetailPrice" value="{RetailPrice}"></td></tr>
              </table>
              <input type="hidden" name="screen" value="EditInventory">
              <input type="hidden" name="subcommand" value="SaveEditedInventory">
              <input type="hidden" name="InvID" value="{InvID}">
              <input type="submit" value="Save Edited Inventory">
              </form>
              <p><a href='mainmenu.py'>Return to the main menu</a> or
              <a href='mainmenu.py?screen=Inventory'>Return to Inventory Menu.</a>
              '''.format(InvID=row[0], SKU=row[1], ProductName=row[2], QtyOnHand=row[3], Cost=row[4], RetailPrice=row[5]))
    elif (subcommand == 'SaveEditedInventory'):
        sku = formdata.getfirst('SKU', '') # Should do error checking on all of these
        invid = int(formdata.getfirst('InvID', ''))
        productname = formdata.getfirst('ProductName', '')
        qtyonhand = int(formdata.getfirst('QtyOnHand', ''))
        cost = float(formdata.getfirst('Cost', ''))
        retailprice = float(formdata.getfirst('RetailPrice', ''))
        dbhelpers.updateinventory(cur, invid, sku, productname, qtyonhand, cost, retailprice)
        print("Data has been saved. <p> <a href='mainmenu.py'>Return to the main menu</a>")
        print("or <a href='mainmenu.py?screen=Inventory'>Return to Inventory Menu.</a>")
    else:
        print('Select a record to edit and hit the Edit Selected Record button to start the process.<p>')
        print ('<form name="main" action="mainmenu.py" method="POST">')
        sql = 'SELECT * from inventory'
        cur.execute(sql)
#        for row in cur:    --- Both methods work but this one is Database Adapter implementation dependent
        for row in cur.fetchall():
            print ('<input type="radio" name="record" value="', row[0], '"> SKU: ', row[1], ' - ', row[2], '<br>', sep='')
        print ('''
               <input type="hidden" name="screen" value="EditInventory">
               <input type="hidden" name="subcommand" value="EditInventory">
               <input type="submit" value="Edit Selected Record">
               </form>
               <p><a href='mainmenu.py'>Return to the main menu</a> or
               <a href='mainmenu.py?screen=Inventory'>Return to Inventory Menu.</a>
               ''')

#
# Code to delete already entered inventory. This performs two functions
# 1) Display a list of inventory items so user can select item to delete
# 2) Deletes the item
#


def deleteinventory(cur, formdata='', subcommand=''):
    if (subcommand == 'DeleteInventory'):
        record = int(formdata.getfirst('record', ''))
        sql = 'DELETE from inventory where InvID = %s'
        cur.execute(sql, record)
        print('''
               <p><a href='mainmenu.py'>Return to the main menu</a> or
               <a href='mainmenu.py?screen=Inventory'>Return to Inventory Menu.</a>
               ''')
    else:
        print('Select a record to delete and hit the Delete Selected Record button to complete the process.<p>')
        print('<form name="main" action="mainmenu.py" method="POST">')
        sql = 'SELECT * from inventory'
        cur.execute(sql)
#        for row in cur:    --- Both methods work but this one is Database Adapter implementation dependent
        for row in cur.fetchall():
            print('<input type="radio" name="record" value="', row[0], '"> SKU: ', row[1], ' - ', row[2], '<br>', sep='')
        print('''
               <input type="hidden" name="screen" value="DeleteInventory">
               <input type="hidden" name="subcommand" value="DeleteInventory">
               <input type="submit" value="Delete Selected Record">
               </form>
               <p><a href='mainmenu.py'>Return to the main menu</a> or
               <a href='mainmenu.py?screen=Inventory'>Return to Inventory Menu.</a>
               ''')

#
# Create sale input screen - display first/last name and all inventory items
#


def sale(cur):
    print('''Record a sale<p>
          <form name="main" action="mainmenu.py" method="POST">
          <table>
          <tr><td>First Name:</td><td><input type="text" name="FirstName"></td></tr>
          <tr><td>Last Name:</td><td><input type="text" name="LastName"></td></tr>
          ''')
    sql = 'SELECT * from inventory'
    cur.execute(sql)
    for row in cur.fetchall():
        print('<tr><td>', row[2], ' / Qty: ', row[3], '</td><td><input type="text" name="', row[0], '">', sep='')
    print('''</table>
          <input type="hidden" name="screen" value="RecordSale">
          <input type="submit" value="Record Sale">
          </form>
          <p><a href='mainmenu.py'>Return to the main menu</a>
          ''')

#
# Record the sale... Since every item has its own record in the sales field, here is the logic.
# First, see if customer already exists. If so, get customer id. If not, create customer and get id.
# Then loop through all form fields and save the data in the sales table every time an item is identified.
# Also, remember to deduct the purchased items from inventory
#

def recordsale(cur, formdata=''):
    name = (formdata.getfirst('FirstName', ''), formdata.getfirst('LastName', ''))
    sql = 'SELECT COUNT(*) from customer where FirstName = %s and LastName = %s'
    cur.execute(sql, name)
    result = cur.fetchone()
    if (result[0] > 0):      # Name was found so get CustID
        sql = 'SELECT * from customer where FirstName = %s and LastName = %s'
        cur.execute(sql, name)
        result = cur.fetchone()
        custid = result[0]
    else:                    # No match for name so add it to the customer table and get CustID
        sql = 'INSERT INTO customer (FirstName, LastName) VALUES (%s, %s)'
        cur.execute(sql, name)
        result = cur.fetchone()
        custid = cur.lastrowid   # Get the CustID value from the insert

# Now that the customer is saved, let's store away the inventory and adjust the qty on hand
# First build a list of tuples for the data and use executemany to save into sales table
    data = []
    sql = 'SELECT * from inventory'
    cur.execute(sql)
    for row in cur.fetchall():
        invid = row[0]
        productname = row[2]
        quantity = int(formdata.getfirst(str(invid)))
        quantityonhand = row[3] - quantity          # Row 3 has the current quantity in the database for the item
        if (quantity):   # Build tuple to insert into list AND update inventory table
            temp = (quantity, productname, invid, custid)
            data.append(temp)
            sql = 'UPDATE inventory SET QtyOnHand = %s where InvID = %s'
            cur.execute(sql, [quantityonhand, invid])
    if (len(data) > 0):
        sql = 'INSERT INTO sales (Quantity, ProductName, InvID, CustID) VALUES (%s, %s, %s, %s)'
        cur.executemany(sql, data)

# Now print out a completion message
    print('''Sale has been recorded<p>
          <p><a href='mainmenu.py'>Return to the main menu</a>
          ''')


#
# Create sale input screen - display first/last name and all inventory items
#

def returns(cur):
    print('''Process a return<p>Select a customer to begin.<p>
          <form name="main" action="mainmenu.py" method="POST">
          ''')
    sql = 'SELECT * from customer'
    cur.execute(sql)
    for row in cur.fetchall():
        print('<input type="radio" name="CustID" value="', row[0], '"> ', row[1], '  ', row[2], '<br>', sep='')
    print ('''
           <input type="hidden" name="screen" value="DisplayPurchases">
           <input type="submit" value="Show Customer Purchases">
           </form>
           <p><a href='mainmenu.py'>Return to the main menu</a>
           ''')

#
# Display purchases does the following:
# 1) Gets a list of items purchased and their quantities from the sales table
# 2) Uses that list to get the product names from the inventory table & prints out table
#


def displaypurchases(cur, formdata):
    print('''Process a return<p>Input how many of each item customer returned.<p>
          <form name="main" action="mainmenu.py" method="POST">
          ''')
    custid = formdata.getfirst('CustID')
    print('<input type="hidden" name="CustID" value="', custid, '">')
    sql = 'SELECT sales.InvID, sum(sales.Quantity),inventory.ProductName FROM sales, inventory WHERE sales.custid=%s and sales.InvID = inventory.InvID group by inventory.InvID'
    cur.execute(sql,custid)
    for row in cur.fetchall():
        if (row[1] > 0): # Make sure we have a positive quantity
            print(row[2], ': <font color="blue">Quantity Purchased: ', row[1], '</font> <input type="text" name="', row[0], '"><br>', sep='')
    print('''
           <input type="hidden" name="screen" value="ProcessReturn">
           <input type="submit" value="Record Returns">
           </form>
           <p><a href='mainmenu.py'>Return to the main menu</a>
           ''')

#
# Get the data for number of items returned for each inventory number and store it in the returns table
# Then add the number back into the inventory table
#


def processreturn(cur, formdata):
    print('''Return has been processed<p>
          ''')
    custid = int(formdata.getfirst('CustID'))

#  Now we will loop through the input data and build a list to save away into the returns table
    data = []
    sql = 'SELECT * from inventory'
    cur.execute(sql)
    for row in cur.fetchall():
        invid = row[0]
        try:
            quantity = int(formdata.getfirst(str(invid)))
        except:
           continue # basically do nothing if there is not an input
        else:   # save the data away as the formdata function was successful
            quantityonhand = row[3] + quantity          # Row 3 has the current quantity in the database for the item
            if (quantity):   # Build tuple to insert into list AND update inventory table
                temp = (quantity, invid, custid)
                data.append(temp)
                sql = 'UPDATE inventory SET QtyOnHand = %s where InvID = %s'
                cur.execute(sql, [quantityonhand, invid])
# and add a new record to the sales table with a negative value
                sql = 'INSERT INTO sales (Quantity, InvID, CustID) VALUES (%s, %s, %s)'
                cur.execute(sql, [-quantity, invid, custid])
# And finally add data to returns table
    if (len(data) > 0):
        sql = 'INSERT INTO returns (Quantity, InvID, CustID) VALUES (%s, %s, %s)'
        cur.executemany(sql, data)

    print('''
           <p><a href='mainmenu.py'>Return to the main menu</a>
           ''')
#
# Print a simple report selector
#


def reports():
    print('''
          <h2>Report Menu</h2>
          Choose your report and hit the the Continue button
          <form name="main" action="mainmenu.py" method="POST">
          <input type="radio" name="screen" value="TotalSales"> Total Sales Report<br>
          <input type="radio" name="screen" value="SalesByCustomer"> Sales by Customer Report<br>
          <input type="radio" name="screen" value="InventoryReport"> Inventory Report<br>
           <br><input type="submit" value="Continue">
         </form>
           <p><a href='mainmenu.py'>Return to the main menu</a>
''')

#
# Calculate total sales report. We want the following in the report on a per inventory item basis
# Product Name/ Total sales / Total returns / Dollar value of sales / Dollar value of returns / Gross profit / Net Profit
#  If any inventory item has no sales, just print 0.
#


def totalsales(cur):
    print('''
          <h2>Total Sales Report</h2>
          <table border="2"><tr>
          <td align="center">Product Name</td><td align="center">Total Sales</td><td align="center">Total Returns</td>
          <td align="center">Dollar Value of Sales</td><td align="center">Dollar Value of Returns</td>
          <td align="center">Gross Profit</td><td align="center">Net Profit</td><td>
          </tr>
''')
    sql = 'SELECT * FROM inventory'
    cur.execute(sql)
    for row in cur.fetchall():      # Loop through inventory table
        invid = row[0]
        productname = row[2]
        cost = float(row[4])
        retailprice = float(row[5])
        sql = 'select sum(Quantity) from sales where Quantity > 0 and InvID = %s' # number of sales
        cur.execute(sql, invid)
        data = cur.fetchone()
        sales = int(data[0])
        sql = 'select sum(Quantity) from sales where Quantity < 0 and InvID = %s' # number of returns
        cur.execute(sql, invid)
        data = cur.fetchone()
        returns = abs(int(data[0]))    # turn to a positive number
# Calculate pricing
        dollarsales = sales * retailprice
        dollarreturns = returns * retailprice
        grossprofit = dollarsales - dollarreturns
        netprofit = grossprofit - ((sales - returns) * cost)
        dollarsales = str("{0:.2f}".format(dollarsales))      # Just an alternate way of formating values
        dollarreturns = str("{0:.2f}".format(dollarreturns))
        grossprofit = str("{0:.2f}".format(grossprofit))
        netprofit = str("{0:.2f}".format(netprofit))
        print('''<tr>
                 <td align="right">{ProductName}</td>
                 <td align="right">{Sales}</td>
                 <td align="right">{TotalReturns}</td>
                 <td align="right">${DollarSales}</td>
                 <td align="right">${DollarReturns}</td>
                 <td align="right">${GrossProfit}</td>
                 <td align="right">${NetProfit}</td>
                 </tr>'''.format(ProductName=productname,Sales=sales,TotalReturns=returns,DollarSales=dollarsales,DollarReturns=dollarreturns,GrossProfit=grossprofit,NetProfit=netprofit))

    print('''<table>
          <p><a href='mainmenu.py'>Return to the main menu</a>
''')

#
# Generate a report that shows number of sales and returns for customer.
# This will be a simple report giving total items only. It will not differentiate
# between inventory items, etc. In a real world scenaro, this would be expanded
# with numerous sub reports to break down sales/returns in a variety of ways.
#


def salesbycustomer(cur):
    print('''
          <h2>Sales by Customer Report</h2>
          <table border="2"><tr>
          <td align="center">Customer</td><td align="center">Sales</td><td align="center">Returns</td>
          </tr>
''')
    sql = 'SELECT * FROM customer group by FirstName, LastName'
    cur.execute(sql)
    for row in cur.fetchall():      # Loop through customer table
        custid = int(row[0])
        firstname = row[1]
        lastname = row[2]
        sql = 'select sum(Quantity) from sales where Quantity > 0 and CustID = %s' # number of sales
        cur.execute(sql, custid)
        data = cur.fetchone()
        try:                        # Need to do a try as there may be no records for customer in table
            sales = int(data[0])    # fetchone basically returns a NULL when there is no match and that throws
        except:                     # a TypeError as int can't convert NULL to a value.
            sales = 0;
        sql = 'select sum(Quantity) from returns where CustID = %s' # number of returns
        cur.execute(sql, custid)
        data = cur.fetchone()
        if(data[0]):                # Alternate way to check if data was returned
            returns = int(data[0])
        else:
            returns = 0;
        print('''<tr>
                 <td align="right">{FirstName} {LastName}</td>
                 <td align="right">{Sales}</td>
                 <td align="right">{Returns}</td>
                 </tr>'''.format(FirstName=firstname, LastName=lastname, Sales=sales, Returns=returns))

    print('''<table>
          <p><a href='mainmenu.py'>Return to the main menu</a>
''')

#
# Simple report showing remaining inventory level of each item in inventory.
# In a real world scenario (one where orders were recorded with dates), lots of
# interesting sub reports could be generated - sales per month/week,
# when to restock a particular item of inventory, best sellers, etc.
#


def inventoryreport(cur):
    print('''
          <h2>Inventory Report</h2>
          <table border="2"><tr>
          <td align="center">Product SKU</td><td align="center">Product Name</td><td align="center">Quantity in Stock</td>
          <td align="center">Retail Price</td><td align="center">Cost</td>
          </tr>
''')
    sql = 'SELECT * FROM inventory'
    cur.execute(sql)
    for row in cur.fetchall():      # Loop through inventory table
        sku = row[1]
        productname = row[2]
        quantity = row[3]
#        cost = float(row[4])
        cost = str("{0:.2f}".format(row[4]))
        retailprice = float(row[5])
        retailprice = str("{0:.2f}".format(retailprice))
        print('''<tr>
                 <td align="right">{SKU}</td>
                 <td align="right">{ProductName}</td>
                 <td align="right">{Quantity}</td>
                 <td align="right">${RetailPrice}</td>
                 <td align="right">${Cost}</td>
                 </tr>'''.format(Cost=cost, RetailPrice=retailprice, SKU=sku, ProductName=productname, Quantity=quantity))

    print('''<table>
          <p><a href='mainmenu.py'>Return to the main menu</a>
''')






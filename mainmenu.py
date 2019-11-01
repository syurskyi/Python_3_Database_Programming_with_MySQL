#!C:\Python34\python.exe
import cgi
import htmlhelpers
import dbhelpers

# Connect to database
conn = dbhelpers.connecttodb()
cur = conn.cursor()

#
# Get input from form if any. If none, print main menu.
# variable screen tells the program what section to process.
# Other variables (if any) are retrived in the section functionality
#
formdata = cgi.FieldStorage()

#
# Create a "pseudo switch" for the various values formdata can contain
#
# Do an orderly exit
#
if (formdata.getfirst('screen', '') == 'Exit'):
    htmlhelpers.printheader('Main Menu')
    print('Goodbye!')
    htmlhelpers.printfooter()
    # close database
    conn.close()

#
# The following are Inventory Related function calls
#
#
elif (formdata.getfirst('screen', '') == 'Inventory'):
    htmlhelpers.printheader('Inventory Menu')
    htmlhelpers.inventory()
    htmlhelpers.printfooter()
elif (formdata.getfirst('screen', '') == 'AddInventory'):
    htmlhelpers.printheader('Add Inventory')
    htmlhelpers.addinventory(cur, formdata, formdata.getfirst('subcommand', ''))
    htmlhelpers.printfooter()
elif (formdata.getfirst('screen', '') == 'EditInventory'):
    htmlhelpers.printheader('Edit Inventory')
    htmlhelpers.editinventory(cur, formdata, formdata.getfirst('subcommand', ''))
    htmlhelpers.printfooter()
elif (formdata.getfirst('screen', '') == 'DeleteInventory'):
    htmlhelpers.printheader('Delete Inventory')
    htmlhelpers.deleteinventory(cur, formdata, formdata.getfirst('subcommand', ''))
    htmlhelpers.printfooter()
#
# The following are Sales Related function calls
#
#
elif (formdata.getfirst('screen', '') == 'Sale'):
    htmlhelpers.printheader('Record a Sale')
    htmlhelpers.sale(cur)
    htmlhelpers.printfooter()
elif (formdata.getfirst('screen', '') == 'RecordSale'):
    htmlhelpers.printheader('Record a Sale')
    htmlhelpers.recordsale(cur, formdata)
    htmlhelpers.printfooter()
#
# The following are Return Related function calls
#
#
elif (formdata.getfirst('screen', '') == 'Return'):
    htmlhelpers.printheader('Process a Return')
    htmlhelpers.returns(cur)
    htmlhelpers.printfooter()
elif (formdata.getfirst('screen', '') == 'DisplayPurchases'):
    htmlhelpers.printheader('Process a Return')
    htmlhelpers.displaypurchases(cur, formdata)
    htmlhelpers.printfooter()
elif (formdata.getfirst('screen', '') == 'ProcessReturn'):
    htmlhelpers.printheader('Process a Return')
    htmlhelpers.processreturn(cur, formdata)
    htmlhelpers.printfooter()
#
# The following are Report Related function calls
#
#
elif (formdata.getfirst('screen', '') == 'Reports'):
    htmlhelpers.printheader('Generate a Report')
    htmlhelpers.reports()
    htmlhelpers.printfooter()
elif (formdata.getfirst('screen', '') == 'TotalSales'):
    htmlhelpers.printheader('Generate Total Sales Report')
    htmlhelpers.totalsales(cur)
    htmlhelpers.printfooter()
elif (formdata.getfirst('screen', '') == 'SalesByCustomer'):
    htmlhelpers.printheader('Generate Sales by Customer Report')
    htmlhelpers.salesbycustomer(cur)
    htmlhelpers.printfooter()
elif (formdata.getfirst('screen', '') == 'InventoryReport'):
    htmlhelpers.printheader('Generate Inventory Report')
    htmlhelpers.inventoryreport(cur)
    htmlhelpers.printfooter()

#
# Print the main menu as the last choice
#
else:
    htmlhelpers.printheader('Main Menu')
    htmlhelpers.mainmenu()
    htmlhelpers.printfooter()



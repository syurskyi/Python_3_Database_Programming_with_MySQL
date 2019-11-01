#!C:\Python34\python.exe
import cgi
import htmlhelpers
import dbhelpers

# Connect to database
conn = dbhelpers.connecttodb()
cur = conn.cursor()

# Create database tables - or do nothing if tables already exist
dbhelpers.createtables(cur)

htmlhelpers.printheader('Main Menu')
print('Database is set up and ready to use. <a href="mainmenu.py">Run Main Menu')
htmlhelpers.printfooter()

# close database
conn.close()


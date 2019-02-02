#!/usr/bin/python
# speichern unter: /usr/lib/cgi-bin/
import sqlite3

dbname='/var/www/remote/temp_data3.db'

#-------------------------------------------------------------------------------------------------------

def display_data():

    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    for row in curs.execute("SELECT * FROM temps ORDER BY timestamp DESC LIMIT 1;"):
	  print str(row[3])
      
    conn.close()


#-------------------------------------------------------------------------------------------------------
def main():
 display_data()
main()

#----------------------------------------------------------------------------------

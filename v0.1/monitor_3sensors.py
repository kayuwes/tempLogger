#!/usr/bin/env python
#speichern unter /usr/lib/cgi-bin/
import sqlite3

import os
import time
import glob

#-------------------------------------------------------------------------------------------------------
# global variables
speriod=(15*60)-1
#speriod=(5*60)-1
dbname='/var/www/temp_data3.db'

# adjustments for probes. values can be positive or negative.
adjch0=0
adjch1=0
adjch2=0
adjch3=-1.5
adjch4=-1.5

# read bounds for probes, probe readings not within bounds will be retried
hibound=100
lobound=20


#-------------------------------------------------------------------------------------------------------
# store the temperature in the database
def log_temperature(temp0,temp1,temp2):

    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    curs.execute("INSERT INTO temps values(datetime('now','localtime'), (?), (?), (?))", (temp0,temp1,temp2))

    # commit the changes
    conn.commit()

    conn.close()

#-------------------------------------------------------------------------------------------------------
# display the contents of the database
def display_data():

    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    for row in curs.execute("SELECT * FROM temps"):
        print str(row[0])+"	"+str(row[1])+"	"+str(row[2])+"	"+str(row[3])

    conn.close()


#-------------------------------------------------------------------------------------------------------
# get temperature
# returns None on error, or the temperature as a float
def get_temp(devicefile):

    try:
        fileobj = open(devicefile,'r')
        lines = fileobj.readlines()
        fileobj.close()
    except:
        return None

    # get the status from the end of line 1 
    status = lines[0][-4:-1]

# Commented out this section and replaced with next section

    # is the status is ok, get the temperature from line 2
    #if status=="YES":
    #    print status
    #    tempstr= lines[1][-6:-1]
    #    tempvalue=float(tempstr)/1000
    #    print tempvalue
    #    return tempvalue
    
    equals_pos = lines[1].find('t=')
    if equals_pos != -1: 
        tempstr = lines[1][equals_pos+2:]
        print tempstr
        tempvalue_c=float(tempstr)/1000.0
        print tempvalue_c
        tempvalue_f = tempvalue_c * 9.0 / 5.0 +132.0
        print tempvalue_c
        tempvalue = round(tempvalue_c,1)
        print tempvalue
        return tempvalue
        
    else:
        print "There was an error."
        return None


#-------------------------------------------------------------------------------------------------------
# main function
# This is where the program starts 
def main():

    # enable kernel modules
    os.system('sudo modprobe w1-gpio')
    os.system('sudo modprobe w1-therm')

    # search for a device file that starts with 28
    devicelist = glob.glob('/sys/bus/w1/devices/28*')
    if devicelist=='':
        return None
    else:
        # append /w1slave to the device file
        w1devicefile0 = devicelist[0] + '/w1_slave'
        w1devicefile1 = devicelist[1] + '/w1_slave'
        w1devicefile2 = devicelist[2] + '/w1_slave'
#        w1devicefile3 = devicelist[3] + '/w1_slave'
#        w1devicefile4 = devicelist[4] + '/w1_slave'

#    while True:

    # get the first temperature from the first device file
    temperature0 = get_temp(w1devicefile0)+adjch0
    if temperature0 != None and temperature0 > lobound and temperature0 < hibound:
        print "temperature0="+str(temperature0)
    else:
        # Sometimes reads fail on the first attempt
        # so we need to retry
        temperature0 = get_temp(w1devicefile0)+adjch0
        print "temperature0="+str(temperature0)

    # get the second temperature from the second device file
    temperature1 = get_temp(w1devicefile1)+adjch1
    if temperature1 != None and temperature1 > lobound and temperature1 < hibound:
        print "temperature1="+str(temperature1)
    else:
        # Sometimes reads fail on the first attempt
        # so we need to retry
        temperature1 = get_temp(w1devicefile1)+adjch1
        print "temperature1="+str(temperature1)

    # get the third temperature from the third device file
    temperature2 = get_temp(w1devicefile2)+adjch2
    if temperature2 != None and temperature2 > lobound and temperature2 < hibound:
        print "temperature2="+str(temperature2)
    else:
        # Sometimes reads fail on the first attempt
        # so we need to retry
        temperature2 = get_temp(w1devicefile2)+adjch2
        print "temperature2="+str(temperature2)

    # get the fourth temperature from the fourth device file
#    temperature3 = get_temp(w1devicefile3)+adjch3
#    if temperature3 != None and temperature3 > lobound and temperature3 < hibound:
#        print "temperature3="+str(temperature3)
#    else:
        # Sometimes reads fail on the first attempt
        # so we need to retry
#        temperature3 = get_temp(w1devicefile3)+adjch3
#        print "temperature3="+str(temperature3)

    # get the fifth temperature from the fifth device file
#    temperature4 = get_temp(w1devicefile4)+adjch4
#    if temperature4 != None and temperature4 > lobound and temperature4 < hibound:
#        print "temperature4="+str(temperature4)
#    else:
        # Sometimes reads fail on the first attempt
        # so we need to retry
#        temperature4 = get_temp(w1devicefile4)+adjch4
#        print "temperature4="+str(temperature4)


        # Store the five temperatures in the database
    log_temperature(temperature0,temperature1,temperature2)

        # display the contents of the database
#    display_data()

#        time.sleep(speriod)


if __name__=="__main__":
    main()






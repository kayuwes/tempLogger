#!/usr/bin/env python

import sqlite3
import os
import time
import glob

#-------------------------------------------------------------------------------------------------------
# global variables
speriod=(15*60)-1
#speriod=(5*60)-1
dbname='/var/www/temp_data2.db'

# adjustments for probes. values can be positive or negative.
adjch0=0
adjch1=0

# read bounds for probes, probe readings not within bounds will be retried
# set to desired limit values
hibound=100
lobound=20

#-------------------------------------------------------------------------------------------------------
# store the temperature in the database
def log_temperature(temp0,temp1):

    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    curs.execute("INSERT INTO temps values(datetime('now','localtime'), (?), (?))", (temp0,temp1))

    # commit the changes
    conn.commit()

    conn.close()

#-------------------------------------------------------------------------------------------------------
# display the contents of the database
def display_data():

    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    for row in curs.execute("SELECT * FROM temps"):
        print str(row[0])+"	"+str(row[1])+"	"+str(row[2])

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

    equals_pos = lines[1].find('t=')
    if equals_pos != -1: 
        tempstr = lines[1][equals_pos+2:]
        print tempstr
        tempvalue_c=float(tempstr)/1000.0
        print tempvalue_c
        tempvalue_f = tempvalue_c * 9.0 / 5.0 + 32.0
        print tempvalue_f
        tempvalue = round(tempvalue_f,1)
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


        # Store the two temperatures in the database
    log_temperature(temperature0,temperature1)

        # display the contents of the database
    display_data()

#        time.sleep(speriod)


if __name__=="__main__":
    main()






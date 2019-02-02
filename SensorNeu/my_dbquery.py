#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import time
import datetime
import my_settings
from my_settings import *

#print (db)
TIMENOW = int(time.time())
#print(TIMENOW)
#print(datetime.datetime.fromtimestamp(int(TIMENOW)).strftime('%Y-%m-%d %H:%M:%S'))
# calculate Timestamp from Time ago
currentTIMEago = TIMENOW - span3DAY
#print(currentTIMEago)

# Database select query helper.
con = lite.connect(db)
db = con.cursor()

# Execute the select.
def min1():#evtl ist MAXIMUM überflüssig
    db.execute("SELECT min(C), DeviceID, Timestamp, C FROM Temperature WHERE DeviceID = 1 AND Timestamp >=?",
               (currentTIMEago,))
    result = db.fetchall()
    for r in result:
        print ("Min1: " + datetime.datetime.fromtimestamp(int(r[2])).strftime('%d.%m. %H:%M')+" " + str(r[3])+"°C")

def min2():
    db.execute("SELECT min(C), DeviceID, Timestamp, C FROM Temperature WHERE DeviceID = 2 AND Timestamp >=?",
               (currentTIMEago,))
    result = db.fetchall()
    for r in result:
        print ("Min2: " + datetime.datetime.fromtimestamp(int(r[2])).strftime('%d.%m. %H:%M')+" " + str(r[3])+"°C")

def min3():
    db.execute("SELECT min(C), DeviceID, Timestamp, C FROM Temperature WHERE DeviceID = 3 AND Timestamp >=?",
               (currentTIMEago,))
    result = db.fetchall()
    for r in result:
        print ("Min3: " + datetime.datetime.fromtimestamp(int(r[2])).strftime('%d.%m. %H:%M')+" " + str(r[3])+"°C")

def max1():
    db.execute("SELECT max(C), DeviceID, Timestamp, C FROM Temperature WHERE DeviceID = 1 AND Timestamp >=?",
               (currentTIMEago,))
    result = db.fetchall()
    for r in result:
        print ("Max1: " + datetime.datetime.fromtimestamp(int(r[2])).strftime('%d.%m. %H:%M')+" " + str(r[3])+"°C")

def max2():
    db.execute("SELECT max(C), DeviceID, Timestamp, C FROM Temperature WHERE DeviceID = 2 AND Timestamp >=?",
               (currentTIMEago,))
    result = db.fetchall()
    for r in result:
        print ('Max2: {0} {1}°C'.format(datetime.datetime.fromtimestamp(int(r[2])).strftime('%d.%m. %H:%M'), str(r[3])))


def max3():
    db.execute("SELECT max(C), DeviceID, Timestamp, C FROM Temperature WHERE DeviceID = 3 AND Timestamp >=?",
               (currentTIMEago,))
    result = db.fetchall()
    for r in result:
        print ("Max3: {0} {1}°C".format(datetime.datetime.fromtimestamp(int(r[2])).strftime('%d.%m. %H:%M'), str(r[3])))

while 1:
    warten = 1
    min1()
    time.sleep(warten)
    min2()
    time.sleep(warten)
    min3()
    time.sleep(warten)
    max1()
    time.sleep(warten)
    max2()
    time.sleep(warten)
    max3()



#rows = db.fetchall()
con.close()


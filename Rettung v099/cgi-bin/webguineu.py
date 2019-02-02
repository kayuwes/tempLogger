#!/usr/bin/env python

import sqlite3
import sys
import cgi
import cgitb
import os

#---------------------------------------------------------------------------------------------------------------------------------
# global variables
speriod=(15*60)-1
dbname='/var/www/temp_data3.db'


#---------------------------------------------------------------------------------------------------------------------------------
# print the HTTP header
def printHTTPheader():
    print "Content-type: text/html\n\n"


#---------------------------------------------------------------------------------------------------------------------------------
# print the HTML head section
# arguments are the page title and the table for the chart
def printHTMLHead(title, table):
    print "<head>"
    print "    <title>"
    print title
    print "    </title>"
    
    print_graph_script(table)

    print "</head>"

#---------------------------------------------------------------------------------------------------------------------------------
# get data from the database
# if an interval is passed, 
# return a list of records from the database
def get_data(interval):

    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    if interval == None:
        curs.execute("SELECT * FROM temps")
    else:
        curs.execute("SELECT * FROM temps WHERE timestamp>datetime('now','localtime','-%s hours')" % interval)
#        curs.execute("SELECT * FROM temps WHERE timestamp>datetime('2013-09-19 21:30:02','-%s hours') AND timestamp<=datetime('2013-09-19 21:31:02')" % interval)

    rows=curs.fetchall()

    conn.close()

    return rows

#---------------------------------------------------------------------------------------------------------------------------------
# convert rows from database into a javascript table
def create_table(rows):
    chart_table=""

    for row in rows[:-1]:
        rowstr="['{0}', {1}, {2}, {3}],\n".format(str(row[0]),str(row[1]),str(row[2]),str(row[3]))
        chart_table+=rowstr

    row=rows[-1]
    rowstr="['{0}', {1}, {2}, {3}]\n".format(str(row[0]),str(row[1]),str(row[2]),str(row[3]))
    chart_table+=rowstr

    return chart_table

#---------------------------------------------------------------------------------------------------------------------------------
# print the javascript to generate the chart
# pass the table generated from the database info
def print_graph_script(table):

    # google chart snippet
    chart_code="""
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load("visualization", "1", {packages:["corechart"]});
      google.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = google.visualization.arrayToDataTable([
          ['Time', 'Ch0 Room', 'Ch1 Tower Air', 'Ch2 Upper Air'],
%s
        ]);

        var options = {
          title: 'Temperature Chart'
        };

        var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
        chart.draw(data, options);
      }
    </script>"""

    print chart_code % (table)



#---------------------------------------------------------------------------------------------------------------------------------
# print the div that contains the graph
def show_graph():
#    print "<h2>Temperature Chart</h2>"
    print '<div id="chart_div" style="width: 1200px; height: 800px;"></div>'


#---------------------------------------------------------------------------------------------------------------------------------
# connect to the db and show some stats
# argument option is the number of hours
def show_stats(option):

    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    if option is None:
        option = str(24)

#    curs.execute("SELECT timestamp,max(temp0) FROM temps WHERE timestamp>datetime('now','localtime','-%s hour') AND timestamp<=datetime('now','localtime')" % option)
    curs.execute("SELECT max(temp0) FROM temps WHERE timestamp>datetime('now','localtime','-%s hour') AND timestamp<=datetime('now','localtime')" % option)
#    curs.execute("SELECT timestamp,max(temp0) FROM temps WHERE timestamp>datetime('2014-03-18 00:00:00','-%s hour') AND timestamp<=datetime('2014-03-18 20:45:00')" % option)
    rowmax0=curs.fetchone()
#    rowstrmax0="&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp{0}&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp{1}F".format(str(rowmax0[0]),str(rowmax0[1]))

#    curs.execute("SELECT timestamp,max(temp1) FROM temps WHERE timestamp>datetime('now','localtime','-%s hour') AND timestamp<=datetime('now','localtime')" % option)
    curs.execute("SELECT max(temp1) FROM temps WHERE timestamp>datetime('now','localtime','-%s hour') AND timestamp<=datetime('now','localtime')" % option)    
    rowmax1=curs.fetchone()
#    rowstrmax1="&nbsp&nbsp&nbsp&nbsp&nbsp{0}F&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp{1}".format(str(rowmax1[1]),str(rowmax1[0]))

#    curs.execute("SELECT timestamp,max(temp2) FROM temps WHERE timestamp>datetime('now','localtime','-%s hour') AND timestamp<=datetime('now','localtime')" % option)
    curs.execute("SELECT max(temp2) FROM temps WHERE timestamp>datetime('now','localtime','-%s hour') AND timestamp<=datetime('now','localtime')" % option)
    rowmax2=curs.fetchone()
#    rowstrmax2="&nbsp&nbsp&nbsp&nbsp&nbsp{0}F&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp{1}".format(str(rowmax2[0]),str(rowmax2[1]))

#    curs.execute("SELECT timestamp,max(temp3) FROM temps WHERE timestamp>datetime('now','localtime','-%s hour') AND timestamp<=datetime('now','localtime')" % option)
#    curs.execute("SELECT max(temp3) FROM temps WHERE timestamp>datetime('now','localtime','-%s hour') AND timestamp<=datetime('now','localtime')" % option)
#    rowmax3=curs.fetchone()
#    rowstrmax3="&nbsp&nbsp&nbsp&nbsp&nbsp{0}F&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp{1}".format(str(rowmax2[0]),str(rowmax2[1]))

#    curs.execute("SELECT timestamp,max(temp4) FROM temps WHERE timestamp>datetime('now','localtime','-%s hour') AND timestamp<=datetime('now','localtime')" % option)
#    curs.execute("SELECT max(temp4) FROM temps WHERE timestamp>datetime('now','localtime','-%s hour') AND timestamp<=datetime('now','localtime')" % option)
#   rowmax4=curs.fetchone()
#    rowstrmax4="&nbsp&nbsp&nbsp&nbsp&nbsp{0}F&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp{1}".format(str(rowmax2[0]),str(rowmax2[1]))

    
#    curs.execute("SELECT timestamp,min(temp0) FROM temps WHERE timestamp>datetime('now','localtime','-%s hour') AND timestamp<=datetime('now','localtime')" % option)
    curs.execute("SELECT min(temp0) FROM temps WHERE timestamp>datetime('now','localtime','-%s hour') AND timestamp<=datetime('now','localtime')" % option)
#    curs.execute("SELECT timestamp,min(temp0) FROM temps WHERE timestamp>datetime('2014-03-18 00:00:00','-%s hour') AND timestamp<=datetime('2014-03-18 20:45:00')" % option)
    rowmin0=curs.fetchone()
#    rowstrmin0="&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp{0}&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp{1}F".format(str(rowmin0[0]),str(rowmin0[1]))

#    curs.execute("SELECT timestamp,min(temp1) FROM temps WHERE timestamp>datetime('now','localtime','-%s hour') AND timestamp<=datetime('now','localtime')" % option)
    curs.execute("SELECT min(temp1) FROM temps WHERE timestamp>datetime('now','localtime','-%s hour') AND timestamp<=datetime('now','localtime')" % option)
    rowmin1=curs.fetchone()
#    rowstrmin1="&nbsp&nbsp&nbsp&nbsp&nbsp{0}F&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp{1}".format(str(rowmin1[1]),str(rowmin1[0]))

#    curs.execute("SELECT timestamp,min(temp2) FROM temps WHERE timestamp>datetime('now','localtime','-%s hour') AND timestamp<=datetime('now','localtime')" % option)
    curs.execute("SELECT min(temp2) FROM temps WHERE timestamp>datetime('now','localtime','-%s hour') AND timestamp<=datetime('now','localtime')" % option)
    rowmin2=curs.fetchone()
#    rowstrmin2="&nbsp&nbsp&nbsp&nbsp&nbsp{0}F&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp{1}".format(str(rowmin2[0]),str(rowmin2[1]))

#    curs.execute("SELECT timestamp,min(temp3) FROM temps WHERE timestamp>datetime('now','localtime','-%s hour') AND timestamp<=datetime('now','localtime')" % option)
#    curs.execute("SELECT min(temp3) FROM temps WHERE timestamp>datetime('now','localtime','-%s hour') AND timestamp<=datetime('now','localtime')" % option)
#    rowmin3=curs.fetchone()
#    rowstrmin3="&nbsp&nbsp&nbsp&nbsp&nbsp{0}F&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp{1}".format(str(rowmin2[0]),str(rowmin2[1]))

#    curs.execute("SELECT timestamp,min(temp4) FROM temps WHERE timestamp>datetime('now','localtime','-%s hour') AND timestamp<=datetime('now','localtime')" % option)
#    curs.execute("SELECT min(temp4) FROM temps WHERE timestamp>datetime('now','localtime','-%s hour') AND timestamp<=datetime('now','localtime')" % option)
#    rowmin4=curs.fetchone()
#    rowstrmin4="&nbsp&nbsp&nbsp&nbsp&nbsp{0}F&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp{1}".format(str(rowmin2[0]),str(rowmin2[1]))


    curs.execute("SELECT avg(temp0) FROM temps WHERE timestamp>datetime('now','localtime','-%s hour') AND timestamp<=datetime('now','localtime')" % option)
#    curs.execute("SELECT avg(temp0) FROM temps WHERE timestamp>datetime('2014-03-18 00:00:00','-%s hour') AND timestamp<=datetime('2014-03-18 20:45:00')" % option)
    rowavg0=curs.fetchone()

    curs.execute("SELECT avg(temp1) FROM temps WHERE timestamp>datetime('now','localtime','-%s hour') AND timestamp<=datetime('now','localtime')" % option)
    rowavg1=curs.fetchone()

    curs.execute("SELECT avg(temp2) FROM temps WHERE timestamp>datetime('now','localtime','-%s hour') AND timestamp<=datetime('now','localtime')" % option)
    rowavg2=curs.fetchone()

#    curs.execute("SELECT avg(temp3) FROM temps WHERE timestamp>datetime('now','localtime','-%s hour') AND timestamp<=datetime('now','localtime')" % option)
#   rowavg3=curs.fetchone()

#   curs.execute("SELECT avg(temp4) FROM temps WHERE timestamp>datetime('now','localtime','-%s hour') AND timestamp<=datetime('now','localtime')" % option)
#    rowavg4=curs.fetchone()


    curs.execute("SELECT MAX(timestamp),temp0,temp1,temp2 FROM temps")
    rownow=curs.fetchone()
#    rowstrnow="&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp{0}&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp{1}F&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp{2}F&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp{3}F&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp{4}F&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp{5}F".format(str(rownow[0]),str(rownow[1]),str(rownow[2]),str(rownow[3]))
    rowstrnow="&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp{0}F&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp{1}F&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp{2}F&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp{3}F&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp{4}F".format(str(rownow[1]),str(rownow[2]),str(rownow[3]))


    print "<hr>"

    print "<h2>Current Temperatures&nbsp&nbsp&nbsp&nbsp&nbsp&nbspCh0&nbsp&nbsp&nbsp&nbsp&nbspCh1&nbsp&nbsp&nbsp&nbsp&nbspCh2&nbsp&nbsp&nbsp&nbsp&nbspCh3&nbsp&nbsp&nbsp&nbsp&nbspCh4</h2>"
    print rowstrnow
    print "<h2>Minimum Temperature &nbsp&nbsp&nbsp&nbspCh0&nbsp&nbsp&nbsp&nbsp&nbspCh1&nbsp&nbsp&nbsp&nbsp&nbspCh2&nbsp&nbsp&nbsp&nbsp&nbspCh3&nbsp&nbsp&nbsp&nbsp&nbspCh4</h2>"
#    print rowstrmin0, rowstrmin1, rowstrmin2, rowstrmin3, rowstrmin4
    print "&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp%.3f" % rowmin0+"F", "&nbsp&nbsp&nbsp&nbsp%.3f" % rowmin1+"F", "&nbsp&nbsp&nbsp&nbsp%.3f" % rowmin2+"F"
    print "<h2>Maximum Temperature &nbsp&nbsp&nbspCh0&nbsp&nbsp&nbsp&nbsp&nbspCh1&nbsp&nbsp&nbsp&nbsp&nbspCh2&nbsp&nbsp&nbsp&nbsp&nbspCh3&nbsp&nbsp&nbsp&nbsp&nbspCh4</h2>"
#    print rowstrmax0, rowstrmax1, rowstrmax2, rowstrmin3, rowstrmin4
    print "&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp%.3f" % rowmax0+"F", "&nbsp&nbsp&nbsp&nbsp%.3f" % rowmax1+"F", "&nbsp&nbsp&nbsp&nbsp%.3f" % rowmax2+"F"
    print "<h2>Average Temperatures &nbsp&nbsp&nbsp&nbspCh0&nbsp&nbsp&nbsp&nbsp&nbspCh1&nbsp&nbsp&nbsp&nbsp&nbspCh2&nbsp&nbsp&nbsp&nbsp&nbspCh3&nbsp&nbsp&nbsp&nbsp&nbspCh4</h2>"
    print "&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp%.3f" % rowavg0+"F", "&nbsp&nbsp&nbsp&nbsp%.3f" % rowavg1+"F", "&nbsp&nbsp&nbsp&nbsp%.3f" % rowavg2+"F"
    print "<hr>"

    print "<h2>In the last hour:</h2>"
    print "<table>"
    print "<tr><td><strong>Date/Time</strong></td><td><strong>Ch0 Temp</strong>&emsp;&emsp;</td><td><strong>Ch1 Temp</strong>&emsp;&emsp;&emsp;</td><td><strong>Ch2 Temp</strong>&emsp;&emsp;&emsp;</td><td><strong>Ch3 Temp</strong>&emsp;&emsp;&emsp;</td><td><strong>Ch4 Temp</strong></td></tr>"

    rows=curs.execute("SELECT * FROM temps WHERE timestamp>datetime('now','localtime','-1 hour') AND timestamp<=datetime('now','localtime')")
#    rows=curs.execute("SELECT * FROM temps WHERE timestamp>datetime('2014-03-18 00:00:00','-1 hour') AND timestamp<=datetime('2014-03-18 20:45:00')")
    for row in rows:
        rowstr="<tr><td>{0}&emsp;&emsp;</td><td>{1}F&emsp;&emsp;</td><td>{2}F&emsp;&emsp;</td><td>{3}F&emsp;&emsp;</td><td>{4}F&emsp;&emsp;</td><td>{5}F&emsp;</td></tr>".format(str(row[0]),str(row[1]),str(row[2]),str(row[3]))
        print rowstr
    print "</table>"

    print "<hr>"

    conn.close()



#---------------------------------------------------------------------------------------------------------------------------------
def print_time_selector(option):

    print """<form action="/cgi-bin/webgui.py" method="POST">
        Show the temperature logs for  
        <select name="timeinterval">"""


    if option is not None:

        if option == "1":
            print "<option value=\"1\" selected=\"selected\">the last hour</option>"
        else:
            print "<option value=\"1\">the last hour</option>"

        if option == "6":
            print "<option value=\"6\" selected=\"selected\">the last 6 hours</option>"
        else:
            print "<option value=\"6\">the last 6 hours</option>"

        if option == "12":
            print "<option value=\"12\" selected=\"selected\">the last 12 hours</option>"
        else:
            print "<option value=\"12\">the last 12 hours</option>"

        if option == "24":
            print "<option value=\"24\" selected=\"selected\">the last 24 hours</option>"
        else:
            print "<option value=\"24\">the last 24 hours</option>"

        if option == "48":
            print "<option value=\"48\" selected=\"selected\">the last two days</option>"
        else:
            print "<option value=\"48\">the last two days</option>"

        if option == "168":
            print "<option value=\"168\" selected=\"selected\">the last week</option>"
        else:
            print "<option value=\"168\">the last week</option>"

        if option == "240":
            print "<option value=\"240\" selected=\"selected\">the last 10 days</option>"
        else:
            print "<option value=\"240\">the last 10 days</option>"


    else:
        print """<option value="1">the last hour</option>
            <option value="6">the last 6 hours</option>
            <option value="12">the last 12 hours</option>
            <option value="24" selected="selected">the last 24 hours</option>
            <option value="48" selected="selected">the last two days</option>
            <option value="168" selected="selected">the last week</option>
            <option value="240" selected="selected">the 10 days</option>"""

    print """        </select>
        <input type="submit" value="Display">
    </form>"""

#---------------------------------------------------------------------------------------------------------------------------------
# check that the option is valid
# and not an SQL injection
def validate_input(option_str):
    # check that the option string represents a number
    if option_str.isalnum():
        # check that the option is within a specific range
        if int(option_str) > 0 and int(option_str) <= 240:
            return option_str
        else:
            return None
    else: 
        return None

#---------------------------------------------------------------------------------------------------------------------------------
#return the option passed to the script
def get_option():
    form=cgi.FieldStorage()
    if "timeinterval" in form:
        option = form["timeinterval"].value
        return validate_input (option)
    else:
        return None


#---------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------
# main function
# This is where the program starts 
def main():

    cgitb.enable()

    # get options that may have been passed to this script
    option=get_option()

    if option is None:
        option = str(24)

    # get data from the database
    records=get_data(option)

    # print the HTTP header
    printHTTPheader()

    if len(records) != 0:
        # convert the data into a table
        table=create_table(records)
    else:
        print "No data found"
        return

    # start printing the page
    print "<html>"
    # print the head section including the table
    # used by the javascript for the chart
    printHTMLHead("Temperature Logger", table)

    # print the page body
    print "<body>"
    print "<h1>Temperature Logger</h1>"
    print "<hr>"
    print_time_selector(option)
    show_graph()
    show_stats(option)
    print "</body>"
    print "</html>"

    sys.stdout.flush()

if __name__=="__main__":
    main()
#---------------------------------------------------------------------------------------------------------------------------------




#!/usr/bin/env python
import os
import re
#Variable
#DATEI='schalter'
DATEI='/var/www/remote/schalter'		
def main():
	os.system('/usr/local/bin/gpio -g mode 18 out')
        fobj = open(DATEI,"r")
        lines = fobj.readlines()
        fobj.close()

    # get the status from the end of line 1 
        status = lines[0]
	print status
#Wenn An
        if re.search("AN",status):os.system('/usr/local/bin/gpio -g write 18 0')
#Oder Aus 	
	if re.search("AUS",status):os.system('/usr/local/bin/gpio -g write 18 1') 


main()


#!/usr/bin/env python
import os
import re
		
def main():

        fobj = open("stat.txt","r")
        lines = fobj.readlines()
        fobj.close()

    # get the status from the end of line 1 
        status = lines[0]
	print status
#WennAn
        if re.search("AN",status):print("EINSCHALTEN")
	os.system('/usr/local/bin/gpio -g mode 18 out')
	os.system('/usr/local/bin/gpio -g write 18 1')
 	
	if re.search("AUS",status):print("AUSSCHALTEN")
        os.system('/usr/local/bin/gpio -g mode 18 out')
        os.system('/usr/local/bin/gpio -g write 18 0') 


main()


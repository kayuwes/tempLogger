#!/usr/bin/env python
import os

def main():

    # enable kernel modules
    os.system('/usr/local/bin/gpio -g mode 18 out')
    os.system('/usr/local/bin/gpio -g write 18 0')
main()


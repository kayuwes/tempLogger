import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)
#GPIO.setwarnings(False)
#GPIO.cleanup()
while True:
#GPIO.cleanup(18)	
        GPIO.output(18,True)
	time.sleep(0.1)
        GPIO.output(18,False)
	time.sleep(3)

GPIO.cleanup()

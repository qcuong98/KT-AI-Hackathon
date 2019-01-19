import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BOARD)

GPIO.setup(31, GPIO.OUT)
GPIO.output(31, GPIO.HIGH)
time.sleep(10)
GPIO.output(31, GPIO.LOW)

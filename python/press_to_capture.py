#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gkit
import time
import picamera
import os
import sys

cnt = 0
camera = picamera.PiCamera()

def onButtonHandler():
    global cnt
    global camera
    global name
    print ("Button was pressed")
    camera.capture('%s/%02d.jpg' % (name, cnt))
    cnt += 1

def sample():
    camera.resolution = (800, 600)
    camera.start_preview()

    # button
    gkit.get_button().on_press(onButtonHandler)

    message = input("Press enter to quit\n\n")
    
    #GPIO.cleanup()

def main():
    global name
    name = sys.argv[1]
    if not os.path.exists(name):
        os.makedirs(name)
    sample()

if __name__ == '__main__':
    main()

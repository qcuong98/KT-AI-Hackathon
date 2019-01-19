import picamera
import os
import sys
import authenticate as auth

def main():
    camera = picamera.PiCamera()
    camera.resolution = (200, 150)
    camera.start_preview()
    while(True):
        camera.capture('tmp.jpg')
        result = auth.authenticate('tmp.jpg')
        if (result[0]):
            print('Welcome %s' % result[1])
        else:
            print('Sad: %s' % result[1])

main()

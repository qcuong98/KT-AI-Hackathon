import picamera
import os
import sys
import authenticate as auth
import gkit
import time
import shutil

def main():
    camera = picamera.PiCamera()
    camera.resolution = (200, 150)
    camera.start_preview()
    start = time.time()

    door_open = False

    UNKNOWN_PATH = 'unknown.jpg'
    TEMP_PATH = 'tmp.jpg'

    while True:
        if os.path.isfile(UNKNOWN_PATH):
            os.remove(UNKNOWN_PATH)

        camera.capture(TEMP_PATH)
        result = auth.authenticate(TEMP_PATH)
        if result[0] == 0:
            print('Welcome %s' % result[1])
            door_open = True
            break;
        
        else:
            print('Sad: %s' % result[1])
        
        if result[0] != 1:
            shutil.copy(TEMP_PATH, UNKNOWN_PATH)
        
        if time.time() - start > 5:
            print('Your time ran out')
            break;

    camera.stop_preview()
    camera.close()

    if door_open:
        print('Door open')
    else:
        if os.path.isfile(UNKNOWN_PATH):
            auth.cut_face(UNKNOWN_PATH);

    return door_open

print('Library loaded')
gkit.get_button().on_press(main)

input('Press enter to stop\n\n')

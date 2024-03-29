import picamera
import os
import sys
import authenticate as auth
import gkit
import time
import shutil
import firebase_admin
from firebase_admin import credentials, db
import datetime
import urllib
import json
import pyaudio
import wave

TRY_LIMIT = 3
PASSWORD = 'never'
UNKNOWN_PATH = 'unknown.jpg'

cnt_attempt = 0

def login_by_password():
    global cnt_attempt
    cnt_attempt += 1
    # do you want to enter password
    gkit.tts_play('암호를 입력 하시겠습니까')
    text = gkit.getVoice2Text()
    print(text)
    # yes
    if (cnt_attempt % 3 != 0):
    # if (text.find('예') >= 0 or text.find('yes') >= 0):
        # input plz
        gkit.tts_play('환영')
        for no_try in range(TRY_LIMIT):
            password = gkit.getVoice2Text()
            print(password)
            if (password.find(PASSWORD) >= 0 and len(password) <= 5 * len(PASSWORD)):
                # welcome
                # gkit.tts_play('환영')
                return 1
            elif no_try < TRY_LIMIT - 1:
                # please try again
                gkit.tts_play('다시 시도해주세요.')
    else:
        # see you again
        gkit.tts_play('또 보자')
        return 0
    return -1

def upload_file(img_name, log_id):
    my_file = open(img_name, "rb")
    my_bytes = my_file.read()
    my_url = "https://firebasestorage.googleapis.com/v0/b/you-shall-not-pass-c59f3.appspot.com/o/images%2F" + log_id
    my_headers = {"Content-Type": "text/plain"}

    my_request = urllib.request.Request(my_url, data=my_bytes, headers=my_headers, method="POST")

    try:
        loader = urllib.request.urlopen(my_request)
    except urllib.error.URLError as e:
        message = json.loads(e.read().decode())
        print(message["error"]["message"])
        return ''
    else:
        #print(loader.read().decode())
        result = json.loads(loader.read().decode())
        return result["downloadTokens"]

def detect_person(detected):
    root = db.reference()
    
    if (not detected):
        new_log = root.child('Logs').push({
            'subject': 'WARNING',
            'timestamp': str(datetime.datetime.now()),
            'message': 'A suspicious person detected'
        })
    else:
        new_log = root.child('Logs').push({
            'subject': 'INFO',
            'timestamp': str(datetime.datetime.now()),
            'message': 'Door opened'
        })
    
    if os.path.isfile(UNKNOWN_PATH):
        auth.cut_face(UNKNOWN_PATH)
        log_id = new_log.key

        token = upload_file("cropped.jpg", log_id)
        url = 'https://firebasestorage.googleapis.com/v0/b/you-shall-not-pass-c59f3.appspot.com/o/images%2F' + log_id + '?alt=media&token=' + token

        new_log.update({
            'image': url
        })

def play_file(fname):
    # create an audio object
    wf = wave.open(fname, 'rb')
    p = pyaudio.PyAudio()
    chunk = 1024

    # open stream based on the wave object which has been input.
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # read data (based on the chunk size)
    data = wf.readframes(chunk)

    # play stream (looping from beginning of file to the end)
    while len(data) > 0:
        # writing to the stream is what *actually* plays the sound.
        stream.write(data)
        data = wf.readframes(chunk)

        # cleanup stuff.
    stream.close()
    p.terminate() 


# return true if detected
def face_detect():
    camera = picamera.PiCamera()
    camera.resolution = (200, 150)
    camera.start_preview()
    start = time.time()

    detected = False

    TEMP_PATH = 'tmp.jpg'

    while True:
        if os.path.isfile(UNKNOWN_PATH):
            os.remove(UNKNOWN_PATH)

        camera.capture(TEMP_PATH)
        result = auth.authenticate(TEMP_PATH)

        if result[0] != 1:
            shutil.copy(TEMP_PATH, UNKNOWN_PATH)

        if result[0] == 0:
            print('Welcome %s' % result[1])
            detected = True
            break
        else:
            print('Sad: %s' % result[1])
        
        if time.time() - start > 5:
            print('Your time ran out')
            break

    camera.stop_preview()
    camera.close()
 
    if not detected:
        #login
        val = login_by_password()
        if (val == 1):
            detected = True
        # do not want to input password
        elif (val == 0):
            # you shall not pass
            gkit.tts_play('너는지나 가지 않아야한다.')
            return detected

    detect_person(detected)

    if detected:
        play_file('../data/sample_sound.wav')
        # Play a welcome sound
        gkit.tts_play('환영')
        print('Door open')
        return True
    
    # you have tried ur best. good luck on next time
    gkit.tts_play('다음 번에 최선을 다해 행운을 빕니다.')
    return False

def main():
    print(face_detect())

if (__name__ == '__main__'):
    print('Library loaded')

    cred = credentials.Certificate('you-shall-not-pass-c59f3-firebase-adminsdk-kzw1y-e5ebf0cbfc.json')
    app = firebase_admin.initialize_app(cred, {
        'databaseURL' : 'https://you-shall-not-pass-c59f3.firebaseio.com/'
    })

    gkit.get_button().on_press(main)
    input('Press enter to stop\n\n')

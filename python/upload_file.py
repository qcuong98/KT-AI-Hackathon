import firebase_admin
from firebase_admin import credentials, db
import datetime
import urllib
import json
import requests

cred = credentials.Certificate('you-shall-not-pass-c59f3-firebase-adminsdk-kzw1y-e5ebf0cbfc.json')
app = firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://you-shall-not-pass-c59f3.firebaseio.com/'
})

root = db.reference()
new_log = root.child('Logs').push()
log_id = new_log.key

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

token = upload_file("cropped.jpg", log_id)
url = 'https://firebasestorage.googleapis.com/v0/b/you-shall-not-pass-c59f3.appspot.com/o/images%2F' + log_id + '?alt=media&token=' + token

new_log.update({
    'subject': 'Hello C!',
    'timestamp': str(datetime.datetime.now()),
    'message': 'Hello, just kidding, haha!',
    'image': url
})

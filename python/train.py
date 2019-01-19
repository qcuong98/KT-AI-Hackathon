import dlib
import face_recognition as fr
import os
import pickle

mypath = './train/'

encs = []
for dirs in os.listdir(mypath):
    for img_dir in os.listdir(os.path.join(mypath, dirs)):
        img = fr.load_image_file(os.path.join(mypath, dirs, img_dir))
        enc = fr.face_encodings(img)
        print(dirs, ' huhuhu ', img_dir)
        if len(enc) != 1: 
            print(dirs, img_dir)
            continue
        enc = enc[0]
        encs.append((enc, dirs))
with open('train.dat', 'wb') as f:
    pickle.dump(encs, f)

        
        



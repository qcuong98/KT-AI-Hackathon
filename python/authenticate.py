import os
import pickle
import numpy as np
import sys
import face_recognition as fr

train_dir = 'train.dat'

train = pickle.load(open(train_dir, 'rb'))
n = len(train)

def authenticate(path):
    unknown_image = fr.load_image_file(path)
    unknown_encode = fr.face_encodings(unknown_image);

    if not unknown_encode:
        return (0, 'No face detected')

    unknown_encode = unknown_encode[0]

    poll = dict()
    total_vote = 0;

    for enc, name in train:
        dist = np.linalg.norm(unknown_encode - enc)
        if not poll.get(name, False):
            poll[name] = [0,0]
        if dist < 0.45:
            total_vote += 1
            poll[name][0] += 1
        poll[name][1] += 1

    if total_vote < 5:
        return (0, 'Not enough vote')

    #print(poll)

    for name, [vote, total] in poll.items():
        if float(vote)/total > 0.5 and float(vote)/total_vote > 0.8:
            return (1, name)
            
    return (0, 'No consistent candidate')

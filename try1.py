#Leran from pypi.org

import os
import face_recognition as fc
from pathlib import Path

os.chdir(Path(__file__).parent.resolve())

def face_match(known_list,unknown):
    img_encoding=[]
    for img in known_list:
        known_img=fc.load_image_file(img)
        img_encoding.append(fc.face_encodings(known_img)[0])
    unknown_img=fc.load_image_file(unknown)
    unknown_encoding=fc.face_encodings(unknown_img)[0]
    result=fc.compare_faces(img_encoding,unknown_encoding)
    return result

def face_locate(image):
    img=fc.load_image_file(image)
    face_location=fc.face_locations(img)
    return face_location

def face_landmarks(image):
    img=fc.load_image_file(image)
    landmarks_list=fc.face_landmarks(img)
    return landmarks_list

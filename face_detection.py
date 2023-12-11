import face_recognition as fc
import cv2
import pickle
import os
from pathlib import Path
from collections import Counter

def Training():
    # Traning data should be in training folder
    os.chdir(Path(__file__).parent.resolve())
    #opening file
    if not os.path.isfile('training/encodings.pickle'):
        Path('training/encodings.pickle').touch()
    with open(r'training/encodings.pickle','rb') as file:
        if os.path.getsize(r"training/encodings.pickle") == 0:
            print('No training data found, creating training data...')
            name_encoding={'names':[],'encodings':[]}
        else:
            name_encoding=pickle.load(file)
        names=name_encoding['names']
        encodings=name_encoding['encodings']
    #preparation
    for filepath in Path('training').glob('*.jpg'):
        if filepath.name in names:
            print(f'"{filepath.name}" already in training data')
            continue
        names.append(filepath.name)
        print(f'"{filepath.name}" preparing...')
        img=fc.load_image_file(f"training/{filepath.name}")
        face_locations=fc.face_locations(img, model="hog") #hog is faster than cnn  
        face_encoding=fc.face_encodings(img, face_locations, model='hog', num_jitters=1) #this should be either more than 100 or 1
        for encoding in face_encoding:
            encodings.append(encoding)
    #saving
    name_encoding['names']=names
    name_encoding['encodings']=encodings
    with open(r'training/encodings.pickle','wb') as file:
        pickle.dump(name_encoding,file)
    print(f"Training Completed!, \ntraining data : {names}")
    return True

def Detection(_image=None):#_image is list of frame and name
    os.chdir(str(Path(__file__).parent.resolve())+"/validation")
    #opening file
    with open(r'../training/encodings.pickle','rb') as file:
        name_encoding=pickle.load(file)
        encodings=name_encoding['encodings']
    #comparing
    result={}
    print("Detecting ...")
    if not _image:
        _image=list()
        for filepath in Path().glob('*.jpg'):
            print(f'"{filepath.name}" preparing...')
            image_loading=[fc.load_image_file(filepath.name)]
            image_loading.append(filepath.name)
            _image.append(image_loading)
    for image_loading in _image:
        img=image_loading[1]
        image_location=fc.face_locations(image_loading[0], model="hog")
        print("No of faces detected : ",len(image_location))
        if not image_location:
            print(f"No face detected in image '{img}'")
            result[img]=False
            continue
        image_encoding=fc.face_encodings(image_loading[0], image_location, num_jitters=1)
        for bounding, encoding in zip(image_location, image_encoding):
            boolan_match=fc.compare_faces(encodings, encoding ,tolerance=0.49)
            votes=Counter(name for match, name in zip(boolan_match, name_encoding['names']) if match)
            print(f"colelation : {votes}")
            if votes:
                name=votes.most_common(1)[0][0].split('.')[0]
                print(f"The Person in the image ' {img} ' is {name}")
            else:
                name="Gumnaam Insaan"
                print(f"You are {name}")
        result[img]=[name, image_loading[0], bounding]
    return result
import face_recognition as fc
import cv2
import sys
from time import time
from pathlib import Path
import os
import pickle
from collections import Counter
from threading import Thread

class Camera:
    def __init__(self,image=False,video=False,training=False,authentic=False):
        self.image=image
        self.video=video
        self.authentic=authentic
        self.training=training
        navigating_command="Press [esc] to exit "
        if video:
            navigating_command+="| [v] to record video"
        if image:
            navigating_command+="| [space] to capture image"
        self.navigating_command=navigating_command
        cap=cv2.VideoCapture(0)
        if not cap.isOpened():
            sys.exit("\033[31mError: \033[37mCannot open camera")
        cv2.namedWindow(self.navigating_command, cv2.WINDOW_KEEPRATIO)#to close window screen with X button
        cap.set(3,640) #set width
        cap.set(4,480) #set height
        self.cap=cap
    
    def capture(self,_exit=0x1b,_capture=0x20,_record=0x76):

        os.chdir(str(Path(__file__).parent.resolve()))
        def Detection(image_loading):
            image_location=fc.face_locations(image_loading, model="hog")
            if not image_location:
                print("No face found") 
                return []
            print(f"No. of faces detected : {len(image_location)}")
            with open(r'training/encodings.pickle','rb') as file:
                name_encoding=pickle.load(file)
                encodings=name_encoding['encodings']
            image_encoding=fc.face_encodings(image_loading, image_location, num_jitters=1)
            locate_dataset=[]
            for bounding, encoding in zip(image_location, image_encoding):
                boolan_match=fc.compare_faces(encodings, encoding, tolerance=0.48)
                votes=list()
                name_match=""
                for bool, name in zip(boolan_match, name_encoding['names']):
                    name=name.split('.')[0]
                    if bool:
                        votes.append(name)
                        name_match += f" \033[32m{name}\033[37m,"
                    else:
                        name_match += f" \033[31m{name}\033[37m,"
                votes=Counter(votes)
                print(f"Boolian match :[ {name_match}\b ]")
                if votes:
                    name=votes.most_common(1)[0][0]
                    print(f"Hello {name}!")
                    flag=True
                else:
                    name="Lodu"
                    print(name)
                    flag=False
                locate_dataset.append([name, image_loading, bounding, flag])
            return locate_dataset
        # running from here...
        cap=self.cap
        video=self.video
        image=self.image
        Recording=False
        close_cmd: float=1
        while close_cmd >=1:
            ret,frame=cap.read()
            frame=cv2.flip(frame,1)
            if not ret:
                print("can't recieve frame. CLosing....")
                break
            entered_key=cv2.waitKey(1)
            if video and entered_key & 0xff == _record:#press v to record video
                if Recording:
                    out.release()
                    print("saved as 'output.avi'")
                    Recording=False
                else:
                    Path("cVideos").mkdir(exist_ok=True)
                    out = cv2.VideoWriter(f'cVideos/output{time()}.avi', cv2.VideoWriter_fourcc(*'XVID'), 20.0, (640,  480))
                    print("Recording...")
                    Recording=True
            if Recording:
                out.write(frame)
            if image and entered_key & 0xff == _capture:#press space to capture image
                print("Clicked!")
                image_folder="cImages"
                name="image"+time().__str__().split('.')[0]
                if self.training:
                    image_folder="training"
                    name=input("Enter name: ")+"."
                Path(image_folder).mkdir(exist_ok=True)
                cv2.imwrite(f'{image_folder}/{name}.jpg',frame)
                if self.training:
                    from face_detection import Training
                    Training()
                    del Training
            if entered_key & 0xff == _exit: #press 'esc' to quit
                break

            path="training/encodings.pickle"
            if self.authentic and os.path.isfile(path):
                    def Printing(data):
                        name,frame,face,flag = data
                        if(not name=="No face"):
                            if(flag):
                                color=(0,255,0)
                            else:
                                color=(0,0,255)
                            cv2.rectangle(frame,(face[3],face[0]),(face[1],face[2]),color,2)
                            cord=(face[3]+10 , face[2]+20)
                            cv2.putText(frame, name , cord, cv2.FONT_HERSHEY_DUPLEX , 0.75, color, 1, cv2.LINE_AA)
                    dataset = Detection(frame)
                    threads=[]
                    # print(dataset)
                    for data in dataset:
                        threads.append(Thread(target=Printing, args=(data,)))
                    for thread in threads:
                        thread.start()
                    for thread in threads:
                        thread.join()
            close_cmd=cv2.getWindowProperty(self.navigating_command, cv2.WND_PROP_VISIBLE)
            cv2.imshow(self.navigating_command,frame)
                
        cap.release()
        cv2.destroyAllWindows()
import sys
import os

def encoding_data():
    import pickle 
    from pathlib import Path
    os.chdir(Path(__file__).parent.resolve())
    if not os.path.isfile('training/encodings.pickle'):
        return False
    with open(r'training/encodings.pickle','rb') as file:
        if os.path.getsize(r"training/encodings.pickle") == 0:
            return False
        else:
            name_encoding=pickle.load(file)
            return name_encoding

if __name__ == "__main__":
    train: bool=False
    auth: bool=False
    video: bool=False
    cam: bool=False

    argus = sys.argv[1:]+['$']
    argus = iter(argus)
    argu = next(argus)
    err = f"python3 main.py has no attribute '{argu}', try [--help] for more info"
    while argu != '$':
        if argu == "--train" or argu == "-t":
            argu = next(argus)
            if argu == "/data" or argu == "/d":
                print("Loading...")
                encoding = encoding_data()
                if not encoding:
                    print('No training data found')
                else:
                    print(f"Trained data : {encoding['names']}")
            elif argu == "/folder" or argu == "/f":
                from face_detection import Training
                Training()
                del Training
            elif argu[0] == "/":
                err = f"python3 main.py --train has no command '{argu}'"+" \nProper use of this --train is: python3 main.py --train [/d | /f]"
                continue
            else:
                train = True
                continue
        elif argu == "--auth" or argu == "-a":
            argu = next(argus)
            if argu == "/folder" or argu == "/f":
                from face_detection import Detection
                Detection()
                del Detection
            elif argu[0] == "/":
                err = f"python3 main.py --auth has no command '{argu}'"+" \nProper use of this --auth is: python3 main.py --auth [/f]"
                continue
            else:
                auth = True
                continue
        elif argu == "--cam" or argu == "-C":
            cam = True
        elif argu == "--video" or argu == "-V":
            video = True
        elif argu == "--help" or argu == "-h":
            print("""Usage: python3 main.py [option] ... [-t | --train /d /f ] [-a | --auth] [-C | --cam] [-V | --video] \n[-v | --version] [-h | --help]
            Options:
            -t, --train     Train the model
                  /data     Show the trained data
                  /folder   Train the model with images in folder 'training'
            -a, --auth      Authenticate the user
                  /folder   Authenticate the user with images in folder 'validation'
            -C, --cam       Open the camera
            -V, --video     Record the video
            -v, --version   Show the version
            -h, --help      Show this help""")
            quit()
        elif argu == "--version" or argu == "-v":
            print("Version 1.0.0")
            quit()
        else:
            print(f"\033[31mError:\033[37m {err} ")
            quit()
        err = f"python3 main.py has no attribute '{argu}', try [--help] for more info"
        argu = next(argus)

    if cam or auth or train or video:
        print("importing packages...")
        from camera import Camera
        print("switching to camera...")
        Camera(image=cam,video=video,training=train,authentic=auth).capture()
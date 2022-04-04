import os
import datetime
import serial
import pyrebase
from picamera import PiCamera
from time import sleep
from time import strftime

if __name__ == '__main__':
    serConn = serial.Serial('/dev/ttyACM0', baudrate=9600, timeout=5)
    camera = PiCamera()
    firebaseConfig = {
      "apiKey": "AIzaSyDBlb8Lgzl1KWEqq8gmBfdM7myFDsLxiW8",
      "authDomain": "project-tvt20kmo-r2.firebaseapp.com",
      "databaseURL": "gs://project-tvt20kmo-r2.appspot.com",
      "projectId": "project-tvt20kmo-r2",
      "storageBucket": "project-tvt20kmo-r2.appspot.com",
      #messagingSenderId: "327198659484",
      #appId: "1:327198659484:web:f915b50d78216676dbee59",
      #measurementId: "G-RJ7REQEYK1"
      "serviceAccount": "serviceAccountKey.json"
    }
    firebase_storage = pyrebase.initialize_app(firebaseConfig)
    storage = firebase_storage.storage()
    muuttuja = True
    if serConn.isOpen():
        print("{} connected".format(serConn.port))
        while True:
            value = int(serConn.readline()) #Liiketunnistimen arvo muuttujaan
            if value == 1:
                print("liikettä")
                while True:
                    if muuttuja == True:
                        date = datetime.datetime.now().strftime('%d-%m-%Y_%H.%M.%S')
                        print("video alkaa")
                        camera.start_preview()
                        camera.start_recording('/home/pi/Product-Design-And-Implementation/Python/' + date + '.h264')
                        sleep(60)
                        camera.stop_recording()
                        camera.stop_preview()
                        print("video loppuu")
                        muuttuja = False
                        storage.child(date + '.h264').put(date + '.h264')
                        sleep(0.01)
                        if os.path.exists(date + '.h264'):
                            os.remove(date + '.h264')
                            print("Video poistettu.")
                        else:
                          print("The file does not exist")
                    else:
                        print("nyt tulee break")
                        break
            else:
                print("ei liikettä")
                muuttuja = True
    else:
        print("Serial connection is not available.")
    

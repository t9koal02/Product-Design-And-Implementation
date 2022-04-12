import os
import datetime
import serial
import pyrebase
import subprocess
import requests
from picamera import PiCamera
from time import sleep
from time import strftime

if __name__ == '__main__':
    serConn = serial.Serial('/dev/ttyACM0', baudrate=9600, timeout=5)  # Avataan sarjayhteys Arduinolle
    camera = PiCamera()  # Luodaan muuttuja kameralle
    # Yhteyden muodostaminen Firebaseen:
    firebaseConfig = {
      "apiKey": "AIzaSyDBlb8Lgzl1KWEqq8gmBfdM7myFDsLxiW8",
      "authDomain": "project-tvt20kmo-r2.firebaseapp.com",
      "databaseURL": "https://project-tvt20kmo-r2-default-rtdb.firebaseio.com",
      "projectId": "project-tvt20kmo-r2",
      "storageBucket": "project-tvt20kmo-r2.appspot.com",
      #messagingSenderId: "327198659484",
      #appId: "1:327198659484:web:f915b50d78216676dbee59",
      #measurementId: "G-RJ7REQEYK1"
      "serviceAccount": "serviceAccountKey.json"  # Erillinen tiedosto Python -kansiossa
    }
    firebase = pyrebase.initialize_app(firebaseConfig)
    storage = firebase.storage()
    database = firebase.database()
    muuttuja = True  # Apumuuttuja todellisen liikkeen tunnistamiselle
    if serConn.isOpen():
        print("{} connected".format(serConn.port))
        while True:
            value = int(serConn.readline()) # Luetaan liiketunnistimen arvo Arduinolta muuttujaan
            if value == 1:
                print("liikettä")
                while True:
                    if muuttuja == True:
                        # Videon nimeksi tulee päivämäärä ja kellonaika:
                        date = datetime.datetime.now().strftime('%d-%m-%Y_%H.%M.%S') # Haetaan päivä ja aika  
                        filename1 = date + '.h264'  # Tehdään kaksi eri nimi muuttujaa eri muotoisille videoille
                        filename2 = date + '.mp4'
                        print("video alkaa")
                        # Videon kuvaaminen ja tallentaminen oikeaan sijaintiin Raspberryllä:
                        camera.start_preview()
                        camera.start_recording('/home/pi/Product-Design-And-Implementation/Python/' + filename1)  # PiCamera tukee .h264 -formaattia
                        sleep(5)
                        camera.stop_recording()
                        camera.stop_preview()
                        print("video loppuu")

                        # Videon muuntaminen Androidin tukemaan MP4-formaattiin:
                        command = ['MP4Box', '-add', filename1, filename2]
                        subprocess.Popen(command)
                        
                        muuttuja = False
                        sleep(0.55)  # Videon muuntaminen kestää yli 0,5 sekuntia. Jos ei viivästytetä videon siirtäminen Firebaseen ei onnistu
                        
                        storage.child(filename2).put(filename2)  # Video Firebaseen
                        url = storage.child(filename2).get_url(None)  # Haetaan Storagesta videon URL
                    
                        data = {'title':filename2, 'url':url}  # Tallenetaan muuttujaan videon nimi ja url
                        database.child("video").push(data)  # Pusketaan data realtime databaseen
                        sleep(0.01)
                        # Videot (.h264 ja .mp4) poistetaan Raspberryltä:
                        if os.path.exists(date + '.h264') and os.path.exists(date + '.mp4'):
                            os.remove(date + '.h264')
                            os.remove(date + '.mp4')
                            print("Video poistettu.")
                        else:
                          print("The file does not exist")
                    else:
                        print("nyt tulee break")
                        break  # Videon kuvaamiseen riittää 1 kpl true (1) arvoa liiketunnistimelta. Ensimmäisen true arvon jälkeen tulevat ykköset ovat turhia, koska liike on jo havaittu.
            else:
                print("ei liikettä")
                muuttuja = True
    else:
        print("Serial connection is not available.")
    

import datetime
import serial
from picamera import PiCamera
from time import sleep
from time import strftime

if __name__ == '__main__':
    serConn = serial.Serial('/dev/ttyACM0', baudrate=9600, timeout=5)
    camera = PiCamera()
    muuttuja = True
    if serConn.isOpen():
        print("{} connected".format(serConn.port))
        while True:
            value = int(serConn.readline()) #Liiketunnistimen arvo muuttujaan
            #print(type(value2))
            if value == 1:
                print("liikettä")
                while True:
                    if muuttuja == True:
                        date = datetime.datetime.now().strftime('%d-%m-%Y_%H.%M.%S')
                        print("video alkaa")
                        camera.start_preview()
                        camera.start_recording('/home/pi/Desktop/' + date + '.h264')
                        sleep(5)
                        camera.stop_recording()
                        camera.stop_preview()
                        print("video loppuu")
                        muuttuja = False
                    else:
                        print("nyt tulee break")
                        break
            else:
                print("ei liikettä")
                muuttuja = True
    else:
        print("Serial connection is not available.")
    

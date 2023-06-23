
import RPi.GPIO as GPIO
import time

import pickle
import imutils.video
import face_recognition
import cv2

from email.message import EmailMessage
import os
import ssl
import smtplib

import socket


PIR_PIN = 37
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
try:
    GPIO.setup(PIR_PIN, GPIO.IN)
except Exception as e:
    print("Error setting up PIR sensor:", e)

try:
    LED_PIN = 12
    GPIO.setup(LED_PIN, GPIO.OUT)
except Exception as e:
    print("Error setting up LED:", e)

while True:
	
    if not GPIO.input(PIR_PIN):
        time.sleep(5)

    elif GPIO.input(PIR_PIN):
        currentname = "unknown"

        data = pickle.loads(open("encodings.pickle", "rb").read())

        vs = imutils.video.VideoStream(usePiCamera=True).start()
        time.sleep(2)
        
        while True:
            frame = vs.read()
            frame = imutils.resize(frame, width=500)

            names = []

            boxes = face_recognition.face_locations(frame)
            encodings = face_recognition.face_encodings(frame, boxes)
            for encoding in encodings:
                matches = face_recognition.compare_faces(data["known_encodings"], encoding)

                name = "Unknown" 

                if True in matches:
                    matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                    counts = {}

                    for i in matchedIdxs:
                        name = data["names"][i]
                        counts[name] = counts.get(name, 0) + 1
                    name = max(counts, key=counts.get)

                    if currentname != name:
                        currentname = name
                        print(currentname)
                        print(currentname,"is authorized")
                        GPIO.output(12, GPIO.HIGH)

                names.append(name)

                if currentname =="unknown":
                    img_name = "image.jpg"
                    print('Taking a picture...')
                    cv2.imwrite(img_name, frame)
                    vs.stop()
                    time.sleep(2.0)

                    em=EmailMessage()
                    em['From']='s**@gmail.com'
                    em['To']='s**@gmail.com'
                    em['Subject']='unknown visitor'
                    em.set_content("")

                    with open(img_name, 'rb') as image_file:
                        image_data = image_file.read()
                        image_name = os.path.basename(img_name)
                        em.add_attachment(image_data, maintype='image', subtype='jpeg', filename=image_name)

                    context=ssl.create_default_context()
                    with smtplib.SMTP_SSL('smtp.gmail.com',465, context=context) as smtp:
                        smtp.login('s**@gmail.com','*****')
                        smtp.send_message(em)

                    

                    print("Please wait for the administrator to grant you access...")
                    html = """<!DOCTYPE html><html><head>
                        <style>
                        html { font-family: Helvetica; display: inline-block; margin: 0px auto; text-align: center;}
                        .buttonGreen { background-color: #4CAF50; border: 2px solid #000000;; color: white; padding: 15px 32px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; }
                            text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
                        </style>
                    </head><body>
                        <br><br><br><br>
                            <button class="buttonGreen" name="led" value="on" type="submit">LED ON</button>
                        <br><br><br><br>
                    </body></html>"""

                    # Open socket
                    addr = socket.getaddrinfo('0.0.0.0', 4012)[0][-1]
                    s = socket.socket()
                    s.bind(addr)
                    s.listen(1)
                    print('listening on', addr)
                    i =0
                    while True:
                        try:       
                            cl, addr = s.accept()
                            if i == 0:
                                print('Connected from', addr)
                                i=1
                            request = cl.recv(1024)
                            request = str(request)
                            led_on = request.find('led=on')
                            if led_on == 8:
                                GPIO.output(12, GPIO.HIGH)
                                break
                            response = html 
                            cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n'.encode())
                            cl.send(response.encode())
                            cl.close()

                        except OSError as e:
                            cl.close()
                            print('connection closed')
            for ((top, right, bottom, left), name) in zip(boxes, names):
                cv2.rectangle(frame, (left, top), (right, bottom),(0, 255, 225), 2)
                y = top - 15 if top - 15 > 15 else top + 15
                cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, .8, (0, 255, 255), 2)

            cv2.imshow("Facial Recognition is Running", frame)
            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                time.sleep(2.0)
                break
        cv2.destroyAllWindows()
        vs.stop()
            






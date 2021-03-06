# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 14:12:52 2019

@author: Chondro
"""

import imutils
import cv2
from keras.models import load_model
from keras.preprocessing.image import img_to_array
import numpy as np


detection_model_path = 'haarcascade_files/haarcascade_frontalface_default.xml'
emotion_model_path = 'models/model.hdf5'
face_detection = cv2.CascadeClassifier(detection_model_path)
emotion_classifier = load_model(emotion_model_path, compile=False)
EMOTIONS = ["Marah", "Takut", "Senang", "Sedih", "Terkejut", "Netral"]


# starting video
cv2.namedWindow('Pendeteksi Ekspresi')
camera = cv2.VideoCapture(0)
while True:
    frame = camera.read()[1]
    frame = imutils.resize(frame,width=300)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detection.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,
                                            minSize=(30,30),flags=cv2.CASCADE_SCALE_IMAGE)
    canvas = np.zeros((215, 300, 3), dtype="uint8")
    frameClone = frame.copy()
    if len(faces) > 0:
        faces = sorted(faces, reverse=True,
        key=lambda x: (x[2] - x[0]) * (x[3] - x[1]))[0]
        (fX, fY, fW, fH) = faces
        data = gray[fY:fY + fH, fX:fX + fW]
        data = cv2.resize(data, (48, 48))
        data = data.astype("float") / 255.0
        data = img_to_array(data)
        data = np.expand_dims(data, axis=0)
        
        preds = emotion_classifier.predict(data)[0]
        emotion_probability = np.max(preds)
        label = EMOTIONS[preds.argmax()]
    else : continue
 
    for (i, (emotion, prob)) in enumerate(zip(EMOTIONS, preds)):
                text = "{}: {:.2f}%".format(emotion, prob * 100)
                
                cv2.putText(frameClone, label, (fX, fY - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (250, 0, 0), 2)
                cv2.rectangle(frameClone, (fX, fY), (fX + fW, fY + fH),
                              (250, 0, 0), 2)
                
                w = int(prob * 300)
                cv2.rectangle(canvas, (1, (i * 35) + 5),
                (w, (i * 35) + 35), (250, 0, 0), -1)
                cv2.putText(canvas, text, (10, (i * 35) + 23),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45,
                (255, 255, 255), 2)

    cv2.imshow('Pendeteksi Ekspresi', frameClone)
    cv2.imshow("RESULT", canvas)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
camera.release()
cv2.destroyAllWindows()

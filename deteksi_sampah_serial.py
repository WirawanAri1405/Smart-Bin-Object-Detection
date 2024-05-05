import cv2
import torch
import pathlib
import serial
import numpy as np
import os
import time

#save image in folder
def file_save(img , type ,path):
    timestamp = int(time.time())
    filename = f"{type}_{timestamp}.jpg"
    file_path = os.path.join(path, filename)
    cv2.imwrite(file_path, img)
    print(f"Image saved as {filename} in the folder successfully!")

# fixing path
temp = pathlib.PosixPath 
pathlib.PosixPath = pathlib.WindowsPath
from pathlib import Path

ser = serial.Serial('COM3',baudrate = 9600)
path='HASIL TRAINING/weights/125epoch.pt'
model = torch.hub.load(R'D:\YOLO_V5\yolov5','custom',path, source='local',force_reload=True)
while 1:
    arduino = ser.readline().decode('UTF-8').strip()
    if arduino == '1':
        print(arduino)
        # camera initialization
        # 0 = laptop camera
        # 1 = external webcam
        #http://192.168.112.18:81/stream = livestreaming url
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("failed to open the camera")
            exit()

        ret, frame = cap.read()

        if not ret:
            print("failed to read the frame from the camera")
            exit()
        imgs=frame
        cap.release()       
        results = model(imgs)
        results.show()
        detected = False
        for pred in results.xyxy[0]:
            # Get class label and confidence score
                conf, cls = pred[-2:]
                label = f"{model.names[int(cls)]}"
                detected = True
                if label == "HDPE":
                    ser.write(b'2')
                    print("sampah dengan jenis HDPE")
                    file_save(imgs,"HDPE",R"HASIL DETEKSI SAMPAH\HDPE")
                    break
                elif label == "LDPE" :
                    ser.write(b'3')
                    print("sampah dengan jenis LDPE")
                    file_save(imgs,"LDPE",R"HASIL DETEKSI SAMPAH\LDPE")
                    break
                elif label == "PET" :
                    ser.write(b'4')
                    print("sampah dengan jenis PET")
                    file_save(imgs,"PET",R"HASIL DETEKSI SAMPAH\PET")
                    break
                elif label == "PP" :
                    ser.write(b'5')
                    print("sampah dengan jenis PP")
                    file_save(imgs,"PP",R"HASIL DETEKSI SAMPAH\PP")
                    break
                elif label == "PS" :
                    ser.write(b'6')
                    print("sampah dengan jenis PS")
                    file_save(imgs,"PS",R"HASIL DETEKSI SAMPAH\PS")
                    break
                elif label == "PVC" :
                    ser.write(b'7')
                    print("sampah dengan jenis PVC")
                    file_save(imgs,"PVC",R"HASIL DETEKSI SAMPAH\PVC")
                    break
                break
        if not detected:
            ser.write(b'8')
            print("jenis sampah plastik tidak terdeteksi")   
            file_save(imgs,"NULL",R"HASIL DETEKSI SAMPAH\NULL")




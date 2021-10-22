import cv2
import mediapipe as mp # foto.JPG
from math import *
import threading
import serial
import time
import math
import numpy as np

dev = serial.Serial("COM3", 9600, writeTimeout = 0)

def x_axis():
 global angle_x
 global angle_y
   
 if angle_x != x1 or angle_y != y1:
   angle_x = x1
   angle_y = y1
   coord = [angle_x,angle_y]
   
   coord_c = str(coord) 
   coord_c = coord_c.replace('[','')
   coord_c = coord_c.replace(']','')
   coord_c = coord_c.replace(' ','')
   print(coord_c)
   com = str(coord_c) + "\n"
   dev.write(com.encode("ascii"))

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands    

angle_x = 0
angle_y = 0
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

with mp_hands.Hands(
 static_image_mode=False,
 max_num_hands=1,
 min_detection_confidence=0.5) as hands:
 
 while True:
  _, image = cap.read()
  
  height, width, _ = image.shape
 
  image = cv2.flip(image, 1)
  image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
 
  results = hands.process(image_rgb)
  already_flppd = False
  
  if results.multi_hand_landmarks is not None:
   for hand_landmarks in results.multi_hand_landmarks:
    #mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS,
    #mp_drawing.DrawingSpec(color=(0,0,255),thickness=-1, circle_radius=10),
    #mp_drawing.DrawingSpec(color=(0,40,255),thickness=4,))
   
    x1 = int(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x * width)
    y1 = int(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y * height)   
   
    x2 = int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x * width)
    y2 = int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y * height)
    
    x3 = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * width)
    y3 = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * height)

    x4 = int(hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x * width)
    y4 = int(hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y * height)

    length_i = trunc(math.hypot(x3-x2, y3-y2))
    length_p = trunc(math.hypot(x4-x2, y4-y2))
    
    aux_img = np.zeros(image.shape, np.vint8)
    contours = np.array([[x3,y3],[x2,y2],[x4,y4]])   
   
    cv2.fillPoly(overlay, pts=[contours], color=[129,0,250])   
    output = cv2.addWeighted(image, 1, aux_img, 0.8, 3)
    
    cv2.circle(image, (x1,y1), 2,(0, 0,255), 20)
    cv2.line(image, (x1, y1), (x2, y2), (255, 255, 255), thickness=3)
    cv2.line(image, (x2, y2), (x3, y3), (255, 255, 255), thickness=3)
    cv2.line(image, (x4, y4), (x2, y2), (255, 255, 255), thickness=3)
    
    if length_i <= 200 and length_p <= 200:
       cv2.putText(image, "Detected", (10,450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2) 
       x1 = 335
       y1 = 455
     
    threading.Thread(target = x_axis).start()
    
    cv2.imshow("image", output)
    
    #line_l = ceil(sqrt(pow(x2-x1, 2)+pow(y2-y1, 2)))
    #cv2.putText(image, "Envindo", (x1+20,y1+20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    #cv2.putText(image, "Envindo", (x1+40,y1+20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    
    #cv2.line(image, (x1,y1),(x2,y2), (255,0,255), 2)
    
  # image = cv2.flip(image, 1)
  #if already_flppd == True:   
   
   
 
  cv2.imshow("image", image) 
  if cv2.waitKey(20) & 0xFF==ord('d'):
     break
    
cap.release()
cv2.destroyAllWindows()  

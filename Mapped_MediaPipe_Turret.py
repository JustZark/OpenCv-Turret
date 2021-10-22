import cv2
import mediapipe as mp # foto.JPG
from math import *
import threading
import serial
import time
import math
import numpy as np
import colorama
import os
from colorama import Fore, Back, Style

colorama.init()
os.system("cls")
dev = serial.Serial("COM3", 9600, writeTimeout = 0)

print(f"""{Fore.GREEN}{Style.BRIGHT}
████████╗ ██████╗  ██████╗    ███████╗██╗   ██╗███████╗████████╗███████╗███╗   ███╗
╚══██╔══╝██╔═══██╗██╔════╝    ██╔════╝╚██╗ ██╔╝██╔════╝╚══██╔══╝██╔════╝████╗ ████║
   ██║   ██║   ██║██║         ███████╗ ╚████╔╝ ███████╗   ██║   █████╗  ██╔████╔██║
   ██║   ██║   ██║██║         ╚════██║  ╚██╔╝  ╚════██║   ██║   ██╔══╝  ██║╚██╔╝██║
   ██║   ╚██████╔╝╚██████╗    ███████║   ██║   ███████║   ██║   ███████╗██║ ╚═╝ ██║
   ╚═╝    ╚═════╝  ╚═════╝    ╚══════╝   ╚═╝   ╚══════╝   ╚═╝   ╚══════╝╚═╝     ╚═╝
{Style.RESET_ALL}""")

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
   print("Coordenadas pixeles (x,y): ", coord_c, end="\r")
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
  _, image_hand_rig = cap.read()
  

  height, width, _ = image.shape
 
  image = cv2.flip(image, 1)
  image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
  
  results = hands.process(image_rgb)
  already_flppd = False
  
  if results.multi_hand_landmarks is not None:
   for hand_landmarks in results.multi_hand_landmarks:
    #mp_drawing.draw_landmarks(aux_image, hand_landmarks, mp_hands.HAND_CONNECTIONS,
    #mp_drawing.DrawingSpec(color=(0,0,255),thickness=-1, circle_radius=10),
    #mp_drawing.DrawingSpec(color=(0,40,255),thickness=4,))
   
    x1 = int(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x * width)
    y1 = int(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y * height)   
   
    cv2.circle(image, (x1,y1), 2,(0, 0,255), 10)
    cv2.line(image, (x1, 0), (x1, 480), (0, 0, 255), thickness=1)
    cv2.line(image, (0, y1), (900, y1), (0, 0, 255), thickness=1)
     
    threading.Thread(target = x_axis).start()
    
  cv2.imshow("image", image) 

  if cv2.waitKey(20) & 0xFF==ord('d'):
     break
    
cap.release()
cv2.destroyAllWindows()  

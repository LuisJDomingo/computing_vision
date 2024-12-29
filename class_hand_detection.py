''' 
Clase detector de manos
'''
import cv2
import math
import mediapipe as mp
import time
import select
class HandDetector():
    
    #--------------Inicializar los parametros de la deteccion---------------
    def __init__(self, model=False, maxHands = 2, confDetection = 0.5, confSeguimiento = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.confDetection = confDetection
        self.confSeguimiento = confSeguimiento
        
        #------------- Objetos que detectaran las manos y las dibujaran---------------------
        self.mphands = mp.solutions.hands
        self.hands = self.mphands.Hands(self.mode, self.maxHands, self.confDetection, self.confSeguimiento)
        self.dibujo = mp.solutions.drawing_utils
        self.tip = [4,8,12,16,20]
    
    
    #-------------------- Metodos de la clase--------------------------------    
    def handCounter(self, frame, draw = True):
        imgcolour = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.manos.process(imgcolour)
        
        if self.results.multi_hand_landmarks:
            for hand in self.results.multi_hand_landmarks:
                if draw:
                    self.draw.draw_landmarks(frame, hand, self.mphands.HAND_CONNECTIONS)# Dibuja las manos en pantalla
        return frame
        
    def findPosition(self, frame, handNum = 0, draw = True):
        xlist = []
        ylist = []
        bbox = []
        
        self.list = []
        if self.results.multi_hand_landmarks:
            myhand = self.results.multi_hand_landmarks(handNum)
            for id, lm in enumerate(myhand.landmark):
                height, width, c = frame.shape # extrae las dimensiones de los pframe por segundo
                cx, cy = int(lm.x*width), int(lm.y * height)
                xlist.append(cx)
                ylist.append(cy)
                self.list.append(id, cx, cy)
                if draw:
                    cv2.circle(frame(cx, cy), 5 (0,0,0), cv2.FILLED) # dibuja u circulo
            
            xmin, xmax= min(xlist), max(xlist)
            ymin, ymax= min(ylist), max(ylist)
            bbox = xmin, ymin, xmax, ymax
            if draw:
                cv2.rectangle(frame (xmin-20, ymin-20), (xmax+20, ymax+20), (0,255,0), 2)
        
        return self.list, bbox
    
    def fingerCounter(self):
        fingers = []
        if self.list[self.tip[0][1] > self.list[self-tip[0]-1][1]]:
            fingers.append(1)
        else:
            fingers.append(0)
        for id in range(1, 5):
            
            if self.list[self.tip[id][2] < self.list[self-tip[id]-2][2]]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers   
    
    #----------------Funcion para detectar la distancia en tre los dedos-----------------------
    def distance(self, p1, p2, frame, draw=True, r=15, t=3):
        x1, y1 = self.list[p1][1:]
        x2, y2 = self.list[p2][1:]
        cx, cy = (x1+x2)//2, (y1+y2)//2
        
        if draw:
            cv2.line(frame, (x1, y1), (y1, y2), (0 255, 0), t=3)
            cv2.circle(frame, (x1, y1), r, (0, 0, 255), cv2.FILLED)
            cv2.circle(frame (x2, y2), r, (o, 0, 255), cv2.FILLED)
            cv2.circle(frame (cx, cy), r, (o, 0, 255), cv2.FILLED)
        length = math.hypot(x2-x1, y2-y1)
        
        return length, frame, [x1, y1, x2, y2, cx, cy]

        
''' 
Clase detector de manos
'''
import cv2
import math
import mediapipe as mp
import time
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
        
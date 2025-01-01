
# Clase detector de manos

import cv2
import math
import mediapipe as mp

class HandDetector():
    
    #--------------Inicializar los parametros de la deteccion---------------
    def __init__(self, mode=False, maxHands=2, confDetection=0.5, confSeguimiento=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.confDetection = confDetection
        self.confSeguimiento = confSeguimiento
        
        #------------- Objetos que detectaran las manos y las dibujaran---------------------
        self.mphands = mp.solutions.hands
        self.hands = self.mphands.Hands(
            static_image_mode=self.mode,  # True o False (indica si es imagen estática o dinámica)
            max_num_hands=self.maxHands,  # Número máximo de manos a detectar
            min_detection_confidence=self.confDetection,  # Confianza mínima para detección de mano
            min_tracking_confidence=self.confSeguimiento  # Confianza mínima para el seguimiento de la mano
        )        
        self.dibujo = mp.solutions.drawing_utils
        self.tip = [4,8,12,16,20]
    
    
    #-------------------- Metodos de la clase--------------------------------    
    def handCounter(self, frame, dibujo= True):
        imgcolour = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgcolour)
        
        if self.results.multi_hand_landmarks:
            for hand in self.results.multi_hand_landmarks:
                if dibujo:
                    # Dibuja las manos en pantalla
                    self.dibujo.draw_landmarks(frame, 
                                               hand, 
                                               self.mphands.HAND_CONNECTIONS)
                    # Dibuja las manos en pantalla
        return frame
        
    def findPosition(self, frame, handNum = 0, dibujo = True):
        xlist = []
        ylist = []
        bbox = []
        
        self.list = []
        if self.results.multi_hand_landmarks:
            myhand = self.results.multi_hand_landmarks[handNum]
            for id, lm in enumerate(myhand.landmark):
                height, width, c = frame.shape # extrae las dimensiones de los pframe por segundo
                cx, cy = int(lm.x*width), int(lm.y * height)
                xlist.append(cx)
                ylist.append(cy)
                self.list.append((id, cx, cy))
                if dibujo:
                    cv2.circle(frame, (cx, cy), 5, (0,0,0), cv2.FILLED) # dibuja u circulo
            
            xmin, xmax= min(xlist), max(xlist)
            ymin, ymax= min(ylist), max(ylist)
            bbox = xmin, ymin, xmax, ymax
            if dibujo:
                cv2.rectangle(frame, (xmin-20, ymin-20), (xmax+20, ymax+20), (0,255,0), 2)
        
        return self.list, bbox
    
    def fingerCounter(self, frame):
        fingers = []
        # Verifica si hay puntos detectados
        if not self.list:
            return []
        print(self.list)
         # Identifica si la mano es izquierda o derecha usando el punto de la muñeca (landmark 0)
        wrist = self.list[0]  # Coordenada de la muñeca (landmark 0)
        is_left_hand = wrist[1] < frame.shape[1] // 2  # Si la muñeca está en la mitad izquierda de la imagen, es la mano izquierda

        # Verificación del pulgar (dedo 0)
        if is_left_hand:
            # Para la mano izquierda, comparamos los puntos 4 (punta) y 3 (base) del pulgar
            if self.list[self.tip[0]][2] > self.list[self.tip[0] - 1][2]:
                fingers.append(1)  # Pulgar levantado
            else:
                fingers.append(0)  # Pulgar cerrado
        else:
            # Para la mano derecha, comparamos los puntos 4 (punta) y 3 (base) del pulgar
            if self.list[self.tip[0]][2] < self.list[self.tip[0] - 1][2]:
                fingers.append(1)  # Pulgar levantado
            else:
                fingers.append(0)  # Pulgar cerrado

        # Verificación de los otros dedos (dedos 1 a 4)
        for id in range(1, 5):
            if self.list[self.tip[id]][2] < self.list[self.tip[id] - 2][2]:  # La punta del dedo debe estar por encima de la segunda falange
                fingers.append(1)  # Dedo levantado
            else:
                fingers.append(0)  # Dedo cerrado

        print(fingers)
        return fingers  
    
    #----------------Funcion para detectar la distancia entre los dedos------------------
    #----------------Esta funcion tiene aplicaciones como subir y bajar el volumen--------------
    
    def distance(self, p1, p2, frame, dibujo=True, r=15, t=3):
        x1, y1 = self.list[p1][1:]
        x2, y2 = self.list[p2][1:]
        cx, cy = (x1+x2)//2, (y1+y2)//2
        
        if dibujo:
            cv2.line(frame, (x1, y1), (y1, y2), (0, 255, 0), t=3)
            cv2.circle(frame, (x1, y1), r, (0, 0, 255), cv2.FILLED)
            cv2.circle(frame (x2, y2), r, (0, 0, 255), cv2.FILLED)
            cv2.circle(frame (cx, cy), r, (0, 0, 255), cv2.FILLED)
        length = math.hypot(x2-x1, y2-y1)
        
        return length, frame, [x1, y1, x2, y2, cx, cy]

    
    

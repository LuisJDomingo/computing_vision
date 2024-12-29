''' 
Clase detector de manos
'''
class HandDetector():
    
    #--------------Inicializar los parametros de la deteccion---------------
    def __init__(self, model=False, maxHands = 2, confDetection = 0.5, confSeguimiento = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.confDetection = confDetection
        self.confSeguimiento = confSeguimiento
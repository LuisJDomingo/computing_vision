from class_hand_detection import HandDetector
import cv2
import time

def main():
    p_time = 0
    c_time = 0
    #--------------------------leemos la webcam------------------------------------------------------
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: No se pudo abrir la cámara.")
        return
    #----------------------------creamos el objeto con la clase----------------------------------------
    detector = HandDetector()
    
    #--------------------------deteccion de las manos---------------------------------------------
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error al capturar el cuadro de la cámara")
            continue
        # Invertir la imagen horizontalmente
        frame = cv2.flip(frame, 1)
        
        frame = detector.handCounter(frame, dibujo=True) 
        list, bbox = detector.findPosition(frame)
        
        if list:  # Verifica si hay datos válidos
            fingers = detector.fingerCounter(frame)  # Llama a la función para contar dedos
            print(f"Dedos levantados: {fingers}")
            cv2.putText(frame, f'Dedos levantados: {sum(fingers)}', (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        c_time = time.time()
        fps = 1/(c_time-p_time)
        p_time = c_time
        
        #cv2.putText(frame, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 255), 3)
        #cv2.putText(frame, f'Dedos levantados: {sum(fingers)}', (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        cv2.imshow("Manos", frame)
        k = cv2.waitKey(1)
        
        if k == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
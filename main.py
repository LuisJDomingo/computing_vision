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
            break
        # Invertir la imagen horizontalmente
        frame = cv2.flip(frame, 1)
        
        # Agregar texto con instrucciones en la parte superior derecha
        instructions = "Presiona 'q' para salir"
        text_size = cv2.getTextSize(instructions, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
        text_x = frame.shape[1] - text_size[0] - 10  # Posicionar 10 px del borde derecho
        text_y = 30  # Altura fija
        cv2.putText(frame, instructions, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        # Procesamiento con el detector
        frame = detector.handCounter(frame, dibujo=True) 
        list, bbox = detector.findPosition(frame)
        
        if list:  # Verifica si hay datos válidos
            fingers = detector.fingerCounter(frame)  # Llama a la función para contar dedos
            print(f"Dedos levantados: {fingers}")
            cv2.putText(frame, f'Dedos levantados: {sum(fingers)}', (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        # Calcular FPS
        c_time = time.time()
        fps = 1 / (c_time - p_time)
        p_time = c_time
        
        # Mostrar el frame y el FPS
        # cv2.putText(frame, f'FPS: {int(fps)}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Manos", frame)

        # Detectar si se presiona 'q' o se cierra la ventana
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if cv2.getWindowProperty("Manos", cv2.WND_PROP_VISIBLE) < 1:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

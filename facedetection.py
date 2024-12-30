import cv2
import os

# Crear carpeta para almacenar las caras si no existe
output_folder = "faces"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
    
# Cargar el clasificador en cascada de OpenCV para detección de caras
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Captura de video
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Error al capturar el cuadro de la cámara")
        continue
    # Invertir la imagen horizontalmente
    frame = cv2.flip(frame, 1)
    # Convertir a escala de grises para la detección facial
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detectar caras en la imagen
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Dibujar rectángulos alrededor de las caras detectadas
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.putText(frame, "Cara detectada", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
    
    # Agregar texto con instrucciones en la parte superior derecha
    instructions = "Presiona 'q' para salir"
    text_size = cv2.getTextSize(instructions, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
    text_x = frame.shape[1] - text_size[0] - 10  # Posicionar 10 px del borde derecho
    text_y = 30  # Altura fija
    cv2.putText(frame, instructions, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
    # Mostrar el video con las caras detectadas
    cv2.imshow("Detección de Cara", frame)

    # Salir del loop si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    # Detectar si la ventana ha sido cerrada
    if cv2.getWindowProperty("Detección de Cara", cv2.WND_PROP_VISIBLE) < 1:
        break
cap.release()
cv2.destroyAllWindows()

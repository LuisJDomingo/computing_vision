import cv2
import os
import face_recognition

# Crear carpeta para almacenar las caras si no existe
output_folder = "faces"
# Crear carpeta para las imágenes con puntos de referencia si no existe
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
    print(f"Carpeta '{output_folder}' creada.")
else:
    print(f"Carpeta '{output_folder}' ya existe.")

# Cargar el clasificador en cascada de OpenCV para detección de caras
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Captura de video
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)  # Establece el ancho de la imagen
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)  # Establece la altura de la imagen

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Error al capturar el cuadro de la cámara")
        continue
    
    # Invertir la imagen horizontalmente
    frame = cv2.flip(frame, 1)
    
    face_loc = face_recognition.face_locations(frame) # esto devuelve la localizacion de la cara dentro la imagen
    face_image_encodings = face_recognition.face_encodings(frame, known_face_locations=[face_loc]) # retorna un vector con los puntos caracterisiticos del rostro
    
    # Dibujar rectángulos alrededor de las caras detectadas y guardar la instantánea
    for i, (x, y, w, h) in enumerate(face_loc):
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.putText(frame, "Cara detectada", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
        
        # Recortar la cara detectada
        face_roi = frame[y:y+h, x:x+w]
        
        # Guardar la imagen de la cara
        filename = os.path.join(output_folder, f"face_{i}.jpg")
        cv2.imwrite(filename, face_roi)
        # print(f"Cara guardada en: {filename}")
    
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

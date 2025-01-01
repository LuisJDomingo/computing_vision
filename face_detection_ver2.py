import cv2
import face_recognition
import os
import imutils
from utils import jsonify, upToMongo

output_folder = "computing_vision\\faces"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)
    print(f"Carpeta '{output_folder}' creada.")
else:
    print(f"Carpeta '{output_folder}' ya existe.")

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
face_frame_encodings = None  # Variable para almacenar los puntos de interés de la cara

while True:
    ret, frame = cap.read()
    if not ret: break
    frame = cv2.flip(frame, 1)
    
    # mostrar instrucciones por pantalla
    
    instructions = "Presiona 'q' para salir"
    text_size, _ = cv2.getTextSize(instructions, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
    text_width = text_size[0]  # Extraer el ancho del texto
    text_x = frame.shape[1] - text_width - 10  # Posicionar 10 px del borde derecho
    text_y = 30  # Altura fija
    cv2.putText(frame, instructions, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (125, 228, 0), 1)
    
    cv2.imshow("frame", frame) # mostrar el frame por pantalla
    
    # salir del loop se presiona q
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        # Tomar foto al presionar 'q'
        photo_filename = os.path.join(output_folder, "captured_face.jpg")
        cv2.imwrite(photo_filename, frame)
        print(f"Foto tomada y guardada en: {photo_filename}")

        # Extraer los puntos de interés de la cara
        face_locations = face_recognition.face_locations(frame)
        if face_locations:
            face_frame_encodings = face_recognition.face_encodings(frame, known_face_locations=face_locations)
            print(f"Puntos de interés extraídos: {face_frame_encodings}")
        else:
            print("No se detectaron caras en la foto.")
        break
    
    # Detectar si la ventana ha sido cerrada
    if cv2.getWindowProperty("frame", cv2.WND_PROP_VISIBLE) < 1:
        print("Ventana cerrada por el usuario.")
        break
    
cap.release()
cv2.destroyAllWindows()

# Almacenar los encodings en formato JSON si se extrajeron puntos de interés
if face_frame_encodings:    
    output_json = jsonify(face_frame_encodings, "captured_face.jpg")
    print(f"Encodings almacenados: {output_json}")
else:
    print("No se almacenaron encodings debido a que no se detectaron caras.")
    

# Eliminar imagen tomada   
file_path = r"computing_vision\faces\captured_face.jpg"

try:
    # Verifica si el archivo existe
    if os.path.exists(file_path):
        os.remove(file_path)  # Elimina el archivo
        print(f"Archivo '{file_path}' eliminado exitosamente.")
    else:
        print(f"El archivo '{file_path}' no existe.")
except Exception as e:
    print(f"Ocurrió un error al intentar eliminar el archivo: {e}")
    
# subir el archivo jason a la base de datos
 
file_path = r"computing_vision\faces\output.json"

try:
    # Verifica si el archivo existe
    if os.path.exists(file_path):
        upToMongo(file_path)
        print(f"Archivo '{file_path}' insertado exitosamente.")
    else:
        print(f"El archivo '{file_path}' no existe.")
except Exception as e:
    print(f"Ocurrió un error al intentar eliminar el archivo: {e}")


    '''
    face_locations = face_recognition.face_locations(frame)
    print("-------------------------face_locations--------------------------\n\n", face_locations)
    if face_locations != []:  # Verifica si hay caras detectadas
        for face_location in face_locations:
            face_frame_encodings = face_recognition.face_encodings(frame, known_face_locations=[face_location])[0]
            print(face_frame_encodings)
            top, right, bottom, left = face_location  # Extrae las coordenadas
                            
            # Dibujar un rectángulo alrededor de la cara
            cv2.rectangle(frame, (left, top), (right, bottom), (125, 228, 0), 2)

            # Dibujar un fondo para el texto justo pegado al borde inferior del rectángulo de la cara
            cv2.rectangle(frame, (left, bottom), (right, bottom + 30), (125, 228, 0), -1)

            # Colocar el texto dentro del fondo
            cv2.putText(frame, "Cara detectada", (left + 5, bottom + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

            # Recortar la cara detectada
            face_roi = frame[top:bottom, left:right]  # Recortar usando las coordenadas correctas

            # Crear un nombre de archivo único para cada cara
            filename = os.path.join(output_folder, f"face.jpg")

            # Guardar la imagen de la cara
            cv2.imwrite(filename, face_roi)
            print(f"Cara guardada en: {filename}")
            
    # output_json = jsonify(face_frame_encodings, "face.jpg")
            
    instructions = "Presiona 'q' para salir"
    text_size, _ = cv2.getTextSize(instructions, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
    text_width = text_size[0]  # Extraer el ancho del texto
    text_x = frame.shape[1] - text_width - 10  # Posicionar 10 px del borde derecho
    text_y = 30  # Altura fija
    cv2.putText(frame, instructions, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (125, 228, 0), 1)

    # conseguir los puntos de refencia de la imagen guardada
    
    img_file = os.path.join(output_folder, "face.jpg")
    with open (img_file, 'r') as img:
        face_locations = face_recognition.face_locations(img)
        face_frame_encodings = face_recognition.face_encodings(frame, known_face_locations=[face_location])[0]
        
    output_json = jsonify(face_frame_encodings, "face.jpg")
    
    cv2.imshow("frame", frame)
    # Salir del loop si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    # Detectar si la ventana ha sido cerrada
    if cv2.getWindowProperty("frame", cv2.WND_PROP_VISIBLE) < 1:
        break    
cap.release()
cv2.destroyAllWindows()
'''

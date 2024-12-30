import cv2
import face_recognition
import os
import imutils

'''coge las imagenes de la carpeta faces
    las examina una por una.
    dentro de un bucle for in
'''
print("--------------------------")
img = cv2.imread("faces/face_0.jpg")
if img is None:
    print(f"Error al cargar la imagen: {img}")
face_loc = face_recognition.face_locations(img)[0]
print("face_loc: ", face_loc)

face_image_encodings = face_recognition.face_encodings(img, known_face_locations=[face_loc])[0]
print("face_image_encodins: ", face_image_encodings)

#cv2.imshow("imagen", img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

############# Reconocimiento facial mediante video streaming

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    ret, frame = cap.read()
    if not ret: break
    frame = cv2.flip(frame, 1)
    
    face_locations = face_recognition.face_locations(frame)
    print("-------------------------face_locations--------------------------\n\n", face_locations)
    if face_locations != []:  # Verifica si hay caras detectadas
        for face_location in face_locations:
            face_frame_encodings = face_recognition.face_encodings(frame, known_face_locations=[face_location])[0]
            result = face_recognition.compare_faces([face_frame_encodings], face_image_encodings)
            print("result: ", result)
            top, right, bottom, left = face_location  # Extrae las coordenadas
            if result[0] == True:
                text = "conocido"
                color = (125,228,0)
            else:
                text = "desconocido"
                color = (50, 50, 255)
                
            cv2.rectangle(frame, (bottom, right, top, right), color, -1)
            cv2.rectangle(frame, (left, top, right, bottom), color, 2)
            cv2.putText(frame, text, (bottom, right+20 ), 2, 0.7, (255, 255, 255), 1 )
    
    cv2.imshow("frame", frame)
    # Salir del loop si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    # Detectar si la ventana ha sido cerrada
    if cv2.getWindowProperty("frame", cv2.WND_PROP_VISIBLE) < 1:
        break    

cap.release()
cv2.destroyAllWindows()
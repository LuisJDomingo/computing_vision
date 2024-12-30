import cv2
import face_recognition
import os
import imutils

'''coge las imagenes de la carpeta faces
    las examina una por una.
    dentro de un bucle for in
'''
print("--------------------------")
img = cv2.imread(r"computing_vision\faces\face_0.jpg")
if img is None:
    print(f"Error al cargar la imagen: {img}")
face_loc = face_recognition.face_locations(img)
print("face_loc: ", face_loc)
face_image_encodings = face_recognition.face_encodings(img, known_face_locations=[face_loc])
cv2.imshow("imagen", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
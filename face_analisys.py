import cv2
import dlib
import os
import imutils
import time

# Ruta de la carpeta donde están las imágenes
input_folder = "faces"
output_folder = "landmarks_output"

# Crear carpeta para las imágenes con puntos de referencia si no existe
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
    print(f"Carpeta '{output_folder}' creada.")
else:
    print(f"Carpeta '{output_folder}' ya existe.")

# Cargar el detector de caras de dlib y el predictor de puntos de referencia
detector = dlib.get_frontal_face_detector()
predictor_path = "shape_predictor_68_face_landmarks.dat"
print(predictor_path)
# Asegúrate de que la ruta sea correcta
try:
    predictor = dlib.shape_predictor(predictor_path)
except RuntimeError as e:
    print(f"Error al abrir el archivo: {e}")
print("------------------------------------------")
# Procesar cada imagen de la carpeta
print("comienzo de proceso de las imagenes")
for image_name in os.listdir(input_folder):
    image_path = os.path.join(input_folder, image_name)
    if not image_name.lower().endswith(('.png', '.jpg', '.jpeg')):
        continue

    # Leer la imagen
    print("\tleyenfo imagen desde archivo")
    image = cv2.imread(image_path)
    
    cv2.imshow("imagen 1:", image)
    time.sleep(10)
    
    if image is None:
        print(f"No se pudo cargar la imagen: {image_name}")
        continue
    
    print("----------------------------------")

    # Convertir a escala de grises
    print("\tConvertir a escala de grises")
    frame = imutils.resize(image, width=720)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    cv2.imshow("imagen 2", gray)
    time.sleep(5)
    print("----------------------------------")
    
    # Detectar caras
    print("detectando caras")
    faces = detector(gray, 1)
    print(faces)
    if len(faces) == 0:
        print(f"No se detectaron caras en la imagen: {image_name}")
    print("----------------------------------")
    
    # Procesar cada cara detectada
    print("procesando caras")
    for i, face in enumerate(faces):
        # Obtener los puntos de referencia
        landmarks = predictor(gray, face)
        print("dibujar puntos de referencia")
        # Dibujar los puntos de referencia en la imagen
        for n in range(68):  # Dlib predice 68 puntos de referencia
            x = landmarks.part(n).x
            y = landmarks.part(n).y
            cv2.circle(image, (x, y), 2, (0, 255, 0), -1)
            print("estos son los puntod de de referencia x: {},\n y estos los de y: {}".format( x, y))
        # Guardar la imagen con los puntos de referencia
        output_path = os.path.join(output_folder, f"{os.path.splitext(image_name)[0]}_landmarks.jpg")
        cv2.imwrite(output_path, image)
        print(f"Procesada y guardada con landmarks: {output_path}")
        
        print("---------------------------------------------------")

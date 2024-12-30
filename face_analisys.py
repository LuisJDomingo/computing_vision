import cv2
import dlib
import os

# Ruta de la carpeta donde están las imágenes
input_folder = "faces"
output_folder = "landmarks_output"

# Crear carpeta para las imágenes con puntos de referencia si no existe
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Cargar el detector de caras de dlib y el predictor de puntos de referencia
detector = dlib.get_frontal_face_detector()
predictor_path = "shape_predictor_68_face_landmarks.dat"
predictor = dlib.shape_predictor(predictor_path)

# Procesar cada imagen de la carpeta
for image_name in os.listdir(input_folder):
    image_path = os.path.join(input_folder, image_name)
    if not image_name.lower().endswith(('.png', '.jpg', '.jpeg')):
        continue

    # Leer la imagen
    image = cv2.imread(image_path)
    if image is None:
        print(f"No se pudo cargar la imagen: {image_name}")
        continue

    # Convertir a escala de grises
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detectar caras
    faces = detector(gray)
    if len(faces) == 0:
        print(f"No se detectaron caras en la imagen: {image_name}")
        continue

    # Procesar cada cara detectada
    for i, face in enumerate(faces):
        # Obtener los puntos de referencia
        landmarks = predictor(gray, face)

        # Dibujar los puntos de referencia en la imagen
        for n in range(68):  # Dlib predice 68 puntos de referencia
            x = landmarks.part(n).x
            y = landmarks.part(n).y
            cv2.circle(image, (x, y), 2, (0, 255, 0), -1)

        # Guardar la imagen con los puntos de referencia
        output_path = os.path.join(output_folder, f"{os.path.splitext(image_name)[0]}_landmarks.jpg")
        cv2.imwrite(output_path, image)
        print(f"Procesada y guardada con landmarks: {output_path}")

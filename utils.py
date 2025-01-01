# utilidades


import os
import cv2
import json
import base64
import face_recognition
import numpy as np
import pymongo

from pymongo import MongoClient

def jsonify(face_encodings, img, output_folder="computing_vision\\faces", json_file="output.json"):
    
    """
    Detecta caras en un fotograma, guarda sus características en un archivo JSON y sus imágenes en una carpeta.

    Args:
        frame (numpy.ndarray): Imagen o fotograma donde se detectaron las caras.
        face_locations (list): Lista de coordenadas de las caras detectadas (top, right, bottom, left).
        output_folder (str): Carpeta donde se guardarán las imágenes de las caras.
        json_file (str): Nombre del archivo JSON donde se guardarán los datos.

    Returns:
        None
    """
    face_encodings = [encoding.tolist() if isinstance(encoding, np.ndarray) else encoding for encoding in face_encodings]
    
    os.makedirs(output_folder, exist_ok=True)  # Crear carpeta de salida si no existe
    data_list = []

    img_file = os.path.join(output_folder, img)
    
    # Codificar la imagen en base64
    with open(img_file, "rb") as img_file:
        face_image_base64 = base64.b64encode(img_file.read()).decode('utf-8')

    # Información del usuario (puedes modificar estos valores)
    user = input("introduzca el nombre de usuario:")

    # face_encodings = face_encodings.tolist()  # Convierte el numpy ndarray a lista
    
    # Crear un diccionario con los datos
    data = {
        "user": user,
        "vector_caracteristicas": face_encodings,
        "imagen": face_image_base64
        }

    # Agregar al listado de datos
    data_list.append(data)

    json_file = os.path.join(output_folder, json_file)
    # Guardar la información en un archivo JSON
    with open(json_file, "w") as json_out:
        json.dump(data_list, json_out, indent=4)

    print(f"Datos guardados en {json_file}")

def upToMongo(json_file):
    # Ruta del archivo JSON
    json_file_path = r"computing_vision\faces\output.json"

    # Configurar la conexión con MongoDB
    mongo_uri = "mongodb://localhost:27017/"  # Cambia a tu URI de MongoDB si usas un servidor remoto
    client = MongoClient(mongo_uri)

    # Seleccionar la base de datos y la colección
    db = client["vision_computacional"]
    collection = db["faces"]
    
    # Leer el archivo JSON
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)  # Cargar el JSON como un diccionario o lista de diccionarios
        
        # Insertar los datos en la colección
        if isinstance(data, list):  # Si el JSON contiene una lista de documentos
            result = collection.insert_many(data)
            print(f"Se insertaron {len(result.inserted_ids)} documentos en la colección.")
        else:  # Si el JSON contiene un solo documento
            result = collection.insert_one(data)
            print(f"Se insertó un documento con el ID: {result.inserted_id}")

    except FileNotFoundError:
        print("El archivo JSON no fue encontrado.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

    # Cerrar la conexión
    client.close()
    
def downFromMongo(face):
    # Configurar la conexión con MongoDB
    mongo_uri = "mongodb://localhost:27017/"  # Cambia a tu URI de MongoDB si usas un servidor remoto
    client = MongoClient(mongo_uri)

    # Seleccionar la base de datos y la colección
    db = client["vision_computacional"]
    collection = db["faces"]

    # Buscar un documento específico (puedes modificar el criterio de búsqueda)
    documento = collection.find_one({"user": face})  # También puedes usar find_one({"campo": valor}) para una búsqueda más específica

    if documento:
        # Acceder al campo que contiene la lista (por ejemplo, "vector_caracteristicas")
        vector_caracteristicas = documento.get("vector_caracteristicas", [])  # Si no existe, devuelve una lista vacía
        # print("Lista obtenida:", vector_caracteristicas)
    else:
        print("No se encontró el documento.")
    
    return vector_caracteristicas
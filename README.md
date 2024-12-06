# computing_vision
aplicacion de vision por computadora
cuenta el número de dedos levantados en un mano

**stack tecnólogico**

Lenguaje de programación: Python.
Librerías:
OpenCV: Para capturar video desde la webcam y procesar imágenes.
MediaPipe: Una solución de Google para la detección de manos y dedos que incluye modelos de aprendizaje automático preentrenados.
Numpy: Para procesar arrays de datos.
Entorno de desarrollo: Visual Studio Code

**calculo visual**
Calcular los dedos levantados se puede hacer comparando la posición de las articulaciones de los dedos detectadas por MediaPipe. Cada dedo tiene varios puntos clave (landmarks), y para determinar si un dedo está levantado, se puede comparar la posición de la punta del dedo con la posición de su articulación base.

MediaPipe detecta 21 puntos en cada mano.
Los puntos clave que usaremos son:
- TIPS (puntas): Puntos 4 (pulgar), 8 (índice), 12 (medio), 16 (anular), 20 (meñique).
- DIPs (articulaciones base de las puntas): Puntos 3, 7, 11, 15, 19.
Un dedo está levantado si la coordenada y de la punta es menor que la de la articulación base, asumiendo que la cámara apunta hacia la mano con los dedos hacia arriba.

**Función contar_dedos**: Evalúa si la punta del dedo está "levantada" comparando su posición relativa.
Para los dedos normales (índice, medio, anular, meñique), comparamos y (más bajo en la pantalla significa más arriba).
Para el pulgar, se usa la posición x porque se mueve de forma diferente.
Texto en pantalla: Se muestra el número de dedos levantados en tiempo real.


**Mejoras posibles**:
Interfaz gráfica: Usa frameworks como PyQt o Tkinter para añadir controles y una mejor visualización.
Guardar datos: Captura imágenes o coordenadas de las manos para análisis posterior.
Aplicaciones interactivas: Usa la detección para controlar el ratón o realizar gestos específicos para ejecutar comandos.
¿Quieres ayudar para implementar alguna funcionalidad específica o mejorar la aplicación? 😊


**Aplicaciones posibles**:

face detection: sistema de reconocimiento facial para control de accesos

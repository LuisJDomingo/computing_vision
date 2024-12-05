import cv2
import mediapipe as mp

# Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.9, min_tracking_confidence=0.9)
mp_drawing = mp.solutions.drawing_utils

# Función para contar dedos levantados
def contar_dedos(hand_landmarks):
    dedos_levantados = 0
    
    # Coordenadas de los puntos relevantes
    tips = [4, 8, 12, 16, 20]  # Puntas de los dedos
    intermedios = [3, 7, 11, 15, 19]  # Puntos intermedios de los dedos
    dips = [2, 6, 10, 14, 18]  # Articulaciones base
    
     # Comprobar si cada dedo está levantado
    for tip, intermedio, dip in zip(tips, intermedios, dips):
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[intermedio].y < hand_landmarks.landmark[dip].y:
            dedos_levantados += 1

    # Especial para el pulgar (usando su eje X y Y)
    if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
        dedos_levantados += 1

    return dedos_levantados

# Captura de video
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Invertir la imagen horizontalmente (efecto espejo)
    frame = cv2.flip(frame, 1)
    # Convertir BGR a RGB para MediaPipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    # Dibujar las anotaciones y contar dedos
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
            )
            # Contar dedos levantados
            dedos_levantados = contar_dedos(hand_landmarks)
            cv2.putText(frame, f"Dedos: {dedos_levantados}", (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Mostrar el video
    cv2.imshow("Detección de Dedos", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

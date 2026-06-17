import cv2
import numpy as np

video = cv2.VideoCapture("video_prueba.mp4")

if not video.isOpened():
    print("No se pudo abrir el video")
    exit()

ancho = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
alto = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(video.get(cv2.CAP_PROP_FPS)) or 30

salida = cv2.VideoWriter(
    "resultado_balon_limpio.mp4",
    cv2.VideoWriter_fourcc(*"mp4v"),
    fps,
    (ancho, alto)
)

trayectoria_balon = []
max_puntos_trayectoria = 25

while True:
    ret, frame = video.read()

    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    naranja_bajo = np.array([5, 100, 100])
    naranja_alto = np.array([25, 255, 255])

    mascara = cv2.inRange(hsv, naranja_bajo, naranja_alto)
    mascara = cv2.GaussianBlur(mascara, (5, 5), 0)

    contornos, _ = cv2.findContours(
        mascara,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    candidatos = []

    for contorno in contornos:
        area = cv2.contourArea(contorno)

        if 20 < area < 500:
            x, y, w, h = cv2.boundingRect(contorno)

            proporcion = w / h if h != 0 else 0

            # El balón debe ser pequeño y más o menos redondo
            if 0.6 < proporcion < 1.6:
                candidatos.append((area, x, y, w, h))

    if candidatos:
        # Nos quedamos con el candidato más grande dentro del rango permitido
        candidatos.sort(reverse=True)
        area, x, y, w, h = candidatos[0]

        centro_x = x + w // 2
        centro_y = y + h // 2

        trayectoria_balon.append((centro_x, centro_y))

        if len(trayectoria_balon) > max_puntos_trayectoria:
            trayectoria_balon.pop(0)

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 140, 255), 2)
        cv2.circle(frame, (centro_x, centro_y), 5, (0, 0, 255), -1)

        cv2.putText(
            frame,
            "Balon detectado",
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 140, 255),
            2
        )

    for i in range(1, len(trayectoria_balon)):
        cv2.line(frame, trayectoria_balon[i - 1], trayectoria_balon[i], (0, 0, 255), 2)

    salida.write(frame)
    cv2.imshow("Deteccion limpia de balon", frame)

    if cv2.waitKey(25) & 0xFF == ord("q"):
        break

video.release()
salida.release()
cv2.destroyAllWindows()

print("Video guardado como resultado_balon_limpio.mp4")
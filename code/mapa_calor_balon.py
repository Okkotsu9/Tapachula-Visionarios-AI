import cv2
import numpy as np

video = cv2.VideoCapture("video_prueba.mp4")

if not video.isOpened():
    print("No se pudo abrir el video")
    exit()

ancho = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
alto = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

heatmap = np.zeros((alto, ancho), dtype=np.float32)

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

            if 0.6 < proporcion < 1.6:
                candidatos.append((area, x, y, w, h))

    if candidatos:
        candidatos.sort(reverse=True)
        area, x, y, w, h = candidatos[0]

        centro_x = x + w // 2
        centro_y = y + h // 2

        cv2.circle(heatmap, (centro_x, centro_y), 25, 1, -1)

video.release()

heatmap = cv2.GaussianBlur(heatmap, (0, 0), 25)
heatmap_normalizado = cv2.normalize(heatmap, None, 0, 255, cv2.NORM_MINMAX)
heatmap_uint8 = heatmap_normalizado.astype(np.uint8)

heatmap_color = cv2.applyColorMap(heatmap_uint8, cv2.COLORMAP_JET)

video = cv2.VideoCapture("video_prueba.mp4")
ret, frame_base = video.read()
video.release()

if not ret:
    print("No se pudo leer el primer frame")
    exit()

resultado = cv2.addWeighted(frame_base, 0.65, heatmap_color, 0.35, 0)

cv2.putText(
    resultado,
    "Mapa de calor del balon",
    (30, 50),
    cv2.FONT_HERSHEY_SIMPLEX,
    1,
    (255, 255, 255),
    3
)

cv2.imwrite("mapa_calor_balon.png", resultado)

print("Mapa de calor guardado como mapa_calor_balon.png")
import cv2
import math

video = cv2.VideoCapture("video_prueba.mp4")

if not video.isOpened():
    print("No se pudo abrir el video")
    exit()

ancho = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
alto = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(video.get(cv2.CAP_PROP_FPS)) or 30

salida = cv2.VideoWriter(
    "resultado_tracking_robots.mp4",
    cv2.VideoWriter_fourcc(*"mp4v"),
    fps,
    (ancho, alto)
)

restador_fondo = cv2.createBackgroundSubtractorMOG2(
    history=500,
    varThreshold=40,
    detectShadows=False
)

robots = {}
siguiente_id = 1
distancia_maxima = 80
max_puntos = 40

while True:
    ret, frame = video.read()

    if not ret:
        break

    mascara = restador_fondo.apply(frame)

    _, mascara = cv2.threshold(mascara, 200, 255, cv2.THRESH_BINARY)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    mascara = cv2.morphologyEx(mascara, cv2.MORPH_OPEN, kernel)
    mascara = cv2.dilate(mascara, kernel, iterations=1)

    contornos, _ = cv2.findContours(
        mascara,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    detecciones = []

    for contorno in contornos:
        area = cv2.contourArea(contorno)

        if 250 < area < 6000:
            x, y, w, h = cv2.boundingRect(contorno)

            if w > 15 and h > 15:
                centro_x = x + w // 2
                centro_y = y + h // 2
                detecciones.append((centro_x, centro_y, x, y, w, h))

    ids_usados = set()

    for centro_x, centro_y, x, y, w, h in detecciones:
        mejor_id = None
        mejor_distancia = distancia_maxima

        for robot_id, datos in robots.items():
            ultimo_x, ultimo_y = datos["centro"]

            distancia = math.sqrt(
                (centro_x - ultimo_x) ** 2 + (centro_y - ultimo_y) ** 2
            )

            if distancia < mejor_distancia and robot_id not in ids_usados:
                mejor_distancia = distancia
                mejor_id = robot_id

        if mejor_id is None:
            mejor_id = siguiente_id
            siguiente_id += 1
            robots[mejor_id] = {
                "centro": (centro_x, centro_y),
                "trayectoria": []
            }

        robots[mejor_id]["centro"] = (centro_x, centro_y)
        robots[mejor_id]["trayectoria"].append((centro_x, centro_y))

        if len(robots[mejor_id]["trayectoria"]) > max_puntos:
            robots[mejor_id]["trayectoria"].pop(0)

        ids_usados.add(mejor_id)

        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.circle(frame, (centro_x, centro_y), 5, (0, 0, 255), -1)

        cv2.putText(
            frame,
            f"Robot {mejor_id}",
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 0, 0),
            2
        )

    for robot_id, datos in robots.items():
        trayectoria = datos["trayectoria"]

        for i in range(1, len(trayectoria)):
            cv2.line(
                frame,
                trayectoria[i - 1],
                trayectoria[i],
                (255, 255, 0),
                2
            )

    salida.write(frame)
    cv2.imshow("Tracking basico de robots", frame)

    if cv2.waitKey(25) & 0xFF == ord("q"):
        break

video.release()
salida.release()
cv2.destroyAllWindows()

print("Video guardado como resultado_tracking_robots.mp4")
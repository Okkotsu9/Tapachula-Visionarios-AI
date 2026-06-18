import cv2
import numpy as np
import math

video = cv2.VideoCapture("video_prueba.mp4")

if not video.isOpened():
    print("No se pudo abrir el video")
    exit()

ancho = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
alto = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(video.get(cv2.CAP_PROP_FPS)) or 30

salida = cv2.VideoWriter(
    "resultado_completo.mp4",
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
max_puntos_robots = 40

trayectoria_balon = []
max_puntos_balon = 30

while True:
    ret, frame = video.read()

    if not ret:
        break

    # =========================
    # DETECCIÓN DEL BALÓN
    # =========================
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    naranja_bajo = np.array([5, 100, 100])
    naranja_alto = np.array([25, 255, 255])

    mascara_balon = cv2.inRange(hsv, naranja_bajo, naranja_alto)
    mascara_balon = cv2.GaussianBlur(mascara_balon, (5, 5), 0)

    contornos_balon, _ = cv2.findContours(
        mascara_balon,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    candidatos_balon = []

    for contorno in contornos_balon:
        area = cv2.contourArea(contorno)

        if 20 < area < 500:
            x, y, w, h = cv2.boundingRect(contorno)
            proporcion = w / h if h != 0 else 0

            if 0.6 < proporcion < 1.6:
                candidatos_balon.append((area, x, y, w, h))

    if candidatos_balon:
        candidatos_balon.sort(reverse=True)
        area, x, y, w, h = candidatos_balon[0]

        centro_balon_x = x + w // 2
        centro_balon_y = y + h // 2

        trayectoria_balon.append((centro_balon_x, centro_balon_y))

        if len(trayectoria_balon) > max_puntos_balon:
            trayectoria_balon.pop(0)

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 140, 255), 2)
        cv2.circle(frame, (centro_balon_x, centro_balon_y), 5, (0, 0, 255), -1)

        cv2.putText(
            frame,
            "Balon",
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 140, 255),
            2
        )

    for i in range(1, len(trayectoria_balon)):
        cv2.line(
            frame,
            trayectoria_balon[i - 1],
            trayectoria_balon[i],
            (0, 0, 255),
            2
        )

    # =========================
    # DETECCIÓN Y TRACKING DE ROBOTS
    # =========================
    mascara_robots = restador_fondo.apply(frame)

    _, mascara_robots = cv2.threshold(
        mascara_robots,
        200,
        255,
        cv2.THRESH_BINARY
    )

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    mascara_robots = cv2.morphologyEx(mascara_robots, cv2.MORPH_OPEN, kernel)
    mascara_robots = cv2.dilate(mascara_robots, kernel, iterations=1)

    contornos_robots, _ = cv2.findContours(
        mascara_robots,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    detecciones = []

    for contorno in contornos_robots:
        area = cv2.contourArea(contorno)

        if 250 < area < 6000:
            x, y, w, h = cv2.boundingRect(contorno)

            if w > 15 and h > 15:
                centro_x = x + w // 2
                centro_y = y + h // 2
                detecciones.append((centro_x, centro_y, x, y, w, h))

    # Nos quedamos solo con los 3 objetos más grandes,
    # porque en este video de prueba hay 3 robots principales.
    detecciones = sorted(
        detecciones,
        key=lambda d: d[4] * d[5],
        reverse=True
    )

    detecciones = detecciones[:3]

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

        if len(robots[mejor_id]["trayectoria"]) > max_puntos_robots:
            robots[mejor_id]["trayectoria"].pop(0)

        ids_usados.add(mejor_id)

        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.circle(frame, (centro_x, centro_y), 5, (255, 255, 0), -1)

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

    # =========================
    # PANEL INFORMATIVO
    # =========================
    cv2.rectangle(frame, (10, 10), (430, 95), (0, 0, 0), -1)

    cv2.putText(
        frame,
        "Tapachula Visionarios AI",
        (20, 38),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"Robots detectados: {len(detecciones)} | Balon: {'Si' if candidatos_balon else 'No'}",
        (20, 70),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )

    salida.write(frame)
    cv2.imshow("Sistema completo FutBotMX", frame)

    if cv2.waitKey(25) & 0xFF == ord("q"):
        break

video.release()
salida.release()
cv2.destroyAllWindows()

print("Video guardado como resultado_completo.mp4")
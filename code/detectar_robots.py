import cv2

video = cv2.VideoCapture("video_prueba.mp4")

if not video.isOpened():
    print("No se pudo abrir el video")
    exit()

ancho = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
alto = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(video.get(cv2.CAP_PROP_FPS))

if fps == 0:
    fps = 30

salida = cv2.VideoWriter(
    "resultado_robots.mp4",
    cv2.VideoWriter_fourcc(*"mp4v"),
    fps,
    (ancho, alto)
)

restador_fondo = cv2.createBackgroundSubtractorMOG2(
    history=500,
    varThreshold=40,
    detectShadows=False
)

trayectorias = []

while True:
    ret, frame = video.read()

    if not ret:
        break

    mascara = restador_fondo.apply(frame)

    _, mascara = cv2.threshold(
        mascara,
        200,
        255,
        cv2.THRESH_BINARY
    )

    kernel = cv2.getStructuringElement(
        cv2.MORPH_RECT,
        (5, 5)
    )

    mascara = cv2.morphologyEx(
        mascara,
        cv2.MORPH_OPEN,
        kernel
    )

    contornos, _ = cv2.findContours(
        mascara,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    for contorno in contornos:

        area = cv2.contourArea(contorno)

        if 150 < area < 5000:

            x, y, w, h = cv2.boundingRect(contorno)

            centro_x = x + w // 2
            centro_y = y + h // 2

            trayectorias.append((centro_x, centro_y))

            if len(trayectorias) > 50:
                trayectorias.pop(0)

            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (255, 0, 0),
                2
            )

            cv2.circle(
                frame,
                (centro_x, centro_y),
                4,
                (0, 0, 255),
                -1
            )

            cv2.putText(
                frame,
                "Robot",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 0, 0),
                2
            )

    for i in range(1, len(trayectorias)):
        cv2.line(
            frame,
            trayectorias[i - 1],
            trayectorias[i],
            (255, 255, 0),
            2
        )

    salida.write(frame)

    cv2.imshow(
        "Deteccion de Robots",
        frame
    )

    if cv2.waitKey(25) & 0xFF == ord("q"):
        break

video.release()
salida.release()
cv2.destroyAllWindows()

print("Video guardado como resultado_robots.mp4")
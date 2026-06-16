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
    "resultado_movimiento.mp4",
    cv2.VideoWriter_fourcc(*"mp4v"),
    fps,
    (ancho, alto)
)

restador_fondo = cv2.createBackgroundSubtractorMOG2(
    history=700,
    varThreshold=65,
    detectShadows=False
)

while True:
    ret, frame = video.read()

    if not ret:
        break

    mascara = restador_fondo.apply(frame)

    mascara = cv2.GaussianBlur(mascara, (5, 5), 0)
    _, mascara = cv2.threshold(mascara, 200, 255, cv2.THRESH_BINARY)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
    mascara = cv2.morphologyEx(mascara, cv2.MORPH_OPEN, kernel)
    mascara = cv2.dilate(mascara, kernel, iterations=2)

    contornos, _ = cv2.findContours(
        mascara,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    for contorno in contornos:
        area = cv2.contourArea(contorno)

        if area > 1800:
            x, y, w, h = cv2.boundingRect(contorno)

            if w > 40 and h > 40:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(
                    frame,
                    "Movimiento detectado",
                    (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2
                )

    salida.write(frame)
    cv2.imshow("Analisis mejorado", frame)

    if cv2.waitKey(25) & 0xFF == ord("q"):
        break

video.release()
salida.release()
cv2.destroyAllWindows()

print("Video guardado como resultado_movimiento.mp4")
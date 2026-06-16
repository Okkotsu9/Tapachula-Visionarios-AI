import cv2

video = cv2.VideoCapture("video_prueba.mp4")

if not video.isOpened():
    print("No se pudo abrir el video")
    exit()

while True:
    ret, frame = video.read()

    if not ret:
        break

    cv2.imshow("Video FutBotMX", frame)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
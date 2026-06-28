import cv2
import pupil_apriltags

detector = pupil_apriltags.Detector()
cam = cv2.VideoCapture(0)

while True:
    ret, frame = cam.read()
    if not ret:
        break

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    detections = detector.detect(gray_frame)

    for detection in detections:
        corners = detection.corners 
        for i in range(4):
            cv2.line(frame, tuple(corners[i]), tuple(corners[(i + 1) % 4]), (0, 255, 0), 2)

        tag_id = detection.tag_id
        center = detection.center
        cv2.putText(frame, f'Tag ID: {tag_id}', (int(center[0]), int(center[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    cv2.imshow('AprilTag Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
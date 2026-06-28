import cv2
import pupil_apriltags

def detect_apriltags(image):
    detector = pupil_apriltags.Detector(families='tag36h11', nthreads=4, quad_decimate=1.0, quad_sigma=0.0, refine_edges=True)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    tags = detector.detect(gray)

    for tag in tags:
        corners = tag.corners
        for i in range(4):
            pt1 = (int(corners[i][0]), int(corners[i][1]))
            pt2 = (int(corners[(i + 1) % 4][0]), int(corners[(i + 1) % 4][1]))
            cv2.line(image, pt1, pt2, (0, 255, 0), 2)

        cv2.putText(image, str(tag.tag_id), (int(tag.center[0]), int(tag.center[1])),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    return image

def main():
    use_camera = True
    image_path = 'image.jpg'

    if use_camera:
        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            print("Error: Could not open camera.")
            return

        while True:
            ret, frame = cam.read()
            if not ret:
                print("Error: Frame not captured.")
                break

            processed_frame = detect_apriltags(frame)
            cv2.imshow('AprilTag Detection', processed_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cam.release()
    else:
        image = cv2.imread(image_path)
        if image is None:
            print("Error: Image not found.")
            return

        processed_image = detect_apriltags(image)
        cv2.imshow("AprilTag Detection", processed_image)
        cv2.waitKey(0)

    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
import cv2
import numpy as np
import apriltag

def draw_tag_dimensions(frame, corners, id):
    tag_size = 0.165  # original size of an apriltag(165mm)
    tag_corners_3D = np.array([
        [-tag_size / 2, -tag_size / 2, 0],
        [tag_size / 2, -tag_size / 2, 0],
        [tag_size / 2, tag_size / 2, 0],
        [-tag_size / 2, tag_size / 2, 0]
    ], dtype=np.float32)

    camera_matrix = np.array([[640, 0, 320],
                               [0, 640, 240],
                               [0, 0, 1]], dtype=np.float32)
    dist_coeffs = np.zeros((4, 1))

    rvec, tvec, _ = cv2.solvePnP(tag_corners_3D, corners, camera_matrix, dist_coeffs)

    projected_points, _ = cv2.projectPoints(tag_corners_3D, rvec, tvec, camera_matrix, dist_coeffs)

    cv2.putText(frame, f'ID: {id}', (int(corners[0][0][0]), int(corners[0][0][1]) - 10), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    for point in projected_points:
        cv2.circle(frame, (int(point[0][0]), int(point[0][1])), 5, (0, 255, 0), -1)

    for i in range(len(projected_points)):
        start = projected_points[i][0]
        end = projected_points[(i + 1) % len(projected_points)][0]
        cv2.line(frame, (int(start[0]), int(start[1])), (int(end[0]), int(end[1])), (0, 255, 0), 2)

def main():
    cap = cv2.VideoCapture(0)

    detector = apriltag.Detector()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        tags = detector.detect(gray)

        for tag in tags:
            corners = tag.corners
            draw_tag_dimensions(frame, corners, tag.tag_id)

        cv2.imshow('AprilTag Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
    #apriltag library'si kurulu ise matrix çalışır.
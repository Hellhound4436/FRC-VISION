import cv2
import numpy as np
from pupil import Detector

detector = Detector(families='tag36h11', nthreads=4, quad_decimate=1.0, quad_sigma=0.0, refine_edges=True)

image = cv2.imread('image.jpg')
if image is None:
    print("Error: Image not found.")
    exit()
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

cv2.imshow("AprilTag Detection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
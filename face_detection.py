import os
from imutils import face_utils
import dlib
import cv2
import numpy as np


def process_video(video_path, output_folder):
    p = "/Users/yairkruskal/Downloads/facial-landmarks-recognition-master/shape_predictor_68_face_landmarks.dat"
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(p)

    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_number = 0

    while True:
        _, image = cap.read()
        image = cv2.resize(image, None, fx=8, fy=8, interpolation=cv2.INTER_CUBIC)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        frame_number += 1
        progress_percent = (frame_number / total_frames) * 100

        rects = detector(gray, 0)

        for (i, rect) in enumerate(rects):
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)

            for (x, y) in shape:
                cv2.circle(image, (x, y), 2, (0, 255, 0), -1)

            (x, y, w, h) = cv2.boundingRect(np.array([shape]))
            face = image[y:y + h, x:x + w]

            if not face.size == 0:
                filename = os.path.join(output_folder, f"face_frame_{frame_number}_face_{i}.jpg")
                print(f"[+] Face detected from frame: {frame_number}, face {i} ")
                cv2.imwrite(filename, face)

        print(f"Progress: {progress_percent:.2f}%")

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()
    cap.release()



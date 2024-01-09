import os
import cv2
import mediapipe as mp
import numpy as np
import re

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

async def detect_pose(session_key):
    local_file_path = f"user/{session_key}"
    img_list = [file for file in os.listdir(local_file_path) if file.endswith(".png") or file.endswith(".jpg")]
    img_list.sort(key=natural_sort_key)

    imgs = [cv2.imread(local_file_path + '/' + img) for img in img_list]

    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    if not os.path.exists(local_file_path + '/capture'):
        os.makedirs(local_file_path + '/capture')

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        for idx, frame in enumerate(imgs):
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            results = pose.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            try:
                landmarks = results.pose_landmarks.landmark

                left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

                right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

                left_angle1 = calculate_angle(right_shoulder, left_shoulder, left_elbow)
                left_angle2 = calculate_angle(left_shoulder, left_elbow, left_wrist)
                right_angle1 = calculate_angle(left_shoulder, right_shoulder, right_elbow)
                right_angle2 = calculate_angle(right_shoulder, right_elbow, right_wrist)

                state1, state2, state3, state4 = 0, 0, 0, 0

                if left_angle1 > 110:
                    state1 = 1
                if left_angle2 < 140:
                    state2 = 1
                if right_angle1 > 110:
                    state3 = 1
                if right_angle2 < 140:
                    state4 = 1

                if (state1 and state2) or (state3 and state4):
                    cv2.imwrite(f'{local_file_path}/capture/pic' + str(idx) +'.png', image)

                print("Left Shoulder-Elbow angle: ", left_angle1, "Left Elbow-Wrist angle: ", left_angle2)
                print("Right Shoulder-Elbow angle: ", right_angle1, "Right Elbow-Wrist angle: ", right_angle2)

                cv2.putText(image, str(left_angle1), tuple(np.multiply(left_shoulder, [640, 480]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(image, str(left_angle2), tuple(np.multiply(left_elbow, [640, 480]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(image, str(right_angle1), tuple(np.multiply(right_shoulder, [640, 480]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(image, str(right_angle2), tuple(np.multiply(right_elbow, [640, 480]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

            except:
                pass

            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2))



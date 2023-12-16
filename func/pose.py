import os
import mediapipe as mp
import cv2
import numpy as np
import re
def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

def calculate_angle(a,b,c):
    
    # 각 값을 받아 넘파이 배열로 변형
    a = np.array(a) # 첫번째
    b = np.array(b) # 두번째
    c = np.array(c) # 세번째

    # 라디안을 계산하고 실제 각도로 변경한다.
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)

    # 180도가 넘으면 360에서 뺀 값을 계산한다.
    if angle >180.0:
        angle = 360-angle

    # 각도를 리턴한다.
    return angle

def detect_pose(session_key):
    local_file_path = f"user/{session_key}"
    # 이미지 불러오기
    img_list = os.listdir(local_file_path)
    img_list.sort()

    imgs = []

    for img in img_list:
        imgs.append(cv2.imread(local_file_path + '/' + img))

    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    # local_file_path에 capture 폴더 생성
    if not os.path.exists(local_file_path + '/capture'):
        os.makedirs(local_file_path + '/capture')

    cap = cv2.VideoCapture(0)
    count = 0
    state1 = 0
    state2 = 0
    state3 = 0
    state4 = 0
    pose_state = 0

    ## Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        for frame in imgs:
        # while cap.isOpened():
            # ret, frame = cap.read()
            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
        
            # Make detection
            results = pose.process(image)
        
            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            # mkdir 
            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark
                
                # Get coordinates
                left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                
                right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                
                # Calculate angle
                left_angle1 = calculate_angle(right_shoulder, left_shoulder, left_elbow)
                left_angle2 = calculate_angle(left_shoulder, left_elbow, left_wrist)
                right_angle1 = calculate_angle(left_shoulder, right_shoulder, right_elbow)
                right_angle2 = calculate_angle(right_shoulder, right_elbow, right_wrist)
                
                if left_angle1 < 110:
                    state1 = 0
                if left_angle1 > 120 and state1 == 0:
                    state1= 1

                if left_angle2 > 160:
                    state2 = 0
                if left_angle2 < 90 and state2 == 0:
                    state2=1
                
                if right_angle1 < 110:
                    state3 = 0
                if right_angle1 > 120 and state3 == 0:
                    state3= 1
                
                if right_angle2 > 160:
                    state4 = 0
                if right_angle2 < 90 and state4 == 0:
                    state4=1

                if not pose_state:
                    if state1 and state2:
                        pose_state = 1
                        count += 1
                        cv2.imwrite(f'{local_file_path}/capture/pic' + str(count) +'.png', image)
                    elif state1 and not state2:
                        pose_state = 1
                        count += 1
                        cv2.imwrite(f'{local_file_path}/capture/pic' + str(count) +'.png', image)
                    elif not state1 and state2:
                        pose_state = 1
                        count += 1
                        cv2.imwrite(f'{local_file_path}/capture/pic' + str(count) +'.png', image)

                    if state3 and state4:
                        pose_state = 1
                        count += 1
                        cv2.imwrite(f'{local_file_path}/capture/pic' + str(count) +'.png', image)
                    elif state3 and not state4:
                        pose_state = 1
                        count += 1
                        cv2.imwrite(f'{local_file_path}/capture/pic' + str(count) +'.png', image)
                    elif not state3 and state4:
                        pose_state = 1
                        count += 1
                        cv2.imwrite(f'{local_file_path}/capture/pic' + str(count) +'.png', image)

                if (not state1 and not state2) and (not state3 and not state4):
                    pose_state = 0

                
                print("state1: ", state1, "state2: ", state2, "state3: ", state3, "state4: ", state4)
                print("pose_state: ", pose_state)
                print(count)
                    
                # Visualize angle
                cv2.putText(image, str(left_angle1), 
                            tuple(np.multiply(left_shoulder, [640, 480]).astype(int)), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                    )
                cv2.putText(image, str(left_angle2), 
                            tuple(np.multiply(left_elbow, [640, 480]).astype(int)), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                    )
                
                cv2.putText(image, str(right_angle1), 
                            tuple(np.multiply(right_shoulder, [640, 480]).astype(int)), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                    )
                cv2.putText(image, str(right_angle2), 
                            tuple(np.multiply(right_elbow, [640, 480]).astype(int)), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                    )
                        
            except:
                pass
            
            
            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                    )               
            
            # cv2.imshow('Mediapipe Feed', image)

            # if cv2.waitKey(10) & 0xFF == ord('q'):
            #     break

        cap.release()
        cv2.destroyAllWindows()
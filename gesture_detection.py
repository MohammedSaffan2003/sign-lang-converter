# gesture_detection.py
import cv2
import mediapipe as mp
from utils import count_raised_fingers

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)

def detect_hand_gesture(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    hand_result = hands.process(rgb_frame)
    hand_gesture = ""

    if hand_result.multi_hand_landmarks:
        hand_landmarks_list = hand_result.multi_hand_landmarks
        
        for hand_landmarks in hand_landmarks_list:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                                   landmark_drawing_spec=mp_draw.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=4))
        hand_gesture = count_raised_fingers(hand_landmarks_list)

    return hand_gesture, frame

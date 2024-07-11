# gesture_detection.py
import cv2
import mediapipe as mp
from utils import (
    count_raised_fingers, get_head_gesture, are_hands_together,
    is_right_hand_on_chest, is_index_finger_curved, recognize_complex_gestures,
    is_thumbs_up, is_thumbs_down, is_peace_sign, is_hand_raised, WaveDetector
)

mp_hands = mp.solutions.hands
mp_face_mesh = mp.solutions.face_mesh
mp_draw = mp.solutions.drawing_utils
# mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.7, min_tracking_confidence=0.5)

def detect_hand_gesture(frame):
    frame = cv2.flip(frame, 1)  # Flip the frame horizontally
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    hand_result = hands.process(rgb_frame)
    hand_gesture = ""

    if hand_result.multi_hand_landmarks:
        hand_landmarks_list = hand_result.multi_hand_landmarks
        
        for hand_landmarks in hand_landmarks_list:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                                   landmark_drawing_spec=mp_draw.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=4))
        
        hand_gesture = recognize_complex_gestures(hand_landmarks_list)
        if not hand_gesture:
            hand_gesture = count_raised_fingers(hand_landmarks_list)

    return hand_gesture, frame




mp_holistic = mp.solutions.holistic

holistic = mp_holistic.Holistic(
    min_detection_confidence=0.7, min_tracking_confidence=0.5
)

wave_detector = WaveDetector()
import cv2
import mediapipe as mp
from utils import (
    count_raised_fingers, get_head_gesture, are_hands_together,
    is_right_hand_on_chest, is_index_finger_curved, recognize_complex_gestures,
    is_thumbs_up, is_thumbs_down, is_peace_sign, is_hand_raised, WaveDetector
)

mp_holistic = mp.solutions.holistic
mp_draw = mp.solutions.drawing_utils

holistic = mp_holistic.Holistic(
    min_detection_confidence=0.7, min_tracking_confidence=0.5
)

wave_detector = WaveDetector()

def detect_gestures(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = holistic.process(rgb_frame)
    gesture = ""

    if result.face_landmarks:
        # Draw face landmarks
        mp_draw.draw_landmarks(
            frame, result.face_landmarks, mp_holistic.FACEMESH_TESSELATION,
            landmark_drawing_spec=mp_draw.DrawingSpec(color=(255, 255, 255), thickness=1, circle_radius=1),
            connection_drawing_spec=mp_draw.DrawingSpec(color=(0, 0, 255), thickness=1, circle_radius=1)
        )

    hand_landmarks_list = []
    if result.left_hand_landmarks:
        hand_landmarks_list.append(result.left_hand_landmarks)
    if result.right_hand_landmarks:
        hand_landmarks_list.append(result.right_hand_landmarks)

    for hand_landmarks in hand_landmarks_list:
        mp_draw.draw_landmarks(frame, hand_landmarks, mp_holistic.HAND_CONNECTIONS)

    if hand_landmarks_list:
        gesture = recognize_complex_gestures(hand_landmarks_list)
    else:
        gesture = "No Gesture Detected"

    return gesture, frame

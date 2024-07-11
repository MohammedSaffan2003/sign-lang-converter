import mediapipe as mp

mp_hands = mp.solutions.hands

def count_raised_fingers(hand_landmarks_list):
    total_count = 0
    tips_ids = [mp_hands.HandLandmark.THUMB_TIP, 
                mp_hands.HandLandmark.INDEX_FINGER_TIP, 
                mp_hands.HandLandmark.MIDDLE_FINGER_TIP, 
                mp_hands.HandLandmark.RING_FINGER_TIP, 
                mp_hands.HandLandmark.PINKY_TIP]
    pip_ids = [mp_hands.HandLandmark.THUMB_IP, 
               mp_hands.HandLandmark.INDEX_FINGER_PIP, 
               mp_hands.HandLandmark.MIDDLE_FINGER_PIP, 
               mp_hands.HandLandmark.RING_FINGER_PIP, 
               mp_hands.HandLandmark.PINKY_PIP]

    for hand_landmarks in hand_landmarks_list:
        count = 0
        for tip, pip in zip(tips_ids, pip_ids):
            if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y:
                count += 1
        total_count += count

    return total_count

def get_head_gesture(face_landmarks):
    nose_tip = face_landmarks.landmark[1]
    if nose_tip.x < 0.4:
        return "Looking left"
    elif nose_tip.x > 0.6:
        return "Looking right"
    elif nose_tip.y < 0.4:
        return "Looking up"
    elif nose_tip.y > 0.6:
        return "Looking down"
    else:
        return "Looking straight"

def are_hands_together(left_hand, right_hand):
    left_wrist = left_hand.landmark[mp_hands.HandLandmark.WRIST]
    right_wrist = right_hand.landmark[mp_hands.HandLandmark.WRIST]
    distance = ((left_wrist.x - right_wrist.x) ** 2 + (left_wrist.y - right_wrist.y) ** 2) ** 0.5
    return distance < 0.1

def is_right_hand_on_chest(right_hand):
    wrist = right_hand.landmark[mp_hands.HandLandmark.WRIST]
    chest_area_y = 0.5  # Adjust based on your frame
    return wrist.y > chest_area_y

def is_index_finger_curved(hand_landmarks):
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    index_pip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP]
    return index_tip.y > index_pip.y

class WaveDetector:
    def __init__(self):
        self.previous_wrist_positions = []
        self.max_positions = 10

    def update_wrist_position(self, wrist):
        self.previous_wrist_positions.append((wrist.x, wrist.y))
        if len(self.previous_wrist_positions) > self.max_positions:
            self.previous_wrist_positions.pop(0)

    def is_waving(self):
        if len(self.previous_wrist_positions) < self.max_positions:
            return False
        x_positions = [pos[0] for pos in self.previous_wrist_positions]
        if max(x_positions) - min(x_positions) > 0.1:
            return True
        return False

def is_thumbs_up(hand_landmarks):
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    thumb_ip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]
    return thumb_tip.y < thumb_ip.y

def is_thumbs_down(hand_landmarks):
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    thumb_ip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]
    return thumb_tip.y > thumb_ip.y

def is_peace_sign(hand_landmarks):
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

    index_pip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP]
    middle_pip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP]
    ring_pip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP]
    pinky_pip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP]

    return (index_tip.y < index_pip.y and
            middle_tip.y < middle_pip.y and
            ring_tip.y > ring_pip.y and
            pinky_tip.y > pinky_pip.y)

def is_hand_raised(hand_landmarks):
    wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
    return wrist.y < 0.3

def recognize_complex_gestures(hand_landmarks_list):
    if len(hand_landmarks_list) == 2:
        left_hand = hand_landmarks_list[0]
        right_hand = hand_landmarks_list[1]
        
        if are_hands_together(left_hand, right_hand):
            return "Good morning"
        
        if is_right_hand_on_chest(right_hand):
            return "Thank you"

    for hand_landmarks in hand_landmarks_list:
        if is_index_finger_curved(hand_landmarks):
            return "Question"
        
        if is_thumbs_up(hand_landmarks):
            return "Thumbs Up"
        
        if is_thumbs_down(hand_landmarks):
            return "Thumbs Down"
        
        if is_peace_sign(hand_landmarks):
            return "Peace Sign"
        
        if is_hand_raised(hand_landmarks):
            return "Hand Raised"
        
        wave_detector.update_wrist_position(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST])
        if wave_detector.is_waving():
            return "Waving"
    
    return None

import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)

def finger_state(lm):
    fingers = []

    fingers.append(1 if lm[4].x < lm[3].x else 0)

    tips = [8, 12, 16, 20]
    pips = [6, 10, 14, 18]

    for t, p in zip(tips, pips):
        fingers.append(1 if lm[t].y < lm[p].y else 0)

    return fingers

def get_hand_state(frame):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )
            return finger_state(hand_landmarks.landmark)
    return None

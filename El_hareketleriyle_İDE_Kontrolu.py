import cv2
import mediapipe as mp
import pyautogui
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

finger_tips = [4, 8, 12, 16, 20]

last_action_time = 0

def get_finger_states(hand_landmarks):
    fingers = []
   
    for i in range(5):
        tip = hand_landmarks.landmark[finger_tips[i]]
        pip = hand_landmarks.landmark[finger_tips[i] - 2]
        if i == 0:
            fingers.append(tip.x < pip.x)  # Sağ el için
        else:
            fingers.append(tip.y < pip.y)
    return fingers  

while True:
    success, frame = cap.read()
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        fingers = get_finger_states(hand_landmarks)
        total_open = fingers.count(True)
        current_time = time.time()

        if total_open == 5 and current_time - last_action_time > 1:
            pyautogui.hotkey('ctrl', 'enter')
            print("👉 ÇALIŞTIR (Ctrl + Enter)")
            last_action_time = current_time

        elif total_open == 0 and current_time - last_action_time > 1:
            pyautogui.hotkey('ctrl', 's')
            print("💾 KAYDET (Ctrl + S)")
            last_action_time = current_time

        elif fingers == [False, True, False, False, False] and current_time - last_action_time > 0.5:
            pyautogui.scroll(-200)
            print("🔽 SCROLL AŞAĞI")
            last_action_time = current_time

    cv2.imshow("Gesture Code Controller", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()

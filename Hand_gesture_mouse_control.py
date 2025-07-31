import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time


screen_width, screen_height = pyautogui.size()


cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils


prev_x, prev_y = 0, 0
smoothening = 5

while True:
    success, frame = cap.read()
    frame = cv2.flip(frame, 1)  
    h, w, _ = frame.shape

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            landmarks = hand_landmarks.landmark

            index_finger_tip = landmarks[8]
            thumb_tip = landmarks[4]
            x = int(index_finger_tip.x * w)
            y = int(index_finger_tip.y * h)


            screen_x = np.interp(x, (0, w), (0, screen_width))
            screen_y = np.interp(y, (0, h), (0, screen_height))

        
            curr_x = prev_x + (screen_x - prev_x) / smoothening
            curr_y = prev_y + (screen_y - prev_y) / smoothening
            pyautogui.moveTo(curr_x, curr_y)
            prev_x, prev_y = curr_x, curr_y

            # Tıklama algıla
            thumb_x, thumb_y = int(thumb_tip.x * w), int(thumb_tip.y * h)
            distance = np.hypot(thumb_x - x, thumb_y - y)

            if distance < 30:
                pyautogui.click()
                time.sleep(0.2)  
              
    cv2.imshow("Hand Mouse", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC tuşuyla çık
        break

cap.release()
cv2.destroyAllWindows()

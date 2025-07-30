import cv2
import mediapipe as mp
import pyautogui

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

webcam = cv2.VideoCapture(0)
screen_w,screen_h = pyautogui.size()
while True:
    success, image = webcam.read()
    if not success:
        break

    image = cv2.flip(image, 1)
    window_h, window_w, _ = image.shape

    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_image)

    if results.multi_face_landmarks:
        landmarks = results.multi_face_landmarks[0].landmark

        for id,point in enumerate(landmarks[474:478]):  # Sağ göz kenarları
            x = int(point.x * window_w)
            y = int(point.y * window_h)
            print(x, y)
            cv2.circle(image, (x, y), 3, (0, 0, 255), -1)

        left_eye = [landmarks[145], landmarks[159]]
        for point in left_eye:
            x = int(point.x * window_w)
            y = int(point.y * window_h)
           # print(x, y)
            if id==1:
                mouse_x = (screen_w / window_w*x)
                mouse_y = (screen_h / window_h * y)
                pyautogui.moveTo(mouse_x, mouse_y)

            cv2.circle(image, (x, y), 3, (0, 255, 255), -1)
        if (left_eye[0].y -left_eye[1].y<0.01 ) :
            pyautogui.click()
            pyautogui.sleep(2)
            print('mouse click')

    cv2.imshow("Eye controlled mouse", image)
    key = cv2.waitKey(10)
    if key == 27:  # ESC tuşu
        break

webcam.release()
cv2.destroyAllWindows()



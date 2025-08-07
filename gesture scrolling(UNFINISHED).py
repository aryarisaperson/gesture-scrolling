import cv2, time, pyautogui, mediapipe as mp

mp_hands=mp.solutions.hands
hands=mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_drawing=mp.solutions.drawing_utils


mun1, num2=100, 200 #completely unrelated to the whole thing
scrollspeed=300

scrolldelay=1

cam_width, cam_height=640, 480
def detect_gesture(landmarks, handedness):
    fingers=[]
    tips=[mp_hands.HandLandmark.INDEX_FINGER_TIP,mp_hands.HandLandmark.MIDDLE_FINGER_TIP, mp_hands.HandLandmark.RING_FINGER_TIP, mp_hands.HandLandmark.PINKY_FINGER_TIP]
    for tip in tips:
        if landmarks.landmark[tip].y< landmarks.landmark[tip-2].y:
            fingers.append(1)
    thumb_tip=landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    thumb_ip=landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]
    if (handedness=="Right" and thumb_tip>thumb_tip.x ) or (handedness=="Left" and thumb_tip<thumb_tip.x):
        fingers.append(1)
    return "scroll_up" if sum(fingers)==5 else "scroll_down" if len(fingers)==0 else "none"


cap=cv2.VideoCapture(0)
cap.set(3, cam_width)
cap.set(4, cam_height)
last_scroll=p_time=0
print("gesture scroll control is active right now, please open palm or make a fist for scrolling capabilities. Press Q to exit")
while cap.isOpened():
    success, img=cap.read()
    if not success:
        break
    img=cv2.flip(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), 1)
    results=hands.process(img)
    gesture, handedness="none", "Unknown"
    if results.multi_hand_landmarks:
        for hand, handedness_info in zip(results.multi_hand_landmarks, results.multi_handedness):
            handedness=handedness_info.classification[0].label
            gesture=detect_gesture(hand, handedness)
            mp_drawing.draw_landmarks(img, hand, mp_hands.HAND_CONNECTIONS)

            if (time.time()-last_scroll)> scrolldelay:
                if gesture=="scroll_up":
                    pyautogui.scroll(scrollspeed)
                elif gesture=="scroll_down":
                    pyautogui.scroll(-scrollspeed)
                last_scroll=time.time()
    fps=1/(time.time()-p_time) if (time.time()-p_time)>0 else 0
    p_time=time.time()
    cv2.putText(img, f"FPS:{int(fps)} |  hand:{handedness} | Gesture: {gesture}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
    cv2.imshow("gesture control", cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
    if cv2.waitKey(1) & 0xFF==ord("q"): break

cap.release()
cv2.destroyAllWindows()



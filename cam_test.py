import cv2
import mediapipe as mp
import math
mp_hands = mp.solutions.hands
mp_hands_p = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.6, min_tracking_confidence=0.6)
mp_drawing = mp.solutions.drawing_utils

webcam = cv2.VideoCapture(0)
frame_nb = 0
while webcam.isOpened():
    success, img = webcam.read()
    # n_size = (int(img.shape[1] * 0.6), int(img.shape[0] * 0.6))
    # img = cv2.resize(img, n_size, interpolation=cv2.INTER_AREA)
    if frame_nb%1 == 0:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = mp_hands_p.process(img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            # lml = []
            # lml_px = []
            # for id, lm in enumerate(results.multi_hand_landmarks[0].landmark):
            #     h, w, _ = img.shape
            #     xc, yc = int(lm.x * w), int(lm.y * h)
            #     lml.append([lm.x, lm.y, lm.z])
            #     lml_px.append([xc, yc])
                #cv2.circle(img, (xc, yc), 3, (200, 0,0), -1)
            # if len(lml) < 12:continue
            # x=lml[12][0]
            # vel = px - x
            # px= x
            # if vel < -0.2:print("swipe" + str(vel))
            # if len(lml)< 9:continue
            # x1, y1 = lml[4][1], lml[4][2]
            # x2, y2 = lml[8][1], lml[8][2]
            # cv2.circle(img, (x1, y1), 10, (255, 0, 128), cv2.FILLED)
            # cv2.circle(img, (x2, y2), 10, (255, 0, 128), cv2.FILLED)
            # cv2.line(img, (x1, y1), (x2, y2), (255, 0, 128), 3)
            #distance = math.hypot(x2 - x1, y2 - y1)
            #cv2.putText(img, str(int(distance)), (cx+30, cy), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 128), 3)
            for hand_landmarks in results.multi_hand_landmarks:
               mp_drawing.draw_landmarks(img, hand_landmarks, connections=mp_hands.HAND_CONNECTIONS)


    cv2.imshow('Koolac', img)
    frame_nb = (frame_nb + 1)%100
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

webcam.release()
cv2.destroyAllWindows()

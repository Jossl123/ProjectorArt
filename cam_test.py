import cv2
import mediapipe as mp
import math

class VideoAnalyser:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_hands_p = self.mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.6, min_tracking_confidence=0.6)
        self.mp_drawing = mp.solutions.drawing_utils
        self.webcam = cv2.VideoCapture(0)
        self.frame_nb = 0
        self.lml=[]
        self.lml_px=[]
    def get_img(self):
        # n_size = (int(img.shape[1] * 0.6), int(img.shape[0] * 0.6))
        # img = cv2.resize(img, n_size, interpolation=cv2.INTER_AREA)
        return self.webcam.read()
    def analyse_img(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.mp_hands_p.process(img)
        #img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        return results
    def update(self):
        success,img = self.get_img()
        results = self.analyse_img(img)
        if self.frame_nb%1 == 0:
            if results.multi_hand_landmarks:
                self.lml = []
                self.lml_px = []
                for id, lm in enumerate(results.multi_hand_landmarks[0].landmark):
                    h, w, _ = img.shape
                    xc, yc = int(lm.x * w), int(lm.y * h)
                    self.lml.append([lm.x, lm.y, lm.z])
                    self.lml_px.append([xc, yc])
                self.draw_marks(img, results.multi_hand_landmarks)
                self.draw_index_thumb_dist(img)

        cv2.imshow('Koolac', img)
        self.frame_nb = (self.frame_nb + 1)%100

    def draw_index_thumb_dist(self, img):
        if len(self.lml_px)< 9:return
        x1, y1 = self.lml_px[4][0], self.lml_px[4][1]
        x2, y2 = self.lml_px[8][0], self.lml_px[8][1]
        cv2.circle(img, (x1, y1), 10, (255, 0, 128), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255, 0, 128), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 128), 3)
        distance = math.hypot(x2 - x1, y2 - y1)
        cv2.putText(img, str(int(distance)), (x1+30, y1+20), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 128), 3)

    def draw_marks(self, img , multi_hand_marks):
        for hand_landmarks in multi_hand_marks:
            self.mp_drawing.draw_landmarks(img, hand_landmarks, connections=self.mp_hands.HAND_CONNECTIONS)

video_analyser = VideoAnalyser()
while video_analyser.webcam.isOpened():
    video_analyser.update()
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break
video_analyser.webcam.release()
cv2.destroyAllWindows()
import cv2
import mediapipe as mp
import time

class handDetector():
    def __init__(self, mode=False, maxHands=2, complexity=1, detectionCon=0.5, trackCon=0.5 ):
        self.mode = mode
        self.maxHands = maxHands
        self.complexity = complexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands  # we have to use this before using the mediapipe model
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.complexity, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils  # module provided in mediapipe for landmarks or drawing

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # convert to rgb
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def get_label(self, img, draw=True):
        htype = ''
        if self.results.multi_hand_landmarks:
            for hand_index, hand_info in enumerate(self.results.multi_handedness):
                hand_type = hand_info.classification[0].label
                if hand_type == 'Right':
                    hand_type = 'Left'
                else:
                    hand_type = 'Right'
                # hands_status[hand_type] = True
                # hands_status[hand_type + '_index'] = hand_index
                htype = hand_type
                if draw:
                    cv2.putText(img, f'{int(hand_info.classification[0].score * 100)}% ' + hand_type, (300, 70),
                                        cv2.FONT_HERSHEY_PLAIN, 2,
                                        (255, 0, 255), 2)
        return htype, img

    def findPosition(self, img, handNo=0, draw=True):

        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
        return lmList


def main():  # we can use only this main code in other projects to get the landmarks and tracking
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)  # video object created
    detector = handDetector()
    while True:
        success, img = cap.read()  # this will give frame
        img = detector.findHands(img)
        lt, img = detector.get_label(img)
        lmList = detector.findPosition(img)
        #if len(lmList)!=0:
            # print(lmList[4])

        cTime = time.time()  # getting current time
        fps = 1 / (cTime - pTime)  # getting fps
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 255),
                    3)  # placing the fps meter on
        # on the screen with inbuilt parameters
        cv2.imshow("Image", img)  # for showing in the webcam to run it
        cv2.waitKey(1)



if __name__ == "__main__":
    main()
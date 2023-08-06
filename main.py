import os
import cvzone
import cv2
from cvzone.PoseModule import PoseDetector

#カメラなら
# cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture("Resources/Videos/1.mp4")
detector = PoseDetector()

shirtFolderPath = "Resources/Shirts"
listShirts = os.listdir(shirtFolderPath)
# print(listShirts)

# width of shirt / width of point 11 and 12
fixedRatio = 262/190
shirtRatioHeightWidth = 581/440
imgNumber = 0
imgButtonRight = cv2.imread("Resources/button.png", cv2.IMREAD_UNCHANGED)
imgButtonLeft = cv2.flip(imgButtonRight, 1)
counterRight = 0
counterLeft = 0
selectionSpeed = 50

while True:
    success, img = cap.read()
    img = detector.findPose(img)
    # img = cv2.flip(img, 1)
    lmList, bboxInfo = detector.findPosition(img, bboxWithHands=True, draw=True)
    if lmList:
        # center = bboxInfo["center"]
        lm11 = lmList[11][1:3]
        lm12 = lmList[12][1:3]
        imgShirt = cv2.imread(os.path.join(shirtFolderPath, listShirts[imgNumber]), cv2.IMREAD_UNCHANGED)

        widthOfShirt = int((lm11[0]-lm12[0]) * fixedRatio)
        imgShirt = cv2.resize(imgShirt, (widthOfShirt, int(widthOfShirt*shirtRatioHeightWidth)))
        currentScale = (lm11[0]-lm12[0])/190
        offset = int(44*currentScale), int(48*currentScale)

        print(widthOfShirt)
        try:
            img = cvzone.overlayPNG(img, imgShirt, (lm12[0]-offset[0], lm12[1]-offset[1]))
        except:
            pass
        
        img = cvzone.overlayPNG(img, imgButtonRight, (1074,293))
        img = cvzone.overlayPNG(img, imgButtonLeft, (72,293))

        if lmList[16][1] < 300:
            counterRight += 1
            cv2.ellipse(img,(139,360), (66,66), 0, 0, counterRight*selectionSpeed, (0,255,0),20)
            if counterRight*selectionSpeed > 360:
                counterRight = 0
                if imgNumber < len(listShirts)-1:
                    imgNumber += 1
                else:
                    imgNumber =0
        elif lmList[15][1] > 900:
            counterLeft += 1
            cv2.ellipse(img,(1138,360), (66,66), 0, 0, counterLeft*selectionSpeed, (0,255,0),20)
            if counterLeft*selectionSpeed > 360:
                counterLeft = 0
                if imgNumber > 0:
                    imgNumber -= 1
                else:
                    imgNumber = len(listShirts)-1
        else:
            counterRight = 0
            counterLeft = 0

    cv2.imshow("Image", img)
    cv2.waitKey(1)
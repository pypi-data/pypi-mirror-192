import cv2
import mediapipe as mp
import time
import math 

class handDetecter():
    def __init__(self,mode=False,maxHands=2,detectionCon=0.5,trackCon=0.5):

        self.mpHandas=mp.solutions.hands
        self.hands= self.mpHandas.Hands(model_complexity=0,min_detection_confidence=0.5,min_tracking_confidence=0.5) 
        self.mpDraw=mp.solutions.drawing_utils

    ############# atha adunaganda ############

    def findHands(self,img,draw=True):   
        imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:  
                if draw:
                    self.mpDraw.draw_landmarks(img,handLms,self.mpHandas.HAND_CONNECTIONS)
        
        return img
    ############# atha adunaganda ############
    ############ position eka gnada ############

    def findPosition(self, img , handNo=0 , draw=True):
        lmlist=[]
        if self.results.multi_hand_landmarks:

            myhand=self.results.multi_hand_landmarks[handNo]

            for id, lm in enumerate(myhand.landmark):
                h,w,c=img.shape 
                cx,cy=int(lm.x*w),int(lm.y*h)
                lmlist.append([id,cx,cy])

                if draw:
                    cv2.circle(img,(cx,cy),15,(255,0,255),cv2.FILLED)

        return lmlist        
    ############# position eka gnada ############
    ############# agiri namana eka adunaganda ####### 

    def fingerPose(self , img, handNo=0 , draw=True):
        self.tipIds = [4,8,12,16,20]

        landMarks=[]
        if self.results.multi_hand_landmarks:

            myhand=self.results.multi_hand_landmarks[handNo]

            for id, lm in enumerate(myhand.landmark):
                h,w,c=img.shape 
                cx,cy,cd=int(lm.x*w),int(lm.y*h),math.sqrt(int(lm.x*w)*int(lm.x*w)+int(lm.y*h)*int(lm.y*h))
                # cx,cy=lm.x,lm.y
                print(id,cx,cy)
                landMarks.append([id,cx,cy,cd])

                if draw:
                    cv2.circle(img,(cx,cy),15,(255,0,255),cv2.FILLED)
        
        self.fingerLandMarkList = []            
        if len(landMarks) !=0: 
            if landMarks[self.tipIds[0]][3] < landMarks[self.tipIds[0]-2][3] :
                self.fingerLandMarkList.append(1)
            else:
                self.fingerLandMarkList.append(0)

            for id in range(1,5):
                if landMarks[self.tipIds[id]][2] < landMarks[self.tipIds[id]-2][2]:
                    self.fingerLandMarkList.append(1)
                else:
                    self.fingerLandMarkList.append(0)


            return self.fingerLandMarkList
    ############# agiri namana eka adunaganda ####### 

# wena thnaka use karadiid handTrackingModule.py eka lin ekak vidihata import karanda eg: 

# import handTrackingModule as htm
# detcter=htm.handDetecter()



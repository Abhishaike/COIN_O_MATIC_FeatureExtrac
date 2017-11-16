from matplotlib import pyplot as plt
import cv2
from PIL import Image
import numpy as np
    
def FindCoin(FileName):
    COIN_IMAGE = cv2.imread(FileName)
    COIN_IMAGE = cv2.resize(COIN_IMAGE, (500, 500))
    COIN_IMAGE_GRAY = cv2.cvtColor(COIN_IMAGE, cv2.COLOR_BGR2GRAY) #make it good for hough circles
    COIN_IMAGE_GRAY = cv2.medianBlur(COIN_IMAGE_GRAY, 21)
    circles = cv2.HoughCircles(COIN_IMAGE_GRAY, cv2.HOUGH_GRADIENT, dp=1.5, minDist = 400)
    if (len(circles[0] == 1)):
        width = int(circles[0][0][0])
        height = int(circles[0][0][1])
        radius = int(circles[0][0][2])

        circle_img = np.zeros((COIN_IMAGE.shape[0], COIN_IMAGE.shape[1]), np.uint8)
        cv2.circle(img=circle_img, center=(height, width), radius=radius, color=255, thickness=-1)

        masked_data = cv2.bitwise_and(COIN_IMAGE, COIN_IMAGE, mask=circle_img)
        masked_data = cv2.cvtColor(masked_data, cv2.COLOR_BGR2RGB)  # convert to normal color
        masked_data = cv2.resize(masked_data, (500, 500))

        return masked_data

    else:
        print(len(circles[0]), "circles were found. Fix parameter selection.")
        return


def SplitIntoConcentric(radius, COIN_IMAGE, Center_Y, Center_X): #height and width should be center_x and center_y
    COIN_IMAGE_GRAYED = cv2.cvtColor(COIN_IMAGE, cv2.COLOR_RGB2GRAY)
    COIN_IMAGE_GRAYED = cv2.medianBlur(COIN_IMAGE_GRAYED, 1)
    gx = cv2.Sobel(COIN_IMAGE_GRAYED, cv2.CV_32F, 1, 0, ksize=1)
    gy = cv2.Sobel(COIN_IMAGE_GRAYED, cv2.CV_32F, 0, 1, ksize=1)
    COIN_IMAGE_GRAYED, angle = cv2.cartToPolar(gx, gy, angleInDegrees=True)
    ret3, COIN_IMAGE_GRAYED = cv2.threshold(COIN_IMAGE_GRAYED, 70, 255, cv2.THRESH_BINARY)
    COIN_IMAGE_GRAYED = COIN_IMAGE_GRAYED.astype(np.uint8)

    AllAngular = []
    Temp =  []
    for K_Rings in [2,4,8,16]: #2,4,8, and 16 rings
        AddedImage = np.zeros((COIN_IMAGE_GRAYED.shape[0], COIN_IMAGE_GRAYED.shape[1]), np.uint8)  # get circle image
        RadDiv = radius*((1/K_Rings)**1/2) * 2
        for NewRad in np.arange(RadDiv, radius + .01, RadDiv):
            NewRad = int(NewRad)
            circle_img = np.zeros((COIN_IMAGE_GRAYED.shape[0], COIN_IMAGE_GRAYED.shape[1]),np.uint8)  # get circle image
            cv2.circle(img=circle_img, center=(Center_Y, Center_X), radius=NewRad, color=255, thickness=-1) #make circle the size of the coin
            ConcentricCircles = cv2.bitwise_and(COIN_IMAGE_GRAYED, COIN_IMAGE_GRAYED, mask=circle_img) #fit mask over coin
            ConcentricCircles = cv2.subtract(ConcentricCircles, AddedImage)
            AddedImage = cv2.add(AddedImage, ConcentricCircles)

            for NewAngle in np.arange(0, 360, 2):
                ellipse_img = np.zeros((COIN_IMAGE_GRAYED.shape[0], COIN_IMAGE_GRAYED.shape[1]), np.uint8)
                cv2.ellipse(img=ellipse_img,
                            center=(Center_Y, Center_X),
                            axes=(radius, radius),
                            angle=0,
                            startAngle=NewAngle,
                            endAngle=NewAngle + 2,
                            color=255,
                            thickness=-1)
                AngleCircles = cv2.bitwise_and(ConcentricCircles, ConcentricCircles, mask=ellipse_img)
                hist = (cv2.calcHist([AngleCircles], [0], None, [2], [0, 256]))[0][0]
                Temp.append(hist)

                im = Image.fromarray(AngleCircles) #used to save segmented image
                FileName = "shit/_FOCUSED" + str(NewRad) + "_" + str(NewAngle)
                im.save(FileName + ".jpg")
        Temp = [i / sum(Temp) for i in Temp]
        Temp = abs(np.fft.fft(Temp))
        AllAngular.extend(Temp)
        Temp = []

return AllAngular


    

import numpy as np
import cv2
import time

def detectMovement(duration):

    cap = cv2.VideoCapture(0)

    fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows = True)

    # Tempo inicial
    start_time = time.time()

    detected = False

    while time.time() - start_time < duration:
        success, img = cap.read()

        # check if we get the frame
        if success == True:
            img = cv2.resize(img, (600, 500))
            cv2.waitKey(30)
            fgmask = fgbg.apply(img)
            _, thresh = cv2.threshold(fgmask.copy(), 180, 255, cv2.THRESH_BINARY)
            # creating a kernel of 4*4
            kernel = np.ones((7, 7), np.uint8)
            # applying errosion to avoid any small motion in video
            thresh = cv2.erode(thresh, kernel)
            # dilating our image
            thresh = cv2.dilate(thresh, None, iterations=6)

            # finding the contours
            contours, heirarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for contour in contours:
                # finding area of contour
                area = cv2.contourArea(contour)
                # print(area)
                # if area greater than the specified value the only then we will consider it
                if area > 1200 and time.time() - start_time > 1:
                    detected = True
                    # find the rectangle co-ordinates
                    x, y, w, h = cv2.boundingRect(contour)
                    # and then dra it to indicate the moving object
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 3)
                    cv2.putText(img, 'MOTION DETECTED', (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                    cv2.imwrite("motionDetection.jpg", img)
            # cv2.imshow('frame',img)
            # cv2.imshow('frame2', thresh)
            if detected:
                break

        else:
            break


    # cap.release()
    # cv2.destroyAllWindows()

    return detected
detectMovement(5)
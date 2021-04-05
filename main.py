from os import stat
import cv2, time
import pandas as pd
from datetime import datetime

first_frame = None

video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
status_list = [None, None]
time_list = []
time_df = pd.DataFrame(columns= ["Motion Start", "Motion End"])

while True:
    check, frame = video.read()
    status = 0

    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_gray = cv2.GaussianBlur(frame_gray, (21, 21), 0)
    
    if first_frame is None:
        first_frame = frame_gray
        continue
    
    frame_delta = cv2.absdiff(first_frame, frame_gray)
    frame_threshold = cv2.threshold(frame_delta, 30, 255, cv2.THRESH_BINARY)[1]
    frame_threshold = cv2.dilate(frame_threshold, None, iterations= 2)
    
    (cnts, _) = cv2.findContours(frame_threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in cnts:
        if cv2.contourArea(contour) < 10000:
            continue
        
        status = 1
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
    
    status_list.append(status)
    status_list = status_list[-2:]
    
    if status_list[-1] == 1 and status_list[-2] == 0:
        time_list.append(datetime.now())
    
    if status_list[-1] == 0 and status_list[-2] == 1:
        time_list.append(datetime.now())    
    
    #cv2.imshow("Gray Frame", frame_gray)
    #cv2.imshow("Delta Frame", frame_delta)
    #cv2.imshow("Threshold Frame", frame_threshold)
    cv2.imshow("Current Frame", frame)

    key = cv2.waitKey(1)
    if key == ord("q"):
        if status == 1:
            time_list.append(datetime.now())
        break
    

for i in range(0, len(time_list), 2):
    time_df = time_df.append({"Motion Start": time_list[i], "Motion End": time_list[i+1]}, ignore_index= True)

time_df.to_csv("motion_detected.csv")    

video.release()  
cv2.destroyAllWindows()
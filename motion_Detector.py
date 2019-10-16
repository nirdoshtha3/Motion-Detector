import cv2,time,pandas
from datetime import datetime
first_frame=None
status_list=[None,None]
times=[]
df=pandas.DataFrame(columns=["Start","End"])
video=cv2.VideoCapture(0)
while(True):
    check,frame=video.read()
    status=0
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray=cv2.GaussianBlur(gray,(21,21),0)
    if first_frame is None:
        first_frame = gray
        continue
    delta_frame = cv2.absdiff(first_frame,gray)
    thresh_delta = cv2.threshold(delta_frame,50,255,cv2.THRESH_BINARY)[1]
    thresh_delta = cv2.dilate(thresh_delta,None, iterations=0)
    (cnts, _) = cv2.findContours(thresh_delta.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for contour in cnts:
        if cv2.contourArea(contour)< 1000:
            continue
        status=1
        (x,y,w,h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0),3)
    status_list.append(status)
    #print(status_list)
    status_list=status_list[-2:]
    #print(status_list)

    if status_list[-1]==1 and status_list[-2]==0:
        times.append(datetime.now())
    if status_list[-1]==0 and status_list[-2]==1:
        times.append(datetime.now())
    
    cv2.imshow('frame',frame)
    cv2.imshow('Capturing',gray)
    cv2.imshow('delta difference frame',delta_frame)
    cv2.imshow('thresh',thresh_delta)
    
    key=cv2.waitKey(1)
    if key==ord('q'):
        break
print(status_list)
print(times)
#store time values in dataframe
for i in range(0,len(times)-1):
    df=df.append({"Start":times[i],"End":times[i+1]},ignore_index=True)
#write the dataframe to a csv file
df.to_csv("D:\\Nirdosh Thakur\\Project\\MotionDetector\\"+"Times.csv")
video.release()
cv2.destroyAllWindows()

import cv2
import os
print(os.getcwd())
face_classifier=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def face_cropped(img):
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces=face_classifier.detectMultiScale(gray, 1.3, 5, minSize=(30,30),flags = cv2.CASCADE_SCALE_IMAGE)
    for (x,y,w,h) in faces:
        face_cropped=img[y:y+h,x:x+w]
    return face_cropped
cap=cv2.VideoCapture(0,cv2.CAP_DSHOW)
img_id=0
while True:
    rate,my_frame=cap.read()
    gray=cv2.cvtColor(my_frame,cv2.COLOR_BGR2GRAY)
    x=face_cropped(my_frame)
    if x is not None:
        img_id+=1
    face=cv2.resize(face_cropped(my_frame),(500,500))
    face=cv2.cvtColor(face,cv2.COLOR_BGR2GRAY)
    file_name=f'data/user{id}.{img_id}.jpg'
    cv2.imwrite(file_name)
    cv2.putText(face,str(img_id),cv2.FONT_HERSHEY_COMPLEX,2,(255,4,0),2)
    cv2.imshow("faces",face)
    if img_id==100:
        break
cap.release()
cv2.destroyAllWindow()
print('done')


#face_cropped()

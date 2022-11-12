from tkinter import *
from PIL import Image, ImageTk
import csv
import cv2
import os
'''
# Create an instance of TKinter Window or frame
win = Tk()

# Set the size of the window
win.geometry("300x250")

# Create a Label to capture the Video frames
label =Label(win)
label.grid(row=0, column=0)
cap= cv2.VideoCapture(0)

# Define function to show frame
def show_frames():
   # Get the latest frame and convert into Image
   cv2image= cv2.cvtColor(cap.read()[1],cv2.COLOR_BGR2RGB)
   img = Image.fromarray(cv2image)
   # Convert image to PhotoImage
   img=img.resize((300,250), Image.ANTIALIAS)
   imgtk = ImageTk.PhotoImage(image = img)
   label.imgtk = imgtk
   label.configure(image=imgtk)
   # Repeat after an interval to capture continiously
   label.after(20, show_frames)

show_frames()
win.mainloop()

'''
print(os.getcwd())
Id,name='1','vishal'
def takeImages():
   cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
   harcascadePath = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
   detector = cv2.CascadeClassifier(harcascadePath)
   sampleNum = 0

   while(True):
      ret, img = cam.read()
      gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
      faces = detector.detectMultiScale(gray, 1.3, 5, minSize=(30,30),flags = cv2.CASCADE_SCALE_IMAGE)
      for(x,y,w,h) in faces:
         cv2.rectangle(img, (x, y), (x+w, y+h), (10, 159, 255), 2)
         sampleNum = sampleNum+1
         #saving the captured face in the dataset folder TrainingImage
         img_name="TrainingImage" + os.sep +name + "."+Id + '.' +str(sampleNum) + ".jpg"
         print(img_name)
         cv2.imwrite(img_name, gray[y:y+h, x:x+w])
         cv2.imshow('frame', img)
         if cv2.waitKey(100) & 0xFF == ord('q'):
            break
         elif sampleNum > 100:
            break
      cam.release()
      cv2.destroyAllWindows()
      res = "Images Saved for ID : " + Id + " Name : " + name
      row = [Id, name]
      with open("StudentDetails"+os.sep+"StudentDetails.csv", 'a+') as csvFile:
         writer = csv.writer(csvFile)
         writer.writerow(row)
      csvFile.close()
takeImages()
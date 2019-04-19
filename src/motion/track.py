import numpy as np
import cv2
from optical_flow import get_gradient

res_x = 466
res_y = 240
grad_thresh = 10


cap = cv2.VideoCapture(0)

_,old_img = cap.read()
old_img = cv2.resize(old_img,(int(res_x),int(res_y)))
old_img = cv2.cvtColor(old_img, cv2.COLOR_BGR2GRAY)

while(True):
    # Capture frame-by-frame
    _,new_img_rgb = cap.read()

    # Our operations on the frame come here
    new_img_rgb = cv2.resize(new_img_rgb,(int(466),int(240)))
    new_img = cv2.cvtColor(new_img_rgb, cv2.COLOR_BGR2GRAY)
    grad =  get_gradient(old_img,new_img,thresh=grad_thresh)

    """
    ## Additional eroding and dilating operations can be used to increase performance maybe
    kernel = np.ones((5,5),np.uint8)
    #erosion = cv2.erode(grad,kernel,iterations = 1)
    #dilation = cv2.dilate(erosion,kernel,iterations = 1)
    """
    # Display the resulting frame
    cv2.imshow('frame',grad)
    
    ## Calculate center of movement by taking the average of points detected by optical flow
    points = np.array(np.where(grad>grad_thresh))
    center_of_movement = np.mean(points,axis=1).astype(int)
    print ("Center of movement:",center_of_movement)
    
    ## If there is any moving object draw a circle around the center of movement point.
    if center_of_movement[0]>0 and center_of_movement[1]>0:
        cv2.circle(new_img_rgb,(center_of_movement[1],center_of_movement[0]), 30, (0,0,255), -1)
    cv2.imshow('moving',new_img_rgb)

    old_img = new_img
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
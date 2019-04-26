import numpy as np
import cv2
from optical_flow import get_gradient

##################################################################
##################################################################
## Kalman filter part
##################################################################
##################################################################
from pykalman import KalmanFilter

## state_dim by state_dim
transition_matrix = [[1, 1, 0, 0],
                     [0, 1, 0, 0],
                     [0, 0, 1, 1],
                     [0, 0, 0, 1]]

## state_
observation_matrix = [[1, 0, 0, 0],
                      [0, 0, 1, 0]]

kf = KalmanFilter(initial_state_mean=np.zeros((4)),
                  transition_matrices=transition_matrix,
                  observation_matrices=observation_matrix)

state_means = np.array([0,0,0,0])
state_covs = np.eye(4)
##################################################################
##################################################################
## Setup camera
##################################################################
##################################################################
res_x = 466//2
res_y = 240//2
grad_thresh = 200

# HSV Values to filter between
filter_low = np.array([0,150,0])
filter_up = np.array([20,255,255])

cap = cv2.VideoCapture(0)

_,old_img = cap.read()
orig_res = old_img.shape
old_img = cv2.resize(old_img,(int(res_x),int(res_y)))
old_img = cv2.cvtColor(old_img, cv2.COLOR_BGR2HSV)
old_img = cv2.inRange(old_img, filter_low, filter_up)

x_loc = res_x/2
y_loc = res_y/2
line_length = orig_res[0]//10

while(True):
    # Capture frame-by-frame
    _,rgb = cap.read()
    rgb = cv2.resize(rgb,(int(res_x),int(res_y)))

    ## Filter and apply mask to gray image
    gray = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(rgb, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, filter_low, filter_up)
    new_img = cv2.bitwise_and(gray,gray, mask= mask)
    
    ## Calculate center of movement by taking the average of points detected by optical flow
    grad =  get_gradient(old_img,new_img,thresh=None)
    points = np.array(np.where(grad>grad_thresh))
    center_of_movement = np.mean(points,axis=1).astype(int)
    
    ## If there is any moving object update the kalman filter and the new x,y location accordingly
    if center_of_movement[0]>0 and center_of_movement[1]>0:
        state_means, state_covs = kf.filter_update(state_means,state_covs,center_of_movement)
        x_loc = state_means[2]
        y_loc = state_means[0]

    ## Draw a line aroung the locations and show image
    x_point = int(x_loc/res_x*0.3*orig_res[1])
    y_point = int(y_loc/res_y*orig_res[0])
    rgb = cv2.resize(rgb,(orig_res[1],orig_res[0]))
    cv2.line(rgb,((x_point,y_point-line_length)),((x_point,y_point+line_length)), (0,255,255), 15)
    #cv2.circle(new_img_rgb,(x_point,y_point), 15, (0,255,255), -1)
    cv2.imshow('moving',rgb)

    old_img = new_img
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
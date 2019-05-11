import numpy as np
import cv2
from motion.optical_flow import get_gradient

from pykalman import KalmanFilter

colors = {'green':[np.array([50,50,20]),np.array([90,255,255])],
          'blue'  :[np.array([100,100,100]),np.array([150,255,255])]}

class Tracker(object):
    def __init__(self,grad_thresh=1,color='green'):
        pos = 1
        vel = 0.3
        acc = 0.3
        transition_matrix = [[pos, vel, 0, 0],
                            [0, acc, 0, 0],
                            [0, 0, pos, vel],
                            [0, 0, 0, acc]]

        ## state_
        observation_matrix = [[1, 0, 0, 0],
                            [0, 0, 1, 0]]

        self.kf = KalmanFilter(initial_state_mean=np.zeros((4)),
                        transition_matrices=transition_matrix,
                        observation_matrices=observation_matrix)

        self.state_means = np.array([0,0,0,0])
        self.state_covs = np.eye(4)
        self.grad_thresh = grad_thresh

        # HSV Values to filter between
        self.filter_low = colors[color][0]
        self.filter_up = colors[color][1]

        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT,240)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,320)

        _,old_img = self.cap.read()
        self.orig_res = old_img.shape
        
        ## old version resize in opencv
        #self.res_x = 300
        #self.res_y = 300
        #old_img = cv2.resize(old_img,(int(self.res_x),int(self.res_y)))
        
        ## new version hardware capture with 240,320 resolution
        self.res_y,self.res_x,ch = old_img.shape

        old_img = cv2.cvtColor(old_img, cv2.COLOR_BGR2HSV)
        self.old_img = cv2.inRange(old_img, self.filter_low, self.filter_up)
        
        self.x_loc = 0.5
        self.y_loc = 0.5
        self.line_length = self.orig_res[0]//3

    def track(self,show=True):
        _,rgb = self.cap.read()
        rgb = cv2.resize(rgb,(int(self.res_x),int(self.res_y)))
        ## Filter and apply mask to gray image
        gray = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(rgb, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.filter_low, self.filter_up)
        area = np.sum(mask)
        new_img = cv2.bitwise_and(gray,gray, mask= mask)
        grad = get_gradient(self.old_img,new_img,thresh=self.grad_thresh)
        moved_ratio = np.sum(grad)/area

        points = np.array(np.where(grad>0))
        center_of_movement = np.maximum([0,0],np.mean(points,axis=1).astype(int))
        
        if (center_of_movement[0]>0 and center_of_movement[1]>0 and area > 0 and moved_ratio > 0.25):
            self.state_means, self.state_covs = self.kf.filter_update(self.state_means,self.state_covs,center_of_movement)
            self.x_loc = self.state_means[2]/self.res_x
            self.y_loc = self.state_means[0]/self.res_y

        self.old_img = new_img
    
    def __del__(self):
        # When everything done, release the capture
        self.cap.release()
        cv2.destroyAllWindows()

if __name__=="__main__":
    tracker  = Tracker()
    while True:
        tracker.track()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

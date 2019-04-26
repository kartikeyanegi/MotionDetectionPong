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

##################################################################
##################################################################
#game code

import pygame

### Colors
WHITE = (255, 255, 255)
BLACK = (0,0,0)

### Constants
W = 800
H = 600
pygame.font.init()
comic = pygame.font.SysFont('Comic Sans MS', 30)

### Variables
wt = 2
mplay = False

p1x = W/30
p1y = H/2 - ((W/60)**2)/2

p2x = W-(W/30)
p2y = H/2 - ((W/60)**2)/2

p1score = 0
p2score = 0

w_p = False
s_p = False
wsr = False
u_p = False
d_p = False
udr = False

dm = H/40

paddle_width = W/60
paddle_height = 100

bsd = 10

bx = W/2
by = H/2
bw = W/65
bxv = H/60
bxv = -bxv
byv = 0

### Functions
def drawpaddle(x, y, w, h):
    pygame.draw.rect(screen, WHITE, (x, y, w, h))

def drawball(x, y):
    pygame.draw.circle(screen, WHITE, (int(x), int(y)), int(bw))

def uploc():
    global p1y
    global bigy
    global p2y
    if w_p:
        if bigy-(dm) < 0:
            bigy = 0
        else:
            bigy -= dm
    elif s_p:
        if bigy+(dm)+paddle_height > H:
            bigy = H-paddle_height
        else:
            bigy += dm
    if u_p:
        if bigy-(dm) < 0:
            bigy = 0
        else:
            bigy -= dm
    elif d_p:
        if bigy+(dm)+paddle_height > H:
            bigy = H-paddle_height
        else:
            bigy += dm

def upblnv():
    global bx
    global bxv
    global by
    global byv
    global p2score
    global p1score
    

    if (bx+bxv < p1x+paddle_width) and (( bigy< by+byv+bw) and (by+byv-bw < bigy+paddle_height)):
        bxv = -bxv
        byv = ((bigy+(bigy+paddle_height))/2)-by
        byv = -byv/((5*bw)/7)
    elif bx+bxv < 0:
        p2score += 1
        bx = W/2
        bxv = H/60
        by = H/2
        byv = 0
    if (bx+bxv > p2x) and ((bigy < by+byv+bw) and (by+byv-bw < bigy+paddle_height)):
        bxv = -bxv
        byv = ((bigy+(bigy+paddle_height))/2)-by
        byv = -byv/((5*bw)/7)
    elif bx+bxv > W:
        p1score += 1
        bx = W/2
        bxv = -H/60
        by = H/2
        byv = 0
    if by+byv > H or by+byv < 0:
        byv = -byv

    bx += bxv
    by += byv

def drawscore():
    score = comic.render(str(p1score) + " - " + str(p2score), False, WHITE)
    screen.blit(score, (W/2,30))

### Initialize
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption('Snake ML v.1.0.0')
screen.fill(BLACK)
pygame.display.flip()



##################################################################
##################################################################



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

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_w:
                w_p = True
                if s_p == True:
                    s_p = False
                    wsr = True
            if event.key == pygame.K_s:
                s_p = True
                if w_p == True:
                    w_p = False
                    wsr = True
            if event.key == pygame.K_UP:
                u_p = True
                if d_p == True:
                    d_p = False
                    udr = True
            if event.key == pygame.K_DOWN:
                d_p = True
                if u_p == True:
                    u_p = False
                    udr = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                w_p = False
                if wsr == True:
                    s_p = True
                    wsr = False
            if event.key == pygame.K_s:
                s_p = False
                if wsr == True:
                    w_p = True
                    wsr = False
            if event.key == pygame.K_UP:
                u_p = False
                if udr == True:
                    d_p = True
                    udr = False
            if event.key == pygame.K_DOWN:
                d_p = False
                if udr == True:
                    u_p = True
                    udr = False

    screen.fill(BLACK)
    bigy=y_loc*5
    uploc()
    upblnv()
    drawscore()
    drawball(bx, by)
    drawpaddle(p1x, bigy, paddle_width, paddle_height)
    drawpaddle(p2x, bigy, paddle_width, paddle_height)
    pygame.display.flip()
    pygame.time.wait(wt)

    old_img = new_img
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    


# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
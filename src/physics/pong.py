import pygame

class Game(object):
    def __init__(self):
        ### Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (30,137,6)
        self.RED = (229, 17, 46)
        self.BLUE = (9, 79, 187)
        self.ORANGE = (243, 161, 18)

        ### Constants
        self.W = 600
        self.H = 300
        pygame.font.init()
        self.comic = pygame.font.SysFont('Comic Sans MS', 30)

        ### Variables
        self.wt = 2 ## wait time
        self.p1x = self.W/30
        self.p1y = self.H/2 - ((self.W/60)**2)/2

        self.p2x = self.W-(self.W/30)
        self.p2y = self.H/2 - ((self.W/60)**2)/2

        self.p1score = 0
        self.p2score = 0

        self.dm = self.H/40

        self.paddle_width = self.W/60
        self.paddle_height = self.H/4

        self.bsd = 10
        
        self.bw = self.W/65
        self.vely = ((5*self.bw)/7)
        self.velx = 20
        self.bx = self.W/2
        self.by = self.H/2
        
        self.bxv = -self.velx
        self.byv = 0
        

        ### Initialize
        self.screen = pygame.display.set_mode((self.W, self.H))
        pygame.display.set_caption('Hand Pong v0.0.1 beta')
        self.screen.fill(self.BLACK)
        pygame.display.flip()
        self.running = True
        
<<<<<<< HEAD
    def opponent(self, data):
        y_loc2 = float(data['data'])
        self.p2y=self.H*y_loc2-self.paddle_height/2

    def update(self,y_loc1):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        self.screen.fill(self.BLACK)
        self.p1y=self.H*y_loc1-self.paddle_height/2
        self.upblnv()
        self.drawscore()
        self.drawball()
        self.drawpaddle(self.p1x, self.p1y, self.paddle_width, self.paddle_height)
        self.drawpaddle(self.p2x, self.p2y, self.paddle_width, self.paddle_height)
        pygame.display.flip()
        pygame.time.wait(self.wt)
=======
    def get_screen(self):
        return self.screen

    def update(self,y_loc1,y_loc2):
        if self.running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.running = False
            self.drawbg()
            self.p1y=self.H*y_loc1-self.paddle_height/2
            self.p2y=self.H*y_loc2-self.paddle_height/2
            self.upblnv()
            self.drawscore()
            self.drawball()
            self.drawpaddle(self.p1x, self.p1y, self.paddle_width, self.paddle_height, self.RED)
            self.drawpaddle(self.p2x, self.p2y, self.paddle_width, self.paddle_height, self.BLUE)
            pygame.display.flip()
            pygame.time.wait(self.wt)
        else:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.running = True
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit()
>>>>>>> dbcd45aecacdd7d9eb852ead204371d334d70a49

    ### Drawing Functions
    def drawbg(self):
        self.screen.fill(self.BLACK)
        pygame.draw.rect(self.screen, self.WHITE, (self.W/2, 0, 10, self.H))

    def drawpaddle(self,x, y, w, h, color):
        pygame.draw.rect(self.screen, color, (x, y, w, h))

    def drawball(self):
        pygame.draw.circle(self.screen, self.ORANGE, (int(self.bx), int(self.by)), int(self.bw))

    def upblnv(self):
        if (self.bx+self.bxv < self.p1x+self.paddle_width) and (( self.p1y< self.by+self.byv+self.bw) and (self.by+self.byv-self.bw < self.p1y+self.paddle_height)):
            self.bxv = -self.bxv
            self.byv = ((self.p1y+(self.p1y+self.paddle_height))/2)-self.by
            self.byv = -self.byv/self.vely
        elif self.bx+self.bxv < 0:
            self.p2score += 1
            self.bx = self.W/2
            self.bxv = self.velx
            self.by = self.H/2
            self.byv = 0
        if (self.bx+self.bxv > self.p2x) and ((self.p2y < self.by+self.byv+self.bw) and (self.by+self.byv-self.bw < self.p2y+self.paddle_height)):
            self.bxv = -self.bxv
            self.byv = ((self.p2y+(self.p2y+self.paddle_height))/2)-self.by
            self.byv = -self.byv/self.vely
        elif self.bx+self.bxv > self.W:
            self.p1score += 1
            self.bx = self.W/2
            self.bxv = -self.velx
            self.by = self.H/2
            self.byv = 0
        if self.by+self.byv > self.H or self.by+self.byv < 0:
            self.byv = -self.byv

        self.bx += self.bxv
        self.by += self.byv

    def drawscore(self):
<<<<<<< HEAD
        score = self.comic.render(str(self.p1score) + " - " + str(self.p2score), False, self.WHITE)
        self.screen.blit(score, (self.W/2,30))
=======
        string  = str(self.p1score) + "    " + str(self.p2score)
        score = self.comic.render(string, False, self.WHITE)
        position = self.W/2 - score.get_width()/2.5
        self.screen.blit(score, (position, 30))
>>>>>>> dbcd45aecacdd7d9eb852ead204371d334d70a49

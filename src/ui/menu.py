import pygame
import sys

class Menu(object):
    def __init__(self, screen, pubsub):
        self.screen = screen
        pygame.font.init()
        self.text_format = pygame.font.SysFont('Comic Sans MS', 30)
        self.screen_width = 600
        self.H = 300
        self.pubsub = pubsub

    def get_running(self):
        return self.running

    def main_menu(self):
        # Colors
        white=(255, 255, 255)
        black=(0, 0, 0)
        gray=(50, 50, 50)
        red=(255, 0, 0)
        green=(0, 255, 0)
        blue=(0, 0, 255)
        yellow=(255, 255, 0)

        menu=True
        selected="start"
     
        while menu:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_UP:
                        selected="start"
                    elif event.key==pygame.K_DOWN:
                        selected="quit"
                    if event.key==pygame.K_RETURN:
                        if selected=="start":
                            print("Start")
                            menu = False
                        if selected=="quit":
                            pygame.quit()
                            self.pubsub.unsubscribe()
                            sys.exit()
     
            # Main Menu UI
            self.screen.fill(blue)
            title = self.text_format.render("Ping-pong Game", False, yellow)
            title2 = self.text_format.render("Press space to pause/continue", False, yellow)
            if selected=="start":
                text_start = self.text_format.render("START", False, white)
            else:
                text_start = self.text_format.render("START", False, black)
            if selected=="quit":
                text_quit = self.text_format.render("QUIT", False, white)
            else:
                text_quit = self.text_format.render("QUIT", False, black)
     
            title_rect=title.get_rect()
            title_rect2=title2.get_rect()
            start_rect=text_start.get_rect()
            quit_rect=text_quit.get_rect()
     
            # Main Menu Text
            self.screen.blit(title, (self.screen_width/2 - (title_rect[2]/2), 30))
            self.screen.blit(title2, (self.screen_width/2 - (title_rect2[2]/2), 70))
            self.screen.blit(text_start, (self.screen_width/2 - (start_rect[2]/2), 150))
            self.screen.blit(text_quit, (self.screen_width/2 - (quit_rect[2]/2), 200))
            pygame.display.update()
            # clock.tick(FPS)
            pygame.display.set_caption("Python - Pygame Simple Main Menu Selection")

from physics.pong import Game
from motion.track import Tracker
from ui.menu import Menu

player  = Tracker(color='blue')
#p2  = Tracker(color='green')
game = Game()
screen = game.get_screen()
menu = Menu(screen)

menu.main_menu()

while True:
    player.track(show=False)
    #opponent = read()
    #send(player.y_loc)
    game.update(player.y_loc,0.0)
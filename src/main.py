from physics.pong import Game
from motion.track import Tracker
from server.run import Server
from ui.menu import Menu

player  = Tracker(color='blue')
#p2  = Tracker(color='green')
game = Game()
s = Server(handler=game.opponent, host="localhost", sender="player1", receiver="player2")
screen = game.get_screen()
menu = Menu(screen)

menu.main_menu()

while True:
    player.track(show=False)
    s.send(player.y_loc)
    #send(player.y_loc)
    game.update(player.y_loc)

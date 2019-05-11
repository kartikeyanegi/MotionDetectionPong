from physics.pong import Game
from motion.track import Tracker
<<<<<<< HEAD
from server.run import Server
=======
from ui.menu import Menu
>>>>>>> dbcd45aecacdd7d9eb852ead204371d334d70a49

player  = Tracker(color='blue')
#p2  = Tracker(color='green')
game = Game()
<<<<<<< HEAD
s = Server(handler=game.opponent, host="localhost", sender="player1", receiver="player2")
=======
screen = game.get_screen()
menu = Menu(screen)
>>>>>>> dbcd45aecacdd7d9eb852ead204371d334d70a49

menu.main_menu()

while True:
    player.track(show=False)
    s.send(player.y_loc)
    #send(player.y_loc)
<<<<<<< HEAD
    game.update(player.y_loc)
=======
    game.update(player.y_loc,0.0)
>>>>>>> dbcd45aecacdd7d9eb852ead204371d334d70a49

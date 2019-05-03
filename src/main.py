from physics.pong import Game
from motion.track import Tracker
from server.run import Server

player  = Tracker(color='blue')
#p2  = Tracker(color='green')
game = Game()
s = Server(host="localhost", topic="player1")

while game.running:
    player.track(show=False)
    s.send(player.y_loc)
    #opponent = read()
    #send(player.y_loc)
    game.update(player.y_loc,opponent)

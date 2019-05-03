from physics.pong import Game
from motion.track import Tracker

player  = Tracker(color='blue')
#p2  = Tracker(color='green')
game = Game()

while game.running:
    player.track(show=False)
    #opponent = read()
    #send(player.y_loc)
    game.update(player.y_loc,opponent)
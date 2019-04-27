from physics.pong import Game
from motion.track import Tracker

tracker  = Tracker(grad_thresh=200)
game = Game()

while game.running:
    tracker.track(show=True)
    game.update(tracker.y_loc)
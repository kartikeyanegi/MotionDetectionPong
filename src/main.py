import argparse
import sys
from physics.pong import Game
from motion.track import Tracker
from server.run import Server
from ui.menu import Menu


parser = argparse.ArgumentParser(description="Pong game")
parser.add_argument("--host", help="Host IP of the server", default="localhost")
parser.add_argument("--sender", help="Your username. It should be the same on their receiver end")
parser.add_argument("--receiver", help="Your friend's username. It should be the same on their sender end")
args = parser.parse_args()
if args.sender == None or args.receiver == None:
    print("Please enter sender and receiver username")
    sys.exit(1)


def main():
    player  = Tracker(color='blue')
    game = Game(flag=False)
    s = Server(handler=game.opponent, host=args.host, sender=args.sender, receiver=args.receiver)
    screen = game.get_screen()
    menu = Menu(screen)
    menu.main_menu()

    while True:
        player.track(show=False)
        s.send(player.y_loc)
        game.update(player.y_loc)

if __name__ == "__main__":
    main()

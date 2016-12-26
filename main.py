import sys
from player import player
from system import system

def main(filename,pattern):

	player1=player()
	player2=player()
	player1.change_turn(1)
	game=system()
	time,shot=game.get_input(filename,pattern)
	game.control_system(player1,player2,shot)

main(sys.argv[1],pattern = ' ')

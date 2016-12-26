class player :
	
	def __init__(self):
		self.status=0
		self.turn=0
		self.score=0
		self.game_win_count=0
		self.set_win_count=0
		self.advantage=0
		self.tie_break_count=0
	def change_turn(self,turn) :
		self.turn=turn

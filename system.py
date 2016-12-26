import re

class system:

	def __sort_input(self,time,shot):
		for i in range(len(time)):
			smallest=i
			for j in range(i,len(time)):
				if(int(time[j])<int(time[smallest])):
					smallest=j
					temp=int(time[i])
					time[i]=int(time[smallest])
					time[smallest]=int(temp)
					temp=int(shot[i])
					shot[i]=int(shot[smallest])
					shot[smallest]=int(temp)
		return time,shot
	
	def __set_status(self,player1,player2,status) :
		if(player1.turn) :
			player1.status=status
		elif(player2.turn) :
			player2.status=status
	
	def __get_shot(self,iteration,shot) :
		return shot[iteration]

	def __set_score(self,player1,player2,win) :
		if not self.__check_tie_break(player1,player2):
			if not self.__check_deuce(player1,player2):
				if(player1.turn and win) :
					if(player1.score<30) :
						player1.score+=15
					elif(player1.score>=30) :
						player1.score+=10
				elif(player2.turn and win) :
					if(player2.score<30) :
						player2.score+=15
					elif(player2.score>=30) :
						player2.score+=10
				elif(player1.turn and not win) :
					if(player2.score<30) :
						player2.score+=15
					elif(player1.score>=30) :
						player2.score+=10
				elif(player2.turn and not win) :
					if(player1.score<30) :
						player1.score+=15
					elif(player1.score>=30) :
						player1.score+=10
			else:
				if(player1.turn and win) :
					player1.advantage+=1
					player2.advantage=0
				elif(player2.turn and win) :
					player1.advantage=0
					player2.advantage+=1
				elif(player1.turn and  not win) :
					player1.advantage=0
					player2.advantage+=1
				elif(player2.turn and not win) :
					player1.advantage+=1
					player2.advantage=0
		else :
			if(not player1.turn and not win) :
				player1.tie_break_count+=1	
			elif(not player2.turn and not win) :
				player2.tie_break_count+=1
	
	def __check_deuce(self,player1,player2):
		if(player1.score==player2.score==40):
			return 1
		else:
			return 0
	
	def __change_player_turns(self,player1,player2) :
		if(player1.turn) :
			player1.change_turn(0)
			player2.change_turn(1)
		elif(player2.turn) :
			player1.change_turn(1)
			player2.change_turn(0)
	
	def __check_tie_break(self,player1,player2):
		if(player1.game_win_count==player2.game_win_count==6):
			return 1;
		else:
			return 0;
	
	def __check_set_point(self,player1,player2):
		if not self.__check_tie_break(player1,player2):
			if(player1.game_win_count==6):
				player1.game_win_count=0
				player2.game_win_count=0
				player1.set_win_count+=1
			elif(player2.game_win_count==6):
				player1.game_win_count=0
				player2.game_win_count=0
				player1.set_win_count+=1
		else:
			if(player1.tie_break_count>=7 and player1.tie_break_count-player2.tie_break_count==2):
				player1.tie_break_count=0
				player2.tie_break_count=0
				player1.set_win_count+=1
			elif(player2.tie_break_count>=7 and player2.tie_break_count-player1.tie_break_count==2):
				player1.tie_break_count=0
				player2.tie_break_count=0
				player2.set_win_count+=1
	
	def __check_game_point(self,player1,player2) :
		if not self.__check_deuce(player1,player2):
			if(player1.score>40) :
				player1.score=0
				player2.score=0
				player1.game_win_count+=1
			elif(player2.score>40) :
				player1.score=0
				player2.score=0
				player2.game_win_count+=1
		else:
			if player1.advantage==2:
				player1.score=0
				player2.score=0
				player1.advantage=0
				player1.game_win_count+=1
			elif player2.advantage==2:	
				player1.score=0
				player2.score=0
				player2.advantage=0
				player2.game_win_count+=1
	
	def __change_serve_turns(self,player1,player2):
		if((player1.game_win_count+player2.game_win_count)%2==0):
			player1.change_turn(1)
			player2.change_turn(0)
		else:
			player1.change_turn(0)
			player2.change_turn(1)
	
	def __check_win(self,player1,player2):
		if(player1.set_win_count==3 or player2.set_win_count==3):
			exit(0)

	def __print_output(self,iteration,player1,player2) :
		print 'Iteration: '+str(iteration)
		if(player1.turn) :
			print 'Player1 : '+ str(player1.status)
		elif(player2.turn) :
			print 'Player2 : '+ str(player2.status)
		if(self.__check_deuce(player1,player2)):
			print '***In Deuce***'
		print "P1 Score "+ str(player1.score)
		if(player1.advantage==1):
			print '***Player1 in Advantage***'
		print "P2 Score "+ str(player2.score)
		if(player2.advantage==1):
			print '***Player2 in Advantage***'
		print "P1 Game Win Count "+ str(player1.game_win_count)
		print "P2 Game Win Count "+ str(player2.game_win_count)
		print "P1 Set Win Count "+ str(player1.set_win_count)
		print "P2 Set Win Count "+ str(player2.set_win_count)
		print
	
	def get_input(self,filename,pattern):
		opened_file=open(filename,'r')
		lines = opened_file.readlines()
		time=[]
		shot=[]
		
		for line in lines :
			time.append(re.split(pattern,line)[0])
			shot.append(re.split(pattern,line)[1])
		time,shot=self.__sort_input(time,shot)
		return time,shot	

	def control_system(self,player1,player2,shot) :
		for i in range(len(shot)) :
			status=self.__get_shot(i,shot)
			if(re.match('Serve',status)!=None) :
				self.__change_serve_turns(player1,player2)
			elif(re.match('Fault',status)!=None) :
				self.__set_score(player1,player2,0)
			elif(re.match('Ace',status)!=None):
				self.__set_score(player1,player2,1)
			elif(re.match('Backhand',status)!=None or re.match('Forehand',status)!=None)	:
				self.__change_player_turns(player1,player2)
			elif(re.match('PointLost',status)!=None) :
				self.__set_score(player1,player2,0)
			self.__set_status(player1,player2,status)
			self.__check_game_point(player1,player2)
			self.__check_set_point(player1,player2)
			self.__print_output(i+1,player1,player2)
			self.__check_win(player1,player2)

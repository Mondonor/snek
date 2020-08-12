import pygame

import random
from random import seed
from random import randint

from enum import Enum

class Position:
	def __init__(self, x, y):
		self.x = x
		self.y = y

class Color():
	def __init__(self):
		self.WHITE = (255, 255, 255)
		self.RED = (255, 0, 0)
		self.GREEN = (0, 255, 0)

class Game:
	def __init__(self, display):
		self.display = display
		self.font1 = pygame.font.Font('freesansbold.ttf', 8)
		self.font2 = pygame.font.Font('freesansbold.ttf', 20)
		self.IN_PLAY = True
		self.PAUSE = False
		self.END_SUCCESS = False
		self.position = Position(40,40)
		self.food = Position(240,260)		
		self.score = 0
		self.prestige = 0
		self.velocity = 20
		self.rate = 17
		self.length = 1
		self.countcond = 10
		self.level = 1
		self.memlist = [[]]*103
		self.colors = Color()
	
	def dispTEXT(self):
		score_board = self.font1.render(f'SCORE: {self.score}  PRESTIGE: {self.prestige}', True, self.colors.WHITE)
		score_board_rect = score_board.get_rect()
		score_board_rect.center = (80, 8)
		self.display.blit(score_board, score_board_rect)

	def PauseScreen(self):
		pause = self.font2.render("Press 'u' to unpause.", True, self.colors.WHITE)
		pause_rect = pause.get_rect()
		pause_rect.center = (250, 250)
		self.display.blit(pause, pause_rect)
		pygame.display.update()
	
	def winScreen(self):
		congrats = self.font2.render('Congratulations, you beat the game!', True, self.colors.GREEN)
		replay = self.font2.render("To play again, press 'space'. To quit, press 9.", True, self.colors.GREEN)
		congrats_rect = congrats.get_rect()
		replay_rect = replay.get_rect()
		congrats_rect.center = (250 , 175)
		replay_rect.center = (250 , 225)
		self.display.blit(congrats, congrats_rect)
		self.display.blit(replay, replay_rect)

	def loseScreen(self):
		lightning = self.font2.render("You are as likely to be struck by lightning", True, self.colors.RED)
		dreams = self.font2.render("as you are to achieve your dreams.", True, self.colors.RED)
		replay = self.font2.render("Try again with space, 9 to quit.", True, self.colors.RED)
		lightning_rect = lightning.get_rect()
		dreams_rect = dreams.get_rect()
		replay_rect = replay.get_rect()
		lightning_rect.center = (250 , 150)
		dreams_rect.center = (250 , 250)
		replay_rect.center = (250 , 350)
		self.display.blit(lightning, lightning_rect)
		self.display.blit(dreams, dreams_rect)
		self.display.blit(replay,replay_rect)

	def wincond(self):
		self.IN_PLAY = True
		self.END_SUCCESS = False

	def losecond(self):
		self.END_SUCCESS = False

	def eat(self):
		if self.score == 100:
			self.wincond()
		self.length+=1
		self.memlist[self.length-1] = [self.position.x , self.position.y]
		self.food.x = randint(1,24) * 20
		self.food.y = randint(1,24) * 20
		while [self.food.x,self.food.y] in self.memlist:
			self.food.x = randint(1,24) * 20
			self.food.y = randint(1,24) * 20
		self.score+=1
		if self.score%10 == 0:
			self.level+=1
			self.rate=self.rate-1
		if self.score % 20 == 0:
			self.countcond=self.countcond-1

	def move(self, dire):
		if dire == "R":
			if self.position.x >= 480:
				self.losecond()
			else:
				self.position.x += self.velocity
		elif dire == "L":
			if self.position.x <= 0:
            			self.losecond()
			else:
				self.position.x -= self.velocity
		elif dire == "U":
			if self.position.y <= 0:
				self.losecond()
			else:
				self.position.y -= self.velocity
		elif dire == "D":
			if self.position.y >= 480:
				self.losecond()
			else:
				self.position.y += self.velocity

		for i in range(self.length):
			if i == self.length - 1:
				self.memlist[0] = [self.position.x,self.position.y]
			else:
				self.memlist[self.length - i - 1] = self.memlist[self.length - i - 2]
		self.collcheck()

	def collcheck(self):
		for i in range(self.length):
			if self.memlist[0] == self.memlist[i] and i != 0:
            			self.losecond()



def main():
	pygame.init()
	display = pygame.display.set_mode((500,500))
	pygame.display.set_caption("Snek :)")
	snek = Game(display)
	
	ACTIVE = True

	snek.memlist[0] = [snek.position.x,snek.position.y]
	
	count = -5
	dire = "R"
	diretemp = "R"
	
	while ACTIVE:
		pygame.time.delay(snek.rate)


		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				ACTIVE = False
		keys = pygame.key.get_pressed()

		if keys[pygame.K_p]:
			snek.IN_PLAY = False
			snek.PAUSE = True
			snek.PauseScreen()
	    
		if keys[pygame.K_u]:
			snek.IN_PLAY = True
			snek.PAUSE = False

		if snek.PAUSE == True:
			continue
	    
		if snek.IN_PLAY == True:
			if keys[pygame.K_LEFT]:
				if dire == "R":
					pass
				else:
					diretemp = "L"
			if keys[pygame.K_RIGHT]:
				if dire == "L":
					pass
				else:
					diretemp = "R"
			if keys[pygame.K_UP]:
				if dire == "D":
					pass
				else:
					diretemp = "U"
			if keys[pygame.K_DOWN]:
				if dire == "U":
					pass
				else:
					diretemp = "D"
	    
			if  count <= snek.countcond:
					count = count + 1
			else:
				if snek.memlist[0][0] == snek.food.x and snek.memlist[0][1] == snek.food.y:
					snek.eat()
				dire = diretemp
				snek.move(dire)
				count = 1
		  
			snek.display.fill((0,0,0))
			snek.dispTEXT()
			pygame.draw.rect(snek.display, (255,255,255), (snek.food.x + 4, snek.food.y + 4,10,10))
		
			for i in range(snek.length):
				if i <= 10:
					A = 255 - 10 * i
					B = 0
					C = 10 * i
				elif i > 10 and i <= 20:
					A = 155 - 5 * (i - 10)
					B = 5 * (i - 10)
					C = 100
				elif i > 20 and i <= 30:
					A = 105 + (i - 20) * 2
					B = 50 + (i - 20) * 10
					C = 100 + (i - 20) * 10
				elif i > 30 and i <= 50:
					A = 125 - (i - 30) * 5
					B = 150 + (i - 30) * 5
					C = 200 + (i - 30) * 1
				elif i > 50 and i <= 70:
					A = 24 + (i - 50) * 9
					B = 244 - (i - 50) * 2
					C = 224 - (i - 50)
				else:
					A = 204 + (i - 70)
					B = A
					C = A
				pygame.draw.rect(snek.display, (A,B,C), (snek.memlist[i][0],snek.memlist[i][1], 18, 18))
		    
		elif snek.END_SUCCESS == True:
			snek.winScreen()
		else:
			snek.loseScreen()

		keys = pygame.key.get_pressed()
		if keys[pygame.K_y]:
			snek.losecond()
		elif keys[pygame.K_z]:
			snek.wincond()
	    
		pygame.display.update()
		    
		keys = pygame.key.get_pressed()
		if snek.IN_PLAY == False:
			if keys[pygame.K_9]:
				quit()
			if keys[pygame.K_SPACE]:
				display = pygame.display.set_mode((500,500))
				pygame.display.set_caption("Snek :)")
				snek = game(display)

				snek.memlist[0] = [snek.position.x,snek.position.y]
				count = -5
	pygame.quit()

main()

import pygame
from pygame.locals import *

class Pong(object):
	"""docstring for Pong"""
	def __init__(self, screensize):

		self.screensize = screensize
		self.centerx = int(screensize[0]*0.5)
		self.centery = int(screensize[1]*0.5)

		self.radius = 8

		self.rect = pygame.Rect(self.centerx-self.radius,
								self.centery-self.radius,
								self.radius*2, self.radius*2)

		self.color = (100, 100, 255)
		self.direction = [1, 1]

		self.speed = 2

		self.hit_edge_left = False
		self.hit_edge_right = False
	def update(self, player_paddle=None, ai_paddle=None):

		self.centerx += self.direction[0]*self.speed
		self.centery += self.direction[1]*self.speed

		self.rect.center = (self.centerx, self.centery)

		if self.rect.top <= 0:
			self.direction[1] = 1
		elif self.rect.bottom >= self.screensize[1]-1:
			self.direction[1] = -1

		if self.rect.right >= self.screensize[1]-1:
			self.hit_edge_right = True
		elif self.rect.left <= 0:
			self.hit_edge_left = True

	def render(self, screen):
		pygame.draw.circle(screen, self.color, self.rect.center, self.radius, 0)
		pygame.draw.circle(screen, (0, 0, 0), self.rect.center, self.radius, 1)


def main():
	pygame.init()

	screensize = (640, 480)
	screen = pygame.display.set_mode(screensize)
	clock = pygame.time.Clock()

	pong = Pong(screensize)

	running = True

	while running:
		#FPS limiting/reporting phase
		clock.tick(64)

		#event handling phase
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False

		#object updating phase
		pong.update()
		

		if pong.hit_edge_left:
			print ("You Won")
			running = False
		elif pong.hit_edge_right:
			print ("You Lose")
			running = False
		
		#rendering phase
		screen.fill((100, 100, 100))

		pong.render(screen)

		pygame.display.flip()

	pygame.quit()

main()

import pygame
import random
from pygame.locals import *
import time

SIZE = 40
BACKGROUND = (0, 154, 23)

class Food:
	#load food sprite
	def __init__(self, playground):
		self.playground = playground
		self.food = pygame.image.load("assets/food.png")
		self.x = self.y = 400
		self.food = pygame.transform.scale(self.food, (40, 40))

	#display food
	def draw(self):
		self.playground.blit(self.food, (self.x , self.y))
		pygame.display.flip()

	#randomly spawn food
	def move(self):
		self.x = random.randint(0, 23)*SIZE
		self.y = random.randint(0, 18)*SIZE

class Snake:
	#load snake sprite
	def __init__(self, playground, length):
		self.length = length
		self.playground = playground
		self.snake = pygame.image.load("assets/snake1.png")
		self.x = [SIZE]*length
		self.y = [SIZE]*length
		self.snake = pygame.transform.scale(self.snake, (40, 40))
		self.direction = 'right'

	def increase_length(self):
		self.length += 1
		self.x.append(-1)
		self.y.append(-1)

	#display snake 
	def draw(self):
		self.playground.fill(BACKGROUND)
		for i in range(self.length):
			self.playground.blit(self.snake, (self.x[i], self.y[i]))
		pygame.display.flip()

	def move(self):
		for i in range(self.length-1, 0, -1):
			self.x[i] = self.x[i - 1]
			self.y[i] = self.y[i - 1]

		if self.direction == 'up':
			self.y[0] -= SIZE
		if self.direction == 'down':
			self.y[0] += SIZE
		if self.direction == 'left':
			self.x[0] -= SIZE
		if self.direction == 'right':
			self.x[0] += SIZE

		print("{} {}".format(self.x[0], self.y[0]))

		self.draw()

	def move_left(self):
		if self.direction != 'right':
			self.direction = 'left'

	def move_right(self):
		if self.direction != 'left':
			self.direction = 'right'

	def move_up(self):
		if self.direction != 'down':
			self.direction = 'up'

	def move_down(self):
		if self.direction != 'up':
			self.direction = 'down'

class Game:
	def __init__(self):
		pygame.init()

		pygame.display.set_caption('Snake')

		self.playground = pygame.display.set_mode((1000, 800))
		self.playground.fill(BACKGROUND)

		self.snake = Snake(self.playground, 1)
		self.snake.draw()

		self.food = Food(self.playground)
		self.food.draw()

	def display_score(self):
		font = pygame.font.SysFont('arial', 30)
		score = font.render(f"Score: {self.snake.length-1}", True, (255, 255, 255))
		self.playground.blit(score, (800, 10))

	def is_collision(self, x1, y1, x2, y2):
		if x1 >= x2 and x1 < x2+SIZE:
			if y1 >= y2 and y1 < y2+SIZE:
				return True

		return False

	def collides_border(self, x, y):
		if x == (0-SIZE) or x == 1000 or y == (0-SIZE) or y == 800:
			return True
		return False

	def play(self):
		self.snake.move()
		self.food.draw()
		self.display_score()
		pygame.display.flip()

		#snake hitting apple
		if self.is_collision(self.snake.x[0], self.snake.y[0], self.food.x, self.food.y):
			self.snake.increase_length()
			self.food.move()

		#snake hitting itself
		for i in range(3, self.snake.length):
			if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
				raise "game over"

		#snake hitting border
		if self.collides_border(self.snake.x[0], self.snake.y[0]):
			raise "game over"

	def show_game_over(self):
		self.playground.fill(BACKGROUND)
		font = pygame.font.SysFont('arial', 30)
		l1 = font.render(f"Game over! Your score: {self.snake.length}", True, (255, 255, 255))
		self.playground.blit(l1, (300, 300))
		l2 = font.render("Press Enter to start new game or Esc to exit", True, (255, 255, 255))
		self.playground.blit(l2, (300, 350))
		pygame.display.flip()

	def reset(self):
		self.snake = Snake(self.playground, 1)
		self.food = Food(self.playground)
	
	def run(self):
		running = True
		pause = False

		while running:
			for event in pygame.event.get():
				if event.type == KEYDOWN:
					if event.key == K_RETURN:
						pause = False
						self.reset()

					if event.key == K_ESCAPE:
						running = False

					if not pause:
						if event.key == K_UP:
							self.snake.move_up()
						if event.key == K_DOWN:
							self.snake.move_down()
						if event.key == K_LEFT:
							self.snake.move_left()
						if event.key == K_RIGHT:
							self.snake.move_right()	
				elif event.type == QUIT:
					running = False

			
			try:
				if not pause:
					self.play()
			except Exception as e:
				self.show_game_over()
				pause = True

			#delay speed 
			time.sleep(0.15)

if __name__ == "__main__":
	game = Game()
	game.run()
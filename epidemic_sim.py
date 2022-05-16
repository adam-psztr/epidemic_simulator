import pygame
import sys
from random import randint

# Constants
SCREEN_SIZE = WIDTH, HEIGHT = (1280, 720)
NUMBER_OF_PEOPLE = 10
PERSON_SPEED = 30
PERSON_COLOR_CLEAR = (200,150,0)
PERSON_COLOR_INFECTED = (200,0,0)
PERSON_COLOR_IMMUNE =(0,150,0)
PERSON_AURA = 20
ILLNESS_TIME = 500
IMMUNE_TIME = 800
INFECTION_PROBABILITY_WITH_MASK = 50
INFECTION_PROBABILITY_WITHOUT_MASK = 2
FIRST_CONTACT = 2

# Initialization
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Epidemic Simulator 1.0")
fps = pygame.time.Clock()
pause = False

# Person class
class Person:
	def __init__(self, x,y):
		self.x=x 
		self.y=y 
		self.dx = randint(-1,1)
		self.dy = randint(-1,1)
		self.illness = 0
		self.immune = 0
		self.mask = False

	def move(self):
		if randint(1,30) == 1:
			self.dx = randint(-1,1)
		if randint(1,30) == 1:
			self.dy = randint(-1,1)
		if PERSON_AURA < self.x + self.dx < WIDTH-PERSON_AURA:
			self.x += self.dx
		if PERSON_AURA < self.y + self.dy < HEIGHT-PERSON_AURA:
			self.y += self.dy

	def cure(self):
		if self.illness > 0:
			self.illness -= 1
			if self.illness == 0:
				self.immune = IMMUNE_TIME
		if self.immune > 0:
			self.immune -= 1

def modify(people):
	for person in people:
		person.move()
		person.cure()
		
		for other_person in people:
			if id(person) != id(other_person):
				if other_person.x - PERSON_AURA*2 < person.x < other_person.x+2*PERSON_AURA \
					and other_person.y - PERSON_AURA*2 < person.y < other_person.y+2*PERSON_AURA:
					if other_person.illness > 0 and person.illness == 0 and person.immune == 0:
						if person.mask == True or other_person == True:
							if randint(1, INFECTION_PROBABILITY_WITH_MASK) == 1:
								person.illness = ILLNESS_TIME
						else:
							if randint(1, INFECTION_PROBABILITY_WITHOUT_MASK) == 1:
								person.illness = ILLNESS_TIME

def draw(people):
	screen.fill((0,0,0))
	for person in people:
		if person.illness > 0:
			_color = PERSON_COLOR_INFECTED
		elif person.immune > 0:
			_color = PERSON_COLOR_IMMUNE
		else:
			_color = PERSON_COLOR_CLEAR
		pygame.draw.circle(screen, _color, (person.x, person.y), PERSON_AURA, 0)
	pygame.display.update()
	fps.tick(PERSON_SPEED)

# Create people
main_people_list = [Person(randint(50, WIDTH-50), randint(50, HEIGHT-50)) for i in range(NUMBER_OF_PEOPLE)]

# The first infection
for i in range(FIRST_CONTACT):
	main_people_list[i].illness = ILLNESS_TIME

# Main program
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				pause = not pause
	if not pause:
		modify(main_people_list)
		draw(main_people_list)


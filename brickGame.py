import random
import sys
import pygame

print("Craig Brick Game Started.")

print("PATH environment output:")
print("%s" % (sys.path))

pygame.init() #Initiates pygame resources, modules etc.
random.seed() #Initiate random number generator.

#Left mouse click definition...
LEFT = 1

# Colour code definitions (RGB)
black = (  0,   0,   0)
white = (255, 255, 255)
red   = (255,   0,   0)

# Just spacing constant values
#cyanConstant   = 0.2
#greenConstant  = 0.33
#redConstant    = 0.46
#purpleConstant = 0.59

# Some other game constants.
fpsLimit      = 60
displayWidth  = 1600
displayHeight = 900

resolution    = (displayWidth, displayHeight)
gameDisplay   = pygame.display.set_mode(resolution)

# Sprite parameters.
bigBrickCount  = 10
smallBallCount = 100

# Sprite images
playerImg       = pygame.image.load('player.png')
ballYellowImg   = pygame.image.load('smallYellowBall.png')
ballGreenImg    = pygame.image.load('smallGreenBall.png')
ballPinkImg     = pygame.image.load('smallPinkBall.png')
blueBrickImg    = pygame.image.load('blueBrick.png')
fractalBrickImg = pygame.image.load('fractalBrick.png')
brownBrickImg   = pygame.image.load('brownBrick.png')
weirdBrickImg   = pygame.image.load('weirdBrick.png')

# Movement speeds
playerSpeed      = 5
cyanStartSpeed   = 1
redStartSpeed    = 1
purpleStartSpeed = 2
greenStartSpeed  = 3
ballSpeed        = 4

pygame.display.set_caption('Craig''s Brick Moving Game')

clock = pygame.time.Clock()

gameOver = False

# This is a global which is set when the user left clicks on the screen
# and contains the last x,y coordinates where that occured.
# MySpriteData currently uses this to check for whether the sprite has
# been shot.
shootPositionX = 0
shootPositionY = 0


class MySpriteData(pygame.sprite.Sprite):
	def __init__(self, img, startX, startY, startSpeed):
		# Call the parent class (Sprite) constructor
		pygame.sprite.Sprite.__init__(self)
		
		self.image     = img
		self.initSpeed = startSpeed
		self.speedY    = random.randint(-self.initSpeed, self.initSpeed)
		self.speedX    = random.randint(-self.initSpeed, self.initSpeed)
		self.rect      = self.image.get_rect()
		self.rect.x    = startX
		self.rect.y    = startY
		
		self.visibleObjects = pygame.sprite.Group()
		
		# We check for collisions each frame and collided
		# surfaces for 9 cardinal points (N-E-W-S).
		self.collision = [False] * 9
	
		# If die is true then at next update we will animate and die.
		self.die       = False
	
	def setVisibleObjects(self, group):
		self.visibleObjects = group.copy()
		self.visibleObjects.remove(self)
			
	def resetCollisionStatus(self):
		self.collision = [False] * 9
	
	def eraseMe(self):
		gameDisplay.blit(blank, rect)
	
	def checkIfShot(self):
		#if my bounds in click bounds then yep i'm hit!
		if (shootPositionX > self.rect.x and shootPositionX < self.rect.x + self.rect.width and
		shootPositionY > self.rect.y and shootPositionY < self.rect.y + self.rect.height):
			return True
		return False
		
	def update(self):
		# Update position based on size and screen boundaries
		if ((self.rect.x + self.rect.width) >  displayWidth):
			self.speedX = -self.speedX
		elif ((self.rect.x) < 0):
			self.speedX = -self.speedX
		self.rect.x = self.rect.x + self.speedX
		
		if ((self.rect.y + self.rect.height) >  displayHeight):
			self.speedY = -self.speedY
		elif ((self.rect.y) < 0):
			self.speedY = -self.speedY
		self.rect.y = self.rect.y + self.speedY
	
	def collisionCheck(self):
		# Note: spritecollideany only returns 1 sprite collided.
		spriteCollided = pygame.sprite.spritecollideany(self, self.visibleObjects)
		if (spriteCollided):
			self.collision[0] = spriteCollided.rect.collidepoint(self.rect.topleft)
			self.collision[1] = spriteCollided.rect.collidepoint(self.rect.topright)
			self.collision[2] = spriteCollided.rect.collidepoint(self.rect.bottomleft)
			self.collision[3] = spriteCollided.rect.collidepoint(self.rect.bottomright)
			self.collision[4] = spriteCollided.rect.collidepoint(self.rect.midleft)
			self.collision[5] = spriteCollided.rect.collidepoint(self.rect.midright)
			self.collision[6] = spriteCollided.rect.collidepoint(self.rect.midtop)
			self.collision[7] = spriteCollided.rect.collidepoint(self.rect.midbottom)
			self.collision[8] = spriteCollided.rect.collidepoint(self.rect.center)
			return True
		return False
			
	def bounce(self):
		if (self.collision[0]): #top left
			self.speedY = self.initSpeed
			self.speedX = self.initSpeed
		if (self.collision[1]): #topright
			self.speedY = -self.initSpeed
			self.speedX = self.initSpeed
		if (self.collision[2]): #bottomleft
			self.speedY = self.initSpeed
			self.speedX = -self.initSpeed
		if (self.collision[3]): #bottomright
			self.speedY = -self.initSpeed
			self.speedX = -self.initSpeed
		if (self.collision[4]): #midleft
			self.speedY = 0
			self.speedX = self.initSpeed
		if (self.collision[5]): #midright
			self.speedY = 0
			self.speedX = -self.initSpeed
		if (self.collision[6]): #midtop
			self.speedY = self.initSpeed
			self.speedX = 0
		if (self.collision[7]): #midbottom
			self.speedY = -self.initSpeed 
			self.speedX = 0
		if (self.collision[8]): #center [If we get a center hit we 'dither']
			self.speedY = random.randint(-self.initSpeed, self.initSpeed)
			self.speedX = random.randint(-self.initSpeed, self.initSpeed)
				
		self.resetCollisionStatus()

# Spawn Mobs
allObjects = pygame.sprite.Group()
i = 0
while (i < bigBrickCount):
	diceRoll = random.randint(0, 3) #to pick between a few types during random spawn
	if (diceRoll == 0):
		myBrick = MySpriteData(blueBrickImg, random.randint(0, displayWidth - blueBrickImg.get_rect().width), random.randint(0, displayHeight - blueBrickImg.get_rect().height), cyanStartSpeed)
	elif (diceRoll == 1):
		myBrick = MySpriteData(brownBrickImg, random.randint(0, displayWidth - brownBrickImg.get_rect().width), random.randint(0, displayHeight - brownBrickImg.get_rect().height), redStartSpeed)
	elif (diceRoll == 2):
		myBrick = MySpriteData(fractalBrickImg, random.randint(0, displayWidth - fractalBrickImg.get_rect().width), random.randint(0, displayHeight - fractalBrickImg.get_rect().height), purpleStartSpeed)
	elif (diceRoll == 3):
		myBrick =MySpriteData(weirdBrickImg, random.randint(0, displayWidth - weirdBrickImg.get_rect().width), random.randint(0, displayHeight - weirdBrickImg.get_rect().height), greenStartSpeed)
	allObjects.add(myBrick)
	i = i + 1
	
i = 0
while (i < smallBallCount):
	diceRoll = random.randint(0, 2) #to pick between a few types during random spawn
	if (diceRoll == 0):
		myBall = MySpriteData(ballYellowImg, random.randint(0, displayWidth - ballYellowImg.get_rect().width), random.randint(0, displayHeight - ballYellowImg.get_rect().height), ballSpeed)
	if (diceRoll == 1): 
		myBall = MySpriteData(ballGreenImg, random.randint(0, displayWidth - ballGreenImg.get_rect().width), random.randint(0, displayHeight - ballGreenImg.get_rect().height), ballSpeed)
	if (diceRoll == 2):
		myBall = MySpriteData(ballPinkImg, random.randint(0, displayWidth - ballPinkImg.get_rect().width), random.randint(0, displayHeight - ballPinkImg.get_rect().height), ballSpeed)
	allObjects.add(myBall)
	i = i + 1

# Spawn Player
myPlayer = MySpriteData(playerImg, random.randint(0, displayWidth - playerImg.get_rect().width), random.randint(0, displayHeight - ballPinkImg.get_rect().height), playerSpeed)
allObjects.add(myPlayer)

# Make each member of allObjects aware of all other allObjects.
for aBrick in allObjects:
	aBrick.setVisibleObjects(allObjects)

# Main loop
while not gameOver:
	
	#Process key and mouse events...
	for event in pygame.event.get():
		#If they select QUIT then break out of loop.
		if event.type == pygame.QUIT:
			gameOver = True
			
		#Handle it so movement toggles on and off.
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				myPlayer.speedX = -myPlayer.initSpeed
			elif event.key == pygame.K_RIGHT:
				myPlayer.speedX = myPlayer.initSpeed
			if event.key == pygame.K_UP:
				myPlayer.speedY = -myPlayer.initSpeed
			elif event.key == pygame.K_DOWN:
				myPlayer.speedY = myPlayer.initSpeed
		
		# Mouse movement handler
		#if event.type == pygame.MOUSEMOTION:
		
		# Moust left click
		shootPositionX = shootPositionY = 0 # Init it.
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
			shootPositionX = event.pos[0]
			shootPositionY = event.pos[1]
			
	deathObjects = pygame.sprite.Group()
    #Check for collisions and if shot.	
	for aBrick in allObjects:
		if (aBrick.collisionCheck()):
			aBrick.bounce()
		if (aBrick.checkIfShot()):
			deathObjects.add(aBrick)
		
	for dier in deathObjects:
		allObjects.remove(dier)
	
	# Currently because collision checking takes a list copy I have
	# to manually update each object's known objects here...
	if (len(deathObjects)):
		for liver in allObjects:
			liver.setVisibleObjects(allObjects)
	
	gameDisplay.fill(black)
	
	#Update object positions
	allObjects.update()
	
	#Draw all objects
	allObjects.draw(gameDisplay)
	
	pygame.display.update()
	clock.tick(fpsLimit)

pygame.quit ()
print("Finished!")
quit()

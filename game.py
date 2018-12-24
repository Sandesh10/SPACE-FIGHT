#! /usr/bin/env python



#Import
import os, sys, pygame, random
from pygame.locals import *
os.environ['SDL_VIDEO_CENTERED'] = "1"
pygame.init()
pygame.display.set_caption("Space Fight")
icon = pygame.image.load("data/tile.png")
icon = pygame.display.set_icon(icon)
screen = pygame.display.set_mode((800, 600))
pygame.mouse.set_visible(0)

#Background
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0,0,0))
    
#Load Images
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error.message:
        print ('Cannot load image:', fullname)
        raise SystemExit.message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

#Load Sounds
def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    fullname = os.path.join('data', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error.message:
        print ('Cannot load sound:', fullname)
        raise SystemExit.message
    return sound



#Sprites

#This class controls the arena background
class Arena(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("menu/arena.jpg", -1)
        self.dy = 5
        self.reset()
        
    def update(self):
        self.rect.bottom += self.dy
        if self.rect.bottom >= 1200:
            self.reset() 
    
    def reset(self):
        self.rect.top = -600
        

#Player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("sprites/player.png", -1)
        self.rect.center = (400,500)
        self.dx = 0
        self.dy = 0
        self.reset()
        self.lasertimer = 0
        self.lasermax = 5
        self.bombamount = 1
        self.bombtimer = 0
        self.bombmax = 10
        
    def update(self):
        self.rect.move_ip((self.dx, self.dy))
        
        #Fire the laser
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            self.lasertimer = self.lasertimer + 1
            if self.lasertimer == self.lasermax:
                laserSprites.add(Laser(self.rect.midtop))
                fire.play()
                self.lasertimer = 0                    
                                
        #Player Boundaries    
        if self.rect.left < 0:
          self.rect.left = 0
        elif self.rect.right > 800:
          self.rect.right = 800
         
        if self.rect.top <= 260:
          self.rect.top = 260
        elif self.rect.bottom >= 600:
          self.rect.bottom = 600
        
    def reset(self):
        self.rect.bottom = 600  




#Laser class
class Laser(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("sprites/laser.png", -1)
        self.rect.center = pos

    
    def update(self):
        if self.rect.top < 0:
            self.kill()
        else:    
            self.rect.move_ip(0, -15)  



            
#Laser class
class EnemyLaser(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("sprites/elaser.png", -1)
        self.rect.center = pos

    
    def update(self):
        if self.rect.bottom < 0:
            self.kill()
        else:    
            self.rect.move_ip(0, 15) 
   

#Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, centerx):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("sprites/enemy.png", -1)
        self.rect = self.image.get_rect()
        self.dy = 8
        self.reset()
        
    def update(self):
        self.rect.centerx += self.dx
        self.rect.centery += self.dy
        if self.rect.top > screen.get_height():
            self.reset()



           
        #random 1 - 60 determines if firing
        efire = random.randint(1,60)
        if efire == 1:
            enemyLaserSprites.add(EnemyLaser(self.rect.midbottom))
            efire = load_sound("sounds/elaser.ogg")
            efire.play()
            
        #Laser Collisions    
        if pygame.sprite.groupcollide(enemySprites, laserSprites, 1, 1):
           explosionSprites.add(EnemyExplosion(self.rect.center))
           explode.play()
           score.score += 10
    
    def reset(self):
        self.rect.bottom = 0
        self.rect.centerx = random.randrange(0, screen.get_width())
        self.dy = random.randrange(5, 10)
        self.dx = random.randrange(-2, 2)
        
class Shield(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("sprites/shield.png", -1)
        self.rect.center = pos
        self.counter = 0
        self.maxcount = 2
    def update(self):
        self.counter = self.counter + 1
        if self.counter == self.maxcount:
            self.kill()
            
class EnemyExplosion(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("sprites/enemyexplosion.png", -1)
        self.rect.center = pos        
        self.counter = 0
        self.maxcount = 10
    def update(self):
        self.counter = self.counter + 1                 #####to display on screen
        if self.counter == self.maxcount:
            self.kill()
            

#Shield Powerup
class ShieldPowerup(pygame.sprite.Sprite):
    def __init__(self, centerx):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("sprites/shieldpowerup.png", -1)
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randrange(0, screen.get_width())
     
        
    def update(self):
        if self.rect.top > screen.get_height():
            self.kill
        else:    
            self.rect.move_ip(0, 6)         
        
class Score(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.shield = 100
        self.score = 0

        self.font = pygame.font.Font("data/fonts/arial.ttf", 28)
        
    def update(self):
        self.text = "Shield: %d                                            Score: %d" % (self.shield, self.score)
        self.image = self.font.render(self.text, 1, (0, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (400,20)
        
class Gameover(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font("data/fonts/planet5.ttf", 48)
        
    def update(self):
        self.text = ("GAME OVER")
        self.image = self.font.render(self.text, 1, (0, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (400,300)
        
class Gameoveresc(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font("data/fonts/arial.ttf", 28)
        
    def update(self):
        self.text = "PRESS ESC TO RETURN"
        self.image = self.font.render(self.text, 1, (0, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (400,400)
                    
#Game Module    
def game():
 
    #Game Objects
    global player
    player = Player()
    global score
    score = Score()


    ####Sounds are added  here check if error.
    
    global fire
    fire = load_sound("sounds/laser.ogg")
    global explode
    explode = load_sound("sounds/explode.ogg")
    global powerup
    powerup = load_sound("sounds/powerup.ogg")
    
    #Game Groups
    #####################Error12 Resolved
    
    #Player/Enemy
    playerSprite = pygame.sprite.RenderPlain((player))
    
    global enemySprites
    enemySprites = pygame.sprite.RenderPlain(())
    enemySprites.add(Enemy(20))
    enemySprites.add(Enemy(25))
    enemySprites.add(Enemy(30))
    
    
    global laserSprites
    laserSprites = pygame.sprite.RenderPlain(())
    
    global enemyLaserSprites
    enemyLaserSprites = pygame.sprite.RenderPlain(())
    
    global shieldPowerups
    shieldPowerups = pygame.sprite.RenderPlain(())
    
    shieldSprites = pygame.sprite.RenderPlain(())
    
    global explosionSprites
    explosionSprites = pygame.sprite.RenderPlain(())
    
    #################No error    
    #Score/and game over
    scoreSprite = pygame.sprite.Group(score)
    gameOverSprite = pygame.sprite.RenderPlain(())
    
    #Arena
    arena = Arena()
    arena = pygame.sprite.RenderPlain((arena))
    
    #####Tested
    #Set Clock
    clock = pygame.time.Clock()
    keepGoing = True
    counter = 0
  
    #Main Loop
    while keepGoing:
       clock.tick(30)
       #input
       for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.KEYDOWN:     ########Working
                if event.key == pygame.K_ESCAPE:
                    keepGoing = False
                elif event.key == pygame.K_LEFT:
                    player.dx = -10
                elif event.key == K_RIGHT:
                    player.dx = 10
                elif event.key == K_UP:
                    player.dy = -10
                elif event.key == K_DOWN:
                    player.dy = 10
            elif event.type == KEYUP:
                if event.key == K_LEFT:
                    player.dx = 0
                elif event.key == K_RIGHT:
                    player.dx = 0
                elif event.key == K_UP:             #Resolved... see pygame website for coordinate 
                    player.dy = 0
                elif event.key == K_DOWN:
                  player.dy = 0
                
             
             
       #Update and draw on the screen
       
       #Update     
       screen.blit(background, (0,0))     
       playerSprite.update()
       enemySprites.update()
       laserSprites.update()

       enemyLaserSprites.update()
       shieldPowerups.update()
       shieldSprites.update()
       explosionSprites.update()
       arena.update()
       scoreSprite.update()
       gameOverSprite.update()
       
       #Draw
       arena.draw(screen)
       playerSprite.draw(screen)
       enemySprites.draw(screen)
       laserSprites.draw(screen)
       
       enemyLaserSprites.draw(screen)
       
       shieldPowerups.draw(screen)
       shieldSprites.draw(screen)
       explosionSprites.draw(screen)
       
       scoreSprite.draw(screen)
       gameOverSprite.draw(screen)
       pygame.display.flip()
     
       # new enemies production
       counter += 1
       if counter >= 20:
          enemySprites.add(Enemy(20))
          counter = 0
       
       #Shield Power up
       #shieldPowerupcounter += 1      ########333Error NOT RESOLVED ########//NOT NECESSARY
       spawnShieldpowerup = random.randint(1,500)
       if spawnShieldpowerup == 1:
          shieldPowerups.add(ShieldPowerup(300))
          
        
          
       #Check if enemy lasers hit player's ship   
       for hit in pygame.sprite.groupcollide(enemyLaserSprites, playerSprite, 1, 0):
           explode.play()
           explosionSprites.add(Shield(player.rect.center))
           score.shield -= 10
           if score.shield <= 0:
              gameOverSprite.add(Gameover())
              gameOverSprite.add(Gameoveresc())
              playerSprite.remove(player)
              
                
       #Check if enemy collides with player 
       for hit in pygame.sprite.groupcollide(enemySprites, playerSprite, 1, 0):
           explode.play()
           explosionSprites.add(Shield(player.rect.center))
           score.shield -= 10
           if score.shield <= 0:
              gameOverSprite.add(Gameover())
              gameOverSprite.add(Gameoveresc())
              playerSprite.remove(player)
              
              
       #Check if player collides with shield powerup       
       for hit in pygame.sprite.groupcollide(shieldPowerups, playerSprite, 1, 0):
            if score.shield < 100:
               powerup.play()
               score.shield += 10
             
           
class SpaceMenu:

#Constructor
    def __init__(self, *options):

        self.options = options
        self.x = 0
        self.y = 0
        self.font = pygame.font.Font(None, 32)
        self.option = 0
        self.width = 1
        self.color = [0, 0, 0]
        self.hcolor = [0, 0, 0]
        self.height = len(self.options)*self.font.get_height()
        for o in self.options:
            text = o[0]
            ren = self.font.render(text, 1, (0, 0, 0))
            if ren.get_width() > self.width:
                self.width = ren.get_width()

#Draw the menu
    def draw(self, surface):
        i=0
        for o in self.options:
            if i==self.option:
                clr = self.hcolor
            else:
                clr = self.color
            text = o[0]
            ren = self.font.render(text, 1, clr)
            if ren.get_width() > self.width:
                self.width = ren.get_width()
            surface.blit(ren, (self.x, self.y + i*self.font.get_height()))
            i+=1

#Menu Input            
    def update(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:     #####PASS
                if e.key == pygame.K_DOWN:
                    self.option += 1
                if e.key == pygame.K_UP:
                    self.option -= 1
                if e.key == pygame.K_RETURN:
                    self.options[self.option][1]()
        if self.option > len(self.options)-1:
            self.option = 0
        if self.option < 0:
            self.option = len(self.options)-1

#Position Menu
    def set_pos(self, x, y):
        self.x = x
        self.y = y

#Font Style        
    def set_font(self, font):
        self.font = font

#Highlight Color        
    def set_highlight_color(self, color):
        self.hcolor = color         ###Highlighting

#Font Color        
    def set_normal_color(self, color):
        self.color = color

#Font position        
    def center_at(self, x, y):
        self.x = x-(self.width/2)
        self.y = y-(self.height/2)
        
        

def missionMenu():
    
    #Arena
    arena = Arena()
    arena = pygame.sprite.RenderPlain((arena))
    

    #Title for Option Menu
    menuTitle = SpaceMenu(
        ["Space Fight"])

    #Option Menu Text
    instructions = SpaceMenu(
        [""], 
        ["This is just a sample game. Images are directly"],
        [""],
        [" downloaded from internet. Navigate your space"],
        [""],
        [" vehicle with the arrow keys and use the space"],
        [""],
        [" bar to fire the laser. Be careful, you have a "],
        [""],
        [" limited supply. Kill as many enemies as you can!"],
        [""],
        [""],
        [""],
        [""],
        ["                   PRESS ESC TO RETURN                    "])

    #Title 
    menuTitle.center_at(150, 150)
    menuTitle.set_font(pygame.font.Font("data/fonts/planet5.ttf", 48))
    menuTitle.set_highlight_color((0, 255, 255))
        

    #Title Center
    instructions.center_at(440, 350)

    #Menu Font
    instructions.set_font(pygame.font.Font("data/fonts/arial.ttf", 22))

    #Highlight Color
    instructions.set_normal_color((0, 255, 255))


    #Set Clock
    clock = pygame.time.Clock()
    keepGoing = True

    while keepGoing:
           clock.tick(30)
           #input
           for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    keepGoing = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        keepGoing = False
           #Draw
           screen.blit(background, (0,0))    
           arena.update()
           arena.draw(screen)
           menuTitle.draw(screen)
           instructions.draw(screen)
           pygame.display.flip()




def aboutMenu():
 
    #Arena
    arena = Arena()
    arena = pygame.sprite.RenderPlain((arena))
    
    #About Menu Text
    #Title for Option Menu
    menuTitle = SpaceMenu(
        ["Space Fight"])

    info = SpaceMenu(
        [""], 
        ["Space Fight"],
        [""],
        ["A project by Sandesh Timilsina."],
        [""],
        ["B. Tech. CSE"],
        [""],
        [""],
        ["      PRESS ESC TO RETURN            "])
        

    #About Title Font color, alignment, and font type
    menuTitle.center_at(150, 150)
    menuTitle.set_font(pygame.font.Font("data/fonts/planet5.ttf", 48))
    menuTitle.set_highlight_color((0, 255, 255))

    #About Menu Text Alignment
    info.center_at(400, 310)

    #About Menu Font
    info.set_font(pygame.font.Font("data/fonts/arial.ttf", 28))

    #About Menu Font Color
    info.set_normal_color((0, 255, 255))


    #Set Clock
    clock = pygame.time.Clock()
    keepGoing = True

    while keepGoing:
           clock.tick(30)
           #input
           for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    keepGoing = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        keepGoing = False
           #Draw
           screen.blit(background, (0,0))    
           arena.update()
           arena.draw(screen)
           menuTitle.draw(screen)
           info.draw(screen)
           pygame.display.flip()

#Functions

def option1():
    game()
def option2():
    missionMenu()
def option3():
    aboutMenu()   
def option4():
    pygame.quit()
    sys.exit()
    
        

#Main
def main():

    
    #Arena
    arena = Arena()
    arena = pygame.sprite.RenderPlain((arena))

   
    #Defines menu, option functions, and option display.  
    menuTitle = SpaceMenu(
        [" Space Fight"])
        
    menu = SpaceMenu(
        ["Start", option1],
        ["Misson", option2],
        ["About", option3],
        ["Quit", option4])
        
        

    #Title
    menuTitle.center_at(150, 150)
    menuTitle.set_font(pygame.font.Font("data/fonts/planet5.ttf", 48))
    menuTitle.set_highlight_color((0, 255, 255))
    
    #Menu settings
    menu.center_at(400, 320)
    menu.set_font(pygame.font.Font("data/fonts/arial.ttf", 32))
    menu.set_highlight_color((0, 255, 250))
    menu.set_normal_color((0, 85, 88))
    
    clock = pygame.time.Clock()
    keepGoing = True


    while 1:
        clock.tick(30)

        #Events
        events = pygame.event.get()

        #Update Menu
        menu.update(events)

        #Quit Event
        for e in events:
            if e.type == pygame.QUIT:
                pygame.quit()
                return

        #Draw
        screen.blit(background, (0,0))
        arena.update()
        arena.draw(screen)
        menu.draw(screen)
        menuTitle.draw(screen)
        pygame.display.flip()

if __name__ == "__main__":
   main()

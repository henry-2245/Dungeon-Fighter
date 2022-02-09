import pygame
from pygame.locals import * #access locals without pygame prefix
import sys #for exit
import random



pygame.init()#begin the game

#Declearing variables
vec = pygame.math.Vector2 #2d
HEIGHT = 400
WIDTH = 700
ACC = 0.5
FRIC = -0.2
FPS = 60
FPS_CLOCK = pygame.time.Clock()
COUNT = 0



#display the windows
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
black = (0, 0, 0)
pygame.display.set_caption("Dugeon Fighter")

#starting background
background1 = pygame.image.load("mainscreen.png")

#running animation right
run_ani_r = [pygame.image.load("idle1.png"),pygame.image.load("run1.png"),pygame.image.load("run2.png"),pygame.image.load("run3.png"),pygame.image.load("run4.png"),
             pygame.image.load("run5.png"),pygame.image.load("run6.png"),pygame.image.load("run7.png"),pygame.image.load("run8.png"),
             pygame.image.load("run9.png"),pygame.image.load("run10.png"),pygame.image.load("idle1.png")]

#running animation left
run_ani_l = [pygame.image.load("lidle1.png"),pygame.image.load("lrun1.png"),pygame.image.load("lrun2.png"),pygame.image.load("lrun3.png"),pygame.image.load("lrun4.png"),
             pygame.image.load("lrun5.png"),pygame.image.load("lrun6.png"),pygame.image.load("lrun7.png"),pygame.image.load("lrun8.png"),
             pygame.image.load("lrun9.png"),pygame.image.load("lrun10.png"),pygame.image.load("lidle1.png")]

#attack animation right
attack_ani_r = [pygame.image.load("idle1.png"),pygame.image.load("attack1.png"),pygame.image.load("attack2.png"),pygame.image.load("attack3.png"),
                pygame.image.load("attack4.png"),pygame.image.load("attack5.png"),pygame.image.load("attack6.png"),pygame.image.load("attack2.1.png"),
                pygame.image.load("attack2.2.png"),pygame.image.load("attack2.3.png"),pygame.image.load("attack2.4.png"),pygame.image.load("attack2.5.png"),
                pygame.image.load("attack2.6.png"),pygame.image.load("idle1.png")]

#attack animation left
attack_ani_l = [pygame.image.load("lidle1.png"),pygame.image.load("lattack1.png"),pygame.image.load("lattack2.png"),pygame.image.load("lattack3.png"),
                pygame.image.load("lattack4.png"),pygame.image.load("lattack5.png"),pygame.image.load("lattack6.png"),pygame.image.load("lattack2.1.png"),
                pygame.image.load("lattack2.2.png"),pygame.image.load("lattack2.3.png"),pygame.image.load("lattack2.4.png"),pygame.image.load("lattack2.5.png"),
                pygame.image.load("lattack2.6.png"),pygame.image.load("lidle1.png")]


# Door
door_ani = [pygame.image.load("Door-0.png"), pygame.image.load("Door-1.png"),
            pygame.image.load("Door-1.png"),pygame.image.load("Door-2.png"),
            pygame.image.load("Door-2.png"),pygame.image.load("Door-3.png"),
            pygame.image.load("Door-3.png"),pygame.image.load("Door-4.png"),
            pygame.image.load("Door-4.png"),pygame.image.load("Door-5.png"),
            pygame.image.load("Door-5.png")]

#health bar
health_ani = [pygame.transform.scale(pygame.image.load("heart0.png"), (30,35)),pygame.transform.scale(pygame.image.load("heart.png"), (30,35)),
              pygame.transform.scale(pygame.image.load("heart2.png"), (60,35)),pygame.transform.scale(pygame.image.load("heart3.png"), (90,35)),
              pygame.transform.scale(pygame.image.load("heart4.png"), (120,35)),pygame.transform.scale(pygame.image.load("heart5.png"), (150,35))]              


#Classes
class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()  #no need for pygame.sprite.Sprite
        self.bgimage = pygame.image.load("background2.png")
        self.bgimage = pygame.transform.scale(self.bgimage,(700,400))
        self.rect = self.bgimage.get_rect(center = (350, 350))
        self.bgX = 0
        self.bgY = 0

    def render(self):
        displaysurface.blit(self.bgimage, (self.bgX, self.bgY))


#pygame class for visible class object        
class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.bgimage = pygame.image.load("ground1.png")
        self.rect = self.bgimage.get_rect(center = (350, 350))

    def render(self):
        displaysurface.blit(self.bgimage, (self.rect.x, self.rect.y))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pimage = pygame.image.load("idle1.png")
        self.pimage = pygame.transform.scale(self.pimage,(80,75))
        self.rect = self.pimage.get_rect(size = (15,75))


        #movement
        self.jumping = False
        self.running = False
        self.move_frame = 0 #track current frame of the character

        #attack
        self.attacking = False
        self.cooldown = False
        self.attack_frame = 0
        self.health = 5

        #position and direction
        self.pos = vec((340, 260))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.direction = "RIGHT"

        

    def move(self):
        #keeps player down due to gravity(y cord)
        self.acc = vec(0,0.5)
        
        # if player slows down running will be set to false
        if abs(self.vel.x) > 0.3:
            self.running = True
        else:
            self.running = False

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_a]:
            self.acc.x = -ACC
        if pressed_keys[K_d]:
            self.acc.x = ACC
            
        #get acceleration by multiply velocity and friction
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc #update player new position

        #move player from edge of the screen to another edge of the screen
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos #update player to new position

    def gravity_check(self):
        hits = pygame.sprite.spritecollide(player, ground_group, False)
        if self.vel.y > 0:
            if hits: #if the player got contacted with the ground
                lowest = hits[0]
                if self.pos.y < lowest.rect.bottom:
                    self.pos.y = lowest.rect.top + 1
                    self.vel.y = 0
                    self.jumping = False #player is touching ground which isn't in state of jummping
                    
 
    def update(self):
        #return to first frame after the last frame
        if self.move_frame > 11:
            self.move_frame = 0
            return

        #continue to next frame if character meets requirements
        if self.jumping == False and self.running == True:
            if self.vel.x > 0: #direction of player
                self.pimage = pygame.transform.scale(run_ani_r[self.move_frame],(80,75))
                self.direction = "RIGHT"
            else:
                self.pimage = pygame.transform.scale(run_ani_l[self.move_frame],(80,75))
                self.direction = "LEFT"
            self.move_frame += 1 #update player direction

        #return player to base frame if standing still and wrong frame
        if abs(self.vel.x) < 0.2 and self.move_frame != 0:
            self.move_frame = 0
            if self.direction == "RIGHT":
                self.pimage = pygame.transform.scale(run_ani_r[self.move_frame],(80,75))#resize the image
            elif self.direction == "LEFT":
                self.pimage = pygame.transform.scale(run_ani_l[self.move_frame],(80,75))
 
    def attack(self):
        #if last attack frame is finsihed, return to the first frame
        if self.attack_frame > 13:
            self.attack_frame = 0
            self.attacking = False

        #check direction for correct animation to display
        if self.direction == "RIGHT":
            self.pimage = pygame.transform.scale(attack_ani_r[self.attack_frame], (80,75))
        elif self.direction == "LEFT":
            self.pimage = pygame.transform.scale(attack_ani_l[self.attack_frame], (80,75))

        self.attack_frame += 1
            
 
    def jump(self):
        self.rect.x += 1

        #check if player is in contact with the ground
        hits = pygame.sprite.spritecollide(self,ground_group, False)

        self.rect.x -= 1

        #check if touching the ground and not in the jumping motion then player can jump
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -12 #negative because velocity downward is positive

    def player_hit(self):
        if self.cooldown == False:      
            self.cooldown = True # Enable the cooldown
            pygame.time.set_timer(hit_cooldown, 1000) # Resets cooldown in 1 second

            self.health = self.health -1
            health.image = health_ani[self.health]
            
            if self.health <= 0:
                self.kill()
                pygame.display.update()
                print("Game Over")

          

class HealthBar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("heart5.png")
        self.image = pygame.transform.scale(self.image,(150,35))

    def render(self):
        displaysurface.blit(self.image, (10,10))
            

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.mimage = pygame.transform.scale(pygame.image.load("m1idle1.png"),(43,43))
        self.rect = self.mimage.get_rect()
        #create two vectors
        self.pos = vec(0,0) 
        self.vel = vec(0,0)

        self.direction = random.randint(0,1) #0 for Right, 1 for Left
        self.vel.x = random.randint(2,6) / 2 #randomized velocity for enemy

        #set position for enemy
        if self.direction == 0:
            self.pos.x = 0
            self.pos.y = 240
        if self.direction == 1:
            self.pos.x = 700
            self.pos.y = 240


    def move(self):
        #cause the enemy to warp midway
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        
        # Random direction
        if self.pos.x == (WIDTH / 2):
            self.direction = random.randint(0,1)
            
        if self.pos.x == (WIDTH / 4):
            self.direction = random.randint(0,1)

        if self.pos.x == (3 * WIDTH / 4):
            self.direction = random.randint(0,1)

        #update position with new values
        if self.direction == 0:
            self.pos.x += self.vel.x #add into position x base on direction of enemy
        if self.direction == 1:
            self.pos.x -= self.vel.x #same but minus

        self.rect.center = self.pos #update rect
        
    
    def update(self):
        #check collision with player
        hits = pygame.sprite.spritecollide(self, Playergroup, False)


        if self.direction == 0:
            self.mimage = pygame.transform.scale(pygame.image.load("m1idle1.png"),(63,63))
        else:
            self.mimage = pygame.transform.scale(pygame.image.load("lm1idle1.png"),(63,63))

        #Active if player is in attakcing motion and enemy collide with player
        if hits and player.attacking == True:
            print("Enemy Killed")
            self.kill()
        
        #Active if player not in attacking motion and enemy collide with player
        elif hits and player.attacking == False:
            player.player_hit()
            

    def render(self):
        #Display enemy
        displaysurface.blit(self.mimage, (self.pos.x, self.pos.y))
        

class Entrance(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.hide = False
        self.image = pygame.image.load("Door-0.png")
        self.image = pygame.transform.scale(self.image,(120,200))

        #Door
        self.doorop = False
        self.door_frame = 0
        
    def door(self):
        for i in range (10):
            if self.door_frame > 10:
                self.door_frame = 10
                self.doorop = True
                
            self.image = pygame.transform.scale(door_ani[self.door_frame], (120,200))

            self.door_frame += 1

    def update(self):
        if self.hide == False:
            displaysurface.blit(self.image, (499, 105))


class EventHandler():
    def __init__(self):
        super().__init__()
        self.enemy_count = 0
        self.battle = False
        self.enemy_generation = pygame.USEREVENT + 1
        self.stage = 1
        self.level = 10
        self.wincon = self.stage
        self.win = False
        self.lose = False

        #generate based from 1 until num level in game +1
        self.stage_enemies = []
        for x in range(1,self.level + 1):
            self.stage_enemies.append(int((x ** 2 / 2) +1)) #enemies keep getting bigger(odd)

    def world(self):
        pygame.time.set_timer(self.enemy_generation, 2000)
        entrance.hide = True
        self.battle = True

    def next_stage(self):
        if self.win == False:
            if self.stage < self.level:
                self.stage += 1
                self.wincon += 1
                print("Stage: " + str(self.stage))
                self.enemy_count = 0
                pygame.time.set_timer(self.enemy_generation ,1500 - (50 * self.stage))
            else:
                self.win = True
                self.wincon += 1
                print("YOU WIN")
                exit
            
                       

class Win(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("youwin.jpg")
        self.image = pygame.transform.scale(self.image,(700,400))

    def render(self):
        displaysurface.blit(self.image, (0,0))


class Over(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("over.jpg")
        self.image = pygame.transform.scale(self.image,(700,400))


    def render(self):
        displaysurface.blit(self.image, (0,0))


         

Enemies = pygame.sprite.Group()
enemy = Enemy()
win = Win()
over = Over()

player = Player()
Playergroup = pygame.sprite.Group()
Playergroup.add(player)

background = Background()

ground = Ground()
ground_group = pygame.sprite.Group()
ground_group.add(ground)

entrance = Entrance()
handler = EventHandler()
health = HealthBar() 

hit_cooldown = pygame.USEREVENT + 2



#Game Loop
menu = True
running = True

  
while running:

    while menu:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    menu = False


        displaysurface.fill((0,0,0))
        FPS_CLOCK.tick(30)
        displaysurface.blit(background1, (0,0))

        pygame.display.update()
    player.gravity_check() #check at the start of the game



    
    for event in pygame.event.get():
        if event.type == hit_cooldown:
            player.cooldown = False
            pygame.time.set_timer(hit_cooldown, 0)
            
        #close the game if click on the close tab
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        #
        if event.type == handler.enemy_generation:
            if handler.enemy_count < handler.stage_enemies[handler.stage - 1]:
                enemy = Enemy()
                Enemies.add(enemy)
                handler.enemy_count += 1

        if handler.stage_enemies[handler.stage - 1] == handler.enemy_count: 
                  if handler.battle == True and len(Enemies) == 0:
                      handler.next_stage()
                
        
        #key presses
        if event.type == pygame.KEYDOWN:
            if handler.wincon > handler.level:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_e and 370 < player.rect.x < 550:
                entrance.door()
            if event.key == pygame.K_e and 370 < player.rect.x < 550:
                if entrance.doorop == True:
                    handler.world()
    
            if event.key == pygame.K_w: #for jump
                player.jump()
            if event.key == pygame.K_SPACE: #attack
                if player.attacking == False:
                    player.attack()
                    player.attacking = True

            if event.key == pygame.K_p: #pause
                menu = True

            if event.key == pygame.K_c:
                menu = True

            
            
    #player
    player.update()
    if player.attacking == True: #keep calling until all attack frame has been over
        player.attack()
    player.move()

    
    #render
    background.render()
    ground.render()

    entrance.update()
    if player.health > 0:
        displaysurface.blit(player.pimage, player.rect)
    health.render()

    #Win
    if handler.wincon > handler.level:
        win.render()


    #repeat the fucnction
    for entity in Enemies:
          entity.update()
          entity.move()
          entity.render()

    #Game over
    if player.health <= 0:
        over.render()


    pygame.display.update()
    FPS_CLOCK.tick(FPS)


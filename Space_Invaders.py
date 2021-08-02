import pygame, sys, random
class Spaceship(pygame.sprite.Sprite): # sprite class 1
    def __init__(self, path, x_pos, y_pos):
        super().__init__()
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect(center  = (x_pos, y_pos))
        self.shield_surface = pygame.image.load("shield.png").convert_alpha()
        self.health = 5

    def update(self):
        "Updates spaceship's position with the mouse pointer's position on the screen "
        self.rect.center = pygame.mouse.get_pos()
        self.screen_constrain()
        self.display_health()
        

    def screen_constrain(self):
        "This function gives border limits to the spaceship"
        if self.rect.right >= 1280:
            self.rect.right = 1280

        if self.rect.left <= 0:
            self.rect.left = 0

        if self.rect.bottom >= 720:
            self.rect.bottom = 720

        if self.rect.top <= 0:
            self.rect.top = 0

    def display_health(self):
        for index, shield in enumerate(range(self.health)):
            screen.blit(self.shield_surface, (10+index*40, 10))


    def get_damage(self, damage_amount):
        self.health -= damage_amount
        

    

class Meteor(pygame.sprite.Sprite): # sprite class 2
    def __init__(self, path, x_pos, y_pos, x_speed, y_speed):
        " Initialising every parameter of the meteor group"
        super().__init__()
        self.image = pygame.image.load("meteor1.png").convert_alpha()
        self.rect = self.image.get_rect(center = (x_pos, y_pos))
        self.x_speed = x_speed
        self.y_speed = y_speed


    def update(self):
        "Defines and changes the speed and Movement of the meteors on the screen"

        self.rect.centerx += self.x_speed
        self.rect.centery += self.y_speed

        if self.rect.centery >= 800:
            self.kill() # to destroy the sprited from the screen as soon as they leave the screen
        
class Laser(pygame.sprite.Sprite):
    def __init__(self, path, pos, speed):
        super().__init__()
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect(center  = pos)
        self.speed = speed

    def update(self):
        self.rect.centery -= self.speed

        # for destroying the spritewen it goes off the screen
        if self.rect.centery <= -10*100/100:
            self.kill()


def main_game():
    "Method for the main game play"
    laser_group.draw(screen)
    
    spaceship_group.draw(screen)
    meteor_group.draw(screen)
    
    laser_group.update()
    spaceship_group.update()
    meteor_group.update()


    # collision check
    if pygame.sprite.spritecollide(spaceship_group.sprite, meteor_group, True):
        spaceship_group.sprite.get_damage(1)


    for laser in laser_group:
        pygame.sprite.spritecollide(laser, meteor_group, True)


    return 1


def end_game():
    "Method for the game over event in our game"
    text_surface = game_font.render("Game Over!!!", True, (255, 255, 0))
    text_rect = text_surface.get_rect(center = (640, 320))
    screen.blit(text_surface, text_rect)

    score_surface = game_font.render(f"Your Score is {score}", True, (255, 255, 0))
    score_rect = text_surface.get_rect(center = (640, 400))
    screen.blit(score_surface, score_rect)
    
        
pygame.init() # initializig the module

# screen setup
screen = pygame.display.set_mode((1280, 720)) 

title = pygame.display.set_caption("Space Invaders")

# frames per second clock
clock = pygame.time.Clock()

# game font
game_font = pygame.font.Font("kenvector_future.ttf", 100)

score = 0

spaceship = Spaceship("spaceship.png", 640, 500)
spaceship_group = pygame.sprite.GroupSingle()
spaceship_group.add(spaceship)

meteor1 = Meteor("meteor1", 400, -100, 1, 4) # sprite class 2 object 
meteor_group = pygame.sprite.Group()
meteor_group.add(meteor1)

METEOR_EVENT = pygame.USEREVENT # defining the userevent for occuring meteors
pygame.time.set_timer(METEOR_EVENT, 250)

laser_group = pygame.sprite.Group()

# main game loop
game_is_running = True 
while game_is_running:

    for event in pygame.event.get(): # event looping
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == METEOR_EVENT:
            meteor_path = random.choice(("meteor1.png", "meteor2.png", "meteor3.png", "meteor4.png")) # picks one of these images randomly
            random_x_pos = random.randrange(0, 1280)
            random_y_pos = random.randrange(-500, -50)
            random_x_speed = random.randrange(-1, 1)
            random_y_speed = random.randrange(4, 10)
            meteor = Meteor(meteor_path, random_x_pos, random_y_pos, random_x_speed, random_y_speed)
            meteor_group.add(meteor)

        if event.type == pygame.MOUSEBUTTONDOWN:
            new_laser = Laser("laser.png", event.pos, 50)
            laser_group.add(new_laser)


        if event.type == pygame.MOUSEBUTTONDOWN and spaceship_group.sprite.health <= 0:
            spaceship_group.sprite.health = 5
            meteor_group.empty()
            


    screen.fill((12, 42, 61))
    if spaceship_group.sprite.health > 0:
        score += main_game() # calling the main method
    

    else:
        end_game()
        
    




    

    pygame.display.flip()
    clock.tick(60) # setting up the FPS
    

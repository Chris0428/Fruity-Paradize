import pygame, sys, math, random
from os import listdir
from os.path import isfile, join
from Button import Button

#Pygame setup
pygame.init()

OBJECT_SPEED = 5 

#Background Music
BGM = pygame.mixer.music.load('BGM.mp3')
pygame.mixer.music.set_volume(0.02)
pygame.mixer.music.play(-1)

# Screen Size
WIDTH, HEIGHT = (1000, 710)
screen = pygame.display.set_mode((WIDTH, HEIGHT))

#Variables
FPS = 60
PLAYER_VEL = 7
clock = pygame.time.Clock()
block_size = 96

#Background
cloud_1 = pygame.transform.scale(pygame.image.load("background/cloud_1.png"), (WIDTH, HEIGHT)).convert_alpha()
cloud_2 = pygame.transform.scale(pygame.image.load("background/cloud_2.png"), (WIDTH, HEIGHT)).convert_alpha()
cloud_3 = pygame.transform.scale(pygame.image.load("background/cloud_3.png"), (WIDTH, HEIGHT)).convert_alpha()
scroll_speed = 0.5
tiles = math.ceil(WIDTH / WIDTH) + 1

#Item images
size = 64
bomb_img = pygame.transform.scale(pygame.image.load("Trap_Bomb/bomb.png"), (size, size)).convert_alpha()
fruit = None

bg_images = []
for i in range(1, 4):
    bg_image = pygame.transform.scale(pygame.image.load(f"background/bg_{i}.png"), (WIDTH, HEIGHT)).convert_alpha()
    bg_images.append(bg_image)
def draw_bg():
    for i in bg_images:
        screen.blit(i,(0,0))



#Game Title
title = pygame.image.load("Title.png").convert_alpha()
title = pygame.transform.scale(title, (400, 200))


#Flips Spritesheets 
def flip(sprites):
    return[pygame.transform.flip(sprite, True, False) for sprite in sprites]

#Load Spritesheet
def load_spritesheets(dir, width, height, direction=False):
    path = join('.', dir)
    images = [f for f in listdir(path) if isfile(join(path, f))]
    all_sprites = {} 

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()
        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i*width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))

        if direction:
            all_sprites[image.replace(".png", "") + "right"] = sprites
            all_sprites[image.replace(".png", "") + "left"] = flip(sprites)        
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites


#Player Code
class Player(pygame.sprite.Sprite):

    GRAVITY = 1
    SPRITES = load_spritesheets("Berie", 48, 48, True)
    ANIMATION_DELAY = 5

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0 
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self):
        self.move(self.x_vel, self.y_vel)
        self.update_sprite()


 
    def update_sprite(self):
        sprite_sheet = "Idle"
        if self.x_vel != 0:
            sprite_sheet = "Run"

        sprite_sheet_name = sprite_sheet + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win):
        win.blit(self.sprite, (self.rect.x, self.rect.y))


class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width 
        self.height = height
        self.name = name

    def draw(self, win):
        win.blit(self.image, (self.rect.x, self.rect.y))

def get_block(size):
    image = pygame.image.load("Sand.png").convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(5, 0, size, size)
    surface.blit(image, (0,0), rect)
    return pygame.transform.scale2x(surface)

class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = get_block(size)
        self.image.blit(block, (0,0))
        self.mask = pygame.mask.from_surface(self.image)

class Bomb(object):
    def __init__(self, item, bomb):
        self.item = item
        if self.item == 1:
            self.image = bomb
            self.mask = pygame.mask.from_surface(self.image)
        self.randPoint = random.choice([(random.randrange(220, 728), -64)])
        
        self.x, self.y = self.randPoint
        if self.y < HEIGHT:
            self.ydir = 1
        else:
            self.ydir = -1
        self.yv = self.ydir * random.randrange(1, 3)
        
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
    


class animals(Object):
    ANIMATION_DELAY = 8
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "animal")
        self.animal = load_spritesheets("animals",width, height)
        self.image = self.animal["chicken"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "chicken"

    def chicken(self):
        self.animation_name = "chicken"

    def turtle(self):
        self.animation_name = "turtle"

    def duck(self):
        self.animation_name = "duck"

    def crab(self):
        self.animation_name = "crab"
        
        
    def loop(self):
        sprites = self.animal[self.animation_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)
        
        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.anaimation_count = 0

        
#Trees
def draw_tree(f, x):
    trees = []
    l = f + 1
    for i in range(f, l):
        tree_image = pygame.transform.scale(pygame.image.load(f"tree/tree_{i}.png"), (400, 400)).convert_alpha()
        trees.append(tree_image)
    for i in trees:
        screen.blit(i,(x, HEIGHT - block_size -400))
    


bomb = []
#Draws Player & objects on Screen
def draw(screen, player, objects, animal_1,  animal_2,  animal_3,  animal_4):
    for obj in objects:
        obj.draw(screen)
    for a in bomb:
        a.draw(screen)

    animal_1.draw(screen)
    animal_2.draw(screen)
    animal_3.draw(screen)
    animal_4.draw(screen)
    player.draw(screen)

    pygame.display.update()


def handle_vertical_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
        collided_objects.append(obj)





# Player Movement
def movement(player, objects):
    keys = pygame.key.get_pressed()

    player.x_vel = 0
    if keys[pygame.K_LEFT] and player.rect.x > 185:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT] and player.rect.x < 724:
        player.move_right(PLAYER_VEL)

    handle_vertical_collision(player, objects, player.y_vel)



#Playing Screen
def game():
    #Player Rect
    player = Player(448, 519, 48, 48)
    animal_1 = animals(140, HEIGHT - block_size - 32, 16, 16)
    animal_2 = animals(90, HEIGHT - block_size - 32, 16, 16)
    animal_3 = animals(850, HEIGHT - block_size - 32, 16, 16)
    animal_4 = animals(900, HEIGHT - block_size - 32, 16, 16)
    animal_1.chicken()
    animal_2.turtle()
    animal_3.duck()
    animal_4.crab()
   


    #Draws Floor
    floor = [Block(i * block_size, HEIGHT - block_size, block_size)
            for i in range(-WIDTH // block_size, (WIDTH * 2) // block_size)]

    scroll = 0
    count = 0
    while True:
        clock.tick(FPS)
        count += 1
        if count % 50 == 0:
            ran = random.choice([1])
            bomb.append(Bomb(ran, bomb_img))

        for a in bomb:
            a.y += a.yv
    #Displays Background\
        draw_bg()
        #Clouds
        for i in range(0, tiles):
            screen.blit(cloud_1, (i * WIDTH + scroll, 0))
            screen.blit(cloud_2, (i * WIDTH + scroll, 0))
            screen.blit(cloud_3, (i * WIDTH + scroll, 0))
        scroll -= scroll_speed
        
        if abs(scroll) > WIDTH:
            scroll = 0

        #Trees
        draw_tree(1, -20)
        draw_tree(2, 625)
        draw_tree(3, 780)
        draw_tree(4, -190)


    #Event Handler
        for event in pygame.event.get():

        # Exit Game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()



        player.loop()
        animal_1.loop()
        animal_2.loop()
        animal_3.loop()
        animal_4.loop()
        movement(player, floor,)
        draw(screen, player, floor, animal_1, animal_2, animal_3, animal_4)
       

        pygame.display.flip()
        pygame.display.update()



#Main Menu        
def main_menu():
    
    pygame.display.set_caption("Fruity Paradise")
    scroll = 0
    while True:
        draw_bg()
        #Clouds
        for i in range(0, tiles):
            screen.blit(cloud_1, (i * WIDTH + scroll, 0))
            screen.blit(cloud_2, (i * WIDTH + scroll, 0))
            screen.blit(cloud_3, (i * WIDTH + scroll, 0))
        scroll -= scroll_speed

            
        screen.blit(title, (90, 50))
        
        MOUSE = pygame.mouse.get_pos()

        START_BUTTON = Button(130, 500, "Button/Start_Button.png", "Button/Start_Button_Hover.png")
        QUIT_BUTTON =Button(450, 500, "Button/Quit_Button.png", "Button/Quit_Button_Hover.png")

        for button in [START_BUTTON, QUIT_BUTTON]:
            button.hover_button(MOUSE)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if START_BUTTON.checkForInput(MOUSE):
                    game()

        if event.type == pygame.MOUSEBUTTONDOWN:
                if QUIT_BUTTON.checkForInput(MOUSE):
                    sys.exit()

        pygame.display.update()
main_menu()


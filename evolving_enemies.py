import random
import pygame
import math
import os

import pygameMenu
from pygameMenu.locals import *

# *****************************************************************************
# Info text for the About Menu
# *****************************************************************************

ABOUT = ['Evolving Enemies:',
         'A Game where the Enemies evolve using Genetic Algorithms',
         PYGAMEMENU_TEXT_NEWLINE,
         'Author: Nipuna Weeratunge',
         PYGAMEMENU_TEXT_NEWLINE,
         'Email: nipunaw1@gmail.com']

# *****************************************************************************
# Info text for the Help Menu
# *****************************************************************************

HELP = ['Controls:',
         'Use  Arrow  keys  to  move  player  ship  left/right.',
         PYGAMEMENU_TEXT_NEWLINE,
         'Press  SpaceBar  to  fire  Missile.']

# *****************************************************************************
# Defining the constants and variables
# *****************************************************************************

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
WINDOW_START_POSITION_X = 200
WINDOW_START_POSITION_Y = 0
PLAYER_FIRE_TORPEDO = False
PLAYER_TORPEDO_FIRING_RATE = 5
GENERATE_GAME_OBJECTS = True
MUTATION_RATE_MATRIX = ['0.2']
MUTATION_RATE = 0.2
COLOR_BACKGROUND = (100, 100, 100)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (250, 250, 250)
COLOR_BLUE = (0, 0, 250)
COLOR_RED = (250,0,0)
MENU_BACKGROUND_COLOR = (0, 0, 0)
GAME_DIFFICULTY = ['EASY']
RUN_GAME = True
EPISODE_COUNT = 0
ENEMY_MISSILE_TIMER = 5000

# *****************************************************************************
# The start window position for the game window
# *****************************************************************************

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (WINDOW_START_POSITION_X,WINDOW_START_POSITION_Y)

# *****************************************************************************
# Initialize Pygame and create screen and objects
# *****************************************************************************

pygame.init()
pygame.display.set_caption("Evolving Enemies")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
STAR_FIELD_TIMER = pygame.time.get_ticks()
episode_info_text = pygame.font.Font(pygameMenu.fonts.FONT_FRANCHISE, 30)

# *****************************************************************************
# The initial population for the Genetic Algorithm
# *****************************************************************************

A0 = [0, 0, 0, 0, 0, 0, 0]
A1 = [0, 0, 0, 0, 0, 0, 0]
A2 = [0, 0, 0, 0, 0, 0, 0]
A3 = [0, 0, 0, 0, 0, 0, 0]
A4 = [0, 0, 0, 0, 0, 0, 0]
A5 = [0, 0, 0, 0, 0, 0, 0]

initial_population = [A0,A1,A2,A3,A4,A5]
chromosome_length = len(A0)-1

# *****************************************************************************
# Creates the pygame sprite groups and enemy ship lists
# *****************************************************************************

player_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()
player_projectile_list = pygame.sprite.Group()
enemy_projectile_list = pygame.sprite.Group()
enemy_list = pygame.sprite.Group()
enemy_shield_list = pygame.sprite.Group()
star_field_list = pygame.sprite.Group()
current_enemy_population = []
enemy_ship_list = []

# *****************************************************************************
# Creates Genetic Algorithm class
# *****************************************************************************

class Genetic_Algorithm():

    # Initialize the class
    def __init__(self, initial_population,MUTATION_RATE,chromosome_length):
        self.initial_population = initial_population
        self.MUTATION_RATE = MUTATION_RATE
        self.chromosome_length = chromosome_length
        print ('Initial population: ' + str(self.initial_population))

    # Determine fitness of chromosome by looking at element 6
    def current_fitness(self,elem):
        return elem[6]

    # Sort the chromosomes in the population by descending order of the fitness value
    def sort_by_fitness(self,current_population):
        current_population.sort(reverse = True,key = self.current_fitness)
        return current_population

    # Select parents from the sorted population
    def selection(self,current_population):
        fitness_list = []
        for chromosome_index in range(6):
            chromosome = current_population[chromosome_index]

            # Select parents with fitness less than 20
            # This allows chromosomes with lower fitness to be selected as well

            if chromosome[6] < 20:
                fitness_list.append(chromosome)

        if len(fitness_list) > 2:
            p1 = fitness_list[0]
            p2 = fitness_list[1]
            early_stop = False

        # If all chromosomes have fitness more than 20,
        # select the two parents with the highest fitness value.
        # early_stop value can be used to stop the algorithm

        else:
            p1 = current_population[0]
            p2 = current_population[1]
            early_stop = True

        return p1,p2,early_stop

    # Determine the crossover sites for the parents and creates offspring
    def crossover(self,p1,p2):
        crossover_site = random.randint(1,5)
        ch1 = p1[0:crossover_site]+p2[crossover_site:self.chromosome_length]
        ch1.append(p1[6])
        ch2 = p2[0:crossover_site]+p1[crossover_site:self.chromosome_length]
        ch2.append(p2[6])

        return ch1,ch2

    # Randomly change the values of genes depending on the mutation rate
    def mutation(self,chromosome,mutatation_rate):
        mutated_gene_list = []
        no_of_mutating_genes = math.floor(mutatation_rate*self.chromosome_length)

        while True:

            if no_of_mutating_genes == 0:
                break

            # Randomly select a gene from genes 0 to 5 to mutate
            random_gene_to_mutate = random.randint(0, 5)

            # Check to see if this gene has already been mutated
            if mutated_gene_list.count(random_gene_to_mutate) == 0:
                # Mutate gene
                if chromosome[random_gene_to_mutate] == 0:
                    chromosome[random_gene_to_mutate] = 1
                else:
                    chromosome[random_gene_to_mutate] = 0

                # Decrease genes to mutate counter
                no_of_mutating_genes = no_of_mutating_genes-1

                # Add the gene to the mutated gene list
                mutated_gene_list.append(random_gene_to_mutate)

        return chromosome

    # Generate a new population with current parameters
    def generate_new_population(self):
        current_population = self.initial_population
        sorted_current_population = self.sort_by_fitness(current_population)
        selected_parent_1,selected_parent_2,early_stop = self.selection(sorted_current_population)
        generated_child_1,generated_child_2 = self.crossover(selected_parent_1,selected_parent_2)
        mutated_child_1 = self.mutation(generated_child_1,self.MUTATION_RATE)
        mutated_child_2 = self.mutation(generated_child_2,self.MUTATION_RATE)
        current_population[4] = mutated_child_1
        current_population[5] = mutated_child_2
        sorted_generated_population = self.sort_by_fitness(current_population)

        return sorted_generated_population

# *****************************************************************************
# Creates Player class
# *****************************************************************************

class Player(pygame.sprite.Sprite):

    # Initialize the class and the sprites
    def __init__(self,x,y):
        super().__init__()
        self.images = []
        self.images.append(pygame.image.load('Sprites/Player_Ship/Player_Ship_Idle_1.png'))
        self.images.append(pygame.image.load('Sprites/Player_Ship/Player_Ship_Idle_2.png'))
        self.images.append(pygame.image.load('Sprites/Player_Ship/Player_Ship_Idle_3.png'))
        self.images.append(pygame.image.load('Sprites/Player_Ship/Player_Ship_Idle_4.png'))
        self.images.append(pygame.image.load('Sprites/Player_Ship/Player_Ship_Idle_5.png'))
        self.images.append(pygame.image.load('Sprites/Player_Ship/Player_Ship_Moving_Left_1.png'))
        self.images.append(pygame.image.load('Sprites/Player_Ship/Player_Ship_Moving_Left_2.png'))
        self.images.append(pygame.image.load('Sprites/Player_Ship/Player_Ship_Moving_Left_3.png'))
        self.images.append(pygame.image.load('Sprites/Player_Ship/Player_Ship_Moving_Left_4.png'))
        self.images.append(pygame.image.load('Sprites/Player_Ship/Player_Ship_Moving_Left_5.png'))
        self.images.append(pygame.image.load('Sprites/Player_Ship/Player_Ship_Moving_Right_1.png'))
        self.images.append(pygame.image.load('Sprites/Player_Ship/Player_Ship_Moving_Right_2.png'))
        self.images.append(pygame.image.load('Sprites/Player_Ship/Player_Ship_Moving_Right_3.png'))
        self.images.append(pygame.image.load('Sprites/Player_Ship/Player_Ship_Moving_Right_4.png'))
        self.images.append(pygame.image.load('Sprites/Player_Ship/Player_Ship_Moving_Right_5.png'))
        self.index = 0
        self.image = self.images[self.index]
        self.rect = pygame.Rect(x,y,self.image.get_rect()[2],self.image.get_rect()[3])

    # Update function is called once every frame
    def update(self,surface):
        # Check left/right arrow key pressed
        key = pygame.key.get_pressed()

        if key[pygame.K_LEFT]:
            # Change index for animation of sprite moving left
            self.index += 1

            if self.index > 9 or self.index < 5:
                self.index = 5

            # Move sprite to the left
            self.rect.x = self.rect.x - 2

            # Stop sprite from moving off screen left
            if self.rect.x < 0:
                self.rect.x = 0



        elif key[pygame.K_RIGHT]:
            # Change index for animation of sprite moving right
            self.index += 1

            if self.index >=  len(self.images) or self.index < 10 :
                self.index = 10

            # Move sprite to the right
            self.rect.x = self.rect.x + 2

            # Stop sprite from moving off screen right
            if self.rect.x > 960:
                self.rect.x = 960

        else:
            # Change index for animation of sprite moving forward
            self.index += 1

            if self.index > 4:
                self.index = 0

        # Assign index of sprite
        self.image = self.images[self.index]

# *****************************************************************************
# Creates Player Projectile class
# *****************************************************************************

class Player_Projectile(pygame.sprite.Sprite):

    # Initialize the class and the sprites
    def __init__(self,player_projectile_x,player_projectile_y):
        super().__init__()
        self.images = []
        self.images.append(pygame.image.load('Sprites/Player_Ship/Missile_3_Flying_000.png'))
        self.images.append(pygame.image.load('Sprites/Player_Ship/Missile_3_Flying_001.png'))
        self.images.append(pygame.image.load('Sprites/Player_Ship/Missile_3_Flying_002.png'))
        self.images.append(pygame.image.load('Sprites/Player_Ship/Missile_3_Flying_003.png'))
        self.images.append(pygame.image.load('Sprites/Player_Ship/Missile_3_Flying_004.png'))
        self.images.append(pygame.image.load('Sprites/Player_Ship/Missile_3_Flying_005.png'))
        self.images.append(pygame.image.load('Sprites/Player_Ship/Missile_3_Flying_006.png'))
        self.images.append(pygame.image.load('Sprites/Player_Ship/Missile_3_Flying_007.png'))
        self.images.append(pygame.image.load('Sprites/Player_Ship/Missile_3_Flying_008.png'))
        self.images.append(pygame.image.load('Sprites/Player_Ship/Missile_3_Flying_009.png'))
        self.images.append(pygame.image.load('Sprites/Player_Ship/Missile_3_Explosion_000.png'))
        self.images.append(pygame.image.load('Sprites/Player_Ship/Missile_3_Explosion_001.png'))
        self.images.append(pygame.image.load('Sprites/Player_Ship/Missile_3_Explosion_002.png'))
        self.images.append(pygame.image.load('Sprites/Player_Ship/Missile_3_Explosion_003.png'))
        self.images.append(pygame.image.load('Sprites/Player_Ship/Missile_3_Explosion_004.png'))
        self.images.append(pygame.image.load('Sprites/Player_Ship/Missile_3_Explosion_005.png'))
        self.images.append(pygame.image.load('Sprites/Player_Ship/Missile_3_Explosion_006.png'))
        self.images.append(pygame.image.load('Sprites/Player_Ship/Missile_3_Explosion_007.png'))
        self.images.append(pygame.image.load('Sprites/Player_Ship/Missile_3_Explosion_008.png'))
        self.index = 0
        self.image = self.images[self.index]
        self.rect = pygame.Rect(player_projectile_x,player_projectile_y,self.image.get_rect()[2],self.image.get_rect()[3])

    # Update function is called once every frame
    def update(self,surface):
        # Change index for animation of projectile moving forward
        self.index += 1

        if self.index > 9:
            self.index = 0

        # Move sprite forward
        self.rect.y = self.rect.y - 2

        # Assign index of sprite
        self.image = self.images[self.index]

    # Called once a player projectile hits enemy
    def player_projectile_explosion(self):
        # Draws an explosion on the location of collision
        self.index = 15
        self.image = self.images[self.index]
        self.rect.x = self.rect.x - 25
        self.rect.y = self.rect.y - 20
        player_projectile_list.draw(screen)
        pygame.display.update()

# *****************************************************************************
# Creates Enemy Ship class
# *****************************************************************************

class Enemy_Ship(pygame.sprite.Sprite):

    # Initialize the class and the sprites
    def __init__(self,chromosome,enemy_ship_x,enemy_ship_y,enemy_ship_tag):
        super().__init__()
        self.images = []
        self.move_enemy = False
        self.move_left = True
        self.enemy_fire_timer = pygame.time.get_ticks()
        self.enemy_survive_timer = pygame.time.get_ticks()
        self.chaingun_enemy = False
        self.bottom_shield = None
        self.top_shield = None
        self.left_shield = None
        self.right_shield = None
        self.enemy_ship_tag = enemy_ship_tag
        self.chromosome = chromosome
        self.fitness_value = self.chromosome[6]

        # Give enemy ability to shoot back
        if self.chromosome[0] == 1:
            self.chaingun_enemy = True

        # Give enemy ability to move
        if self.chromosome[1] == 1:
            self.move_enemy = True

        # Give enemy bottom shield
        if self.chromosome[2] == 1:
            bottom_shield = Enemy_Shields(0, enemy_ship_x+10, enemy_ship_y+65, chromosome,self.enemy_ship_tag)
            all_sprites_list.add(bottom_shield)
            enemy_shield_list.add(bottom_shield)
            self.bottom_shield = bottom_shield

        # Give enemy top shield
        if self.chromosome[3] == 1:
            top_shield = Enemy_Shields(1,enemy_ship_x+10,enemy_ship_y-10,chromosome,self.enemy_ship_tag)
            all_sprites_list.add(top_shield)
            enemy_shield_list.add(top_shield)
            self.top_shield = top_shield

        # Give enemy left shield
        if self.chromosome[4] == 1:
            left_shield = Enemy_Shields(2,enemy_ship_x-15,enemy_ship_y-10,chromosome,self.enemy_ship_tag)
            all_sprites_list.add(left_shield)
            enemy_shield_list.add(left_shield)
            self.left_shield = left_shield

        # Give enemy right shield
        if self.chromosome[5] == 1:
            right_shield = Enemy_Shields(3,enemy_ship_x+110,enemy_ship_y-10,chromosome,self.enemy_ship_tag)
            all_sprites_list.add(right_shield)
            enemy_shield_list.add(right_shield)
            self.right_shield = right_shield

        self.images.append(pygame.image.load('Sprites/Enemy_Ship/Enemy_Ship.png'))
        self.images.append(pygame.image.load('Sprites/Enemy_Ship/Ship6_Explosion_000.png'))
        self.images.append(pygame.image.load('Sprites/Enemy_Ship/Ship6_Explosion_004.png'))
        self.images.append(pygame.image.load('Sprites/Enemy_Ship/Ship6_Explosion_005.png'))
        self.images.append(pygame.image.load('Sprites/Enemy_Ship/Ship6_Explosion_007.png'))
        self.images.append(pygame.image.load('Sprites/Enemy_Ship/Ship6_Explosion_009.png'))
        self.images.append(pygame.image.load('Sprites/Enemy_Ship/Ship6_Explosion_011.png'))
        self.images.append(pygame.image.load('Sprites/Enemy_Ship/Ship6_Explosion_013.png'))
        self.images.append(pygame.image.load('Sprites/Enemy_Ship/Ship6_Explosion_016.png'))
        self.images.append(pygame.image.load('Sprites/Enemy_Ship/Ship6_Explosion_017.png'))
        self.images.append(pygame.image.load('Sprites/Enemy_Ship/Ship6_Explosion_019.png'))
        self.images.append(pygame.image.load('Sprites/Enemy_Ship/Ship6_Explosion_021.png'))
        self.index = 0
        self.image = self.images[self.index]
        self.rect = pygame.Rect(enemy_ship_x,enemy_ship_y,self.image.get_rect()[2]-10,self.image.get_rect()[3]-25)

    # Update function is called once every frame
    def update(self,screen):
        global ENEMY_MISSILE_TIMER

        # Change index for animation of projectile moving forward
        self.index += 1

        # Move enemy left/right depending on the location of the sprite on screen
        if self.move_enemy == True:
            if self.move_left == True:
                # Stop sprite from moving off screen left
                if self.rect.x < 15:
                    self.move_left = False

                self.rect.x = self.rect.x - 3

            else:
                # Stop sprite from moving off screen right
                if self.rect.x > 890:
                    self.move_left = True

                self.rect.x = self.rect.x + 3

        # Fire projectiles at a time interval if enemy can shoot
        # This time interval decreases as game difficulty increases
        if pygame.time.get_ticks() - self.enemy_fire_timer >= ENEMY_MISSILE_TIMER and self.chaingun_enemy == True:
            enemy_projectile = Enemy_Projectile(self.enemy_ship_tag,self.rect.x+75,self.rect.y+75)
            enemy_projectile_list.add(enemy_projectile)
            all_sprites_list.add(enemy_projectile)
            self.enemy_fire_timer = pygame.time.get_ticks()

        # Increase the fitness value of enemies survived for more than 5 seconds
        # The longer the enemy survives, the higher the fitness
        if pygame.time.get_ticks() - self.enemy_survive_timer >= 5000:
            self.fitness_value = self.fitness_value + 2
            self.chromosome[6] = self.fitness_value
            self.enemy_survive_timer = pygame.time.get_ticks()

    # Called when player projectile hits enemy or enemy projectile hits player
    def update_fitness(self,Message):
        global GENERATE_GAME_OBJECTS

        # When player projectile hits enemy shield
        if Message == 'Shield_Hit':
            # Reduce fitness value by one and assign new fitness to chromosome
            self.fitness_value = self.fitness_value - 1

            if self.fitness_value < 0:
                self.fitness_value = 0

            self.chromosome[6] = self.fitness_value

        # When player projectile hits enemy
        elif Message == 'Enemy_Hit':
            # Destroy shields of enemy hit
            shield_type_list = [self.bottom_shield,self.top_shield,self.left_shield,self.right_shield]

            for shield in shield_type_list:
                if enemy_shield_list.has(shield):
                    enemy_shield_list.remove(shield)
                    all_sprites_list.remove(shield)

            # Reduce fitness value by two and assign new fitness to chromosome
            self.fitness_value = self.fitness_value - 2

            if self.fitness_value < 0:
                self.fitness_value = 0

            self.chromosome[6] = self.fitness_value

            # Regenerate game objects if all enemies are destroyed
            if len(enemy_list) == 0:
                GENERATE_GAME_OBJECTS = True

        # When enemy projectile hits player
        elif Message == 'Player_Hit':
            # Increase fitness value by two and assign new fitness to chromosome
            self.fitness_value = self.fitness_value+4
            self.chromosome[6] = self.fitness_value

            # Regenerate game objects if player is destroyed
            GENERATE_GAME_OBJECTS = True

# *****************************************************************************
# Creates Enemy Shields class
# *****************************************************************************

class Enemy_Shields(pygame.sprite.Sprite):

    # Initialize the class and the sprites
    def __init__(self,shield_index,shield_x,shield_y,chromosome,enemy_ship_tag):
        super().__init__()
        self.images = []
        self.move_enemy = False
        self.move_left = True
        self.shield_index = shield_index
        self.enemy_ship_tag = enemy_ship_tag

        # Give enemy ability to move
        if chromosome[1] == 1:
            self.move_enemy = True

        self.images.append(pygame.image.load('Sprites/Enemy_Ship/Enemy_shield_bottom.png'))
        self.images.append(pygame.image.load('Sprites/Enemy_Ship/Enemy_shield_top.png'))
        self.images.append(pygame.image.load('Sprites/Enemy_Ship/Enemy_shield_left.png'))
        self.images.append(pygame.image.load('Sprites/Enemy_Ship/Enemy_shield_right.png'))
        self.index = shield_index
        self.image = self.images[self.index]
        self.rect = pygame.Rect(shield_x,shield_y,self.image.get_rect()[2],self.image.get_rect()[3])

    # Update function is called once every frame
    def update(self,surface):

        # Move enemy shield left/right depending on the location of the sprite on screen
        if self.move_enemy == True:
            if self.move_left == True:
                if self.shield_index == 2 and self.rect.x < 0:
                    self.move_left = False

                elif self.shield_index == 3 and self.rect.x < 125:
                    self.move_left = False

                elif (self.shield_index == 0 or self.shield_index == 1) and self.rect.x < 25:
                    self.move_left = False

                self.rect.x = self.rect.x - 3

            else:
                if self.shield_index == 2 and self.rect.x > 874:
                    self.move_left = True

                elif self.shield_index == 3 and self.rect.x > 999:
                    self.move_left = True

                elif (self.shield_index == 0 or self.shield_index == 1) and self.rect.x > 899:
                    self.move_left = True

                self.rect.x = self.rect.x + 3

# *****************************************************************************
# Creates Enemy Projectile class
# *****************************************************************************

class Enemy_Projectile(pygame.sprite.Sprite):

    # Initialize the class and the sprites
    def __init__(self,enemy_ship_tag,enemy_projectile_x,enemy_projectile_y):
        super().__init__()
        self.images = []
        self.enemy_ship_tag = enemy_ship_tag
        self.images.append(pygame.image.load('Sprites/Enemy_Ship/Missile_1_Flying_000.png'))
        self.images.append(pygame.image.load('Sprites/Enemy_Ship/Missile_1_Flying_001.png'))
        self.images.append(pygame.image.load('Sprites/Enemy_Ship/Missile_1_Flying_002.png'))
        self.images.append(pygame.image.load('Sprites/Enemy_Ship/Missile_1_Flying_003.png'))
        self.images.append(pygame.image.load('Sprites/Enemy_Ship/Missile_1_Flying_004.png'))
        self.images.append(pygame.image.load('Sprites/Enemy_Ship/Missile_1_Flying_005.png'))
        self.images.append(pygame.image.load('Sprites/Enemy_Ship/Missile_1_Flying_006.png'))
        self.images.append(pygame.image.load('Sprites/Enemy_Ship/Missile_1_Flying_007.png'))
        self.images.append(pygame.image.load('Sprites/Enemy_Ship/Missile_1_Flying_008.png'))
        self.images.append(pygame.image.load('Sprites/Enemy_Ship/Missile_1_Flying_009.png'))
        self.images.append(pygame.image.load('Sprites/Enemy_Ship/Missile_1_Explosion_000.png'))
        self.images.append(pygame.image.load('Sprites/Enemy_Ship/Missile_1_Explosion_001.png'))
        self.images.append(pygame.image.load('Sprites/Enemy_Ship/Missile_1_Explosion_002.png'))
        self.images.append(pygame.image.load('Sprites/Enemy_Ship/Missile_1_Explosion_003.png'))
        self.images.append(pygame.image.load('Sprites/Enemy_Ship/Missile_1_Explosion_004.png'))
        self.images.append(pygame.image.load('Sprites/Enemy_Ship/Missile_1_Explosion_005.png'))
        self.images.append(pygame.image.load('Sprites/Enemy_Ship/Missile_1_Explosion_006.png'))
        self.images.append(pygame.image.load('Sprites/Enemy_Ship/Missile_1_Explosion_007.png'))
        self.images.append(pygame.image.load('Sprites/Enemy_Ship/Missile_1_Explosion_008.png'))
        self.index = 0
        self.image = self.images[self.index]
        self.rect = pygame.Rect(enemy_projectile_x,enemy_projectile_y,self.image.get_rect()[2],self.image.get_rect()[3])

    # Update function is called once every frame
    def update(self,surface):
        # Change index for animation of projectile moving forward
        self.index += 1

        if self.index > 9:
            self.index = 0

        # Move sprite forward
        self.rect.y = self.rect.y + 2

        # Assign index of sprite
        self.image = self.images[self.index]

    # Called once an enemy projectile hits player
    def enemy_projectile_explosion(self):
        # Draws an explosion on the location of collision
        self.index = 15
        self.rect.x = self.rect.x-25
        self.rect.y = self.rect.y
        self.image = self.images[self.index]
        enemy_projectile_list.draw(screen)
        pygame.display.update()

# *****************************************************************************
# Creates Star Field class
# *****************************************************************************

class Star_Field(pygame.sprite.Sprite):

    # Initialize the class and the sprites
    def __init__(self,star_pos_x,star_pos_y):
        super().__init__()
        self.images = []
        self.images.append(pygame.image.load('Sprites/Star_Field/star.png'))
        self.index = 0
        self.image = self.images[self.index]
        self.rect = pygame.Rect(star_pos_x,star_pos_y, self.image.get_rect()[2],
                                self.image.get_rect()[3])

    # Update function is called once every frame
    def update(self,surface):
        # Move sprite forward
        self.rect.y = self.rect.y + 2

        # Detroy game object once it is out of screen
        if self.rect.y > 768:
            star_field_list.remove(self)

# Start game clock to synchronize events
clock = pygame.time.Clock()

# *****************************************************************************
# Called when Start Game is selected from Main Menu
# *****************************************************************************

def play_function():
    # Global variables
    global RUN_GAME
    global GENERATE_GAME_OBJECTS
    global clock
    global STAR_FIELD_TIMER
    global EPISODE_COUNT
    global PLAYER_TORPEDO_FIRING_RATE
    global MUTATION_RATE
    global COLOR_BLACK

    # Disable and reset Main Menu
    main_menu.disable()
    main_menu.reset(1)

    #Initialize variables
    EPISODE_COUNT = 0
    GENERATE_GAME_OBJECTS = True
    current_enemy_population = initial_population

    # Run Game loop
    while RUN_GAME:
        # Set Frame Rate to 60 FPS
        clock.tick(60)

        if GENERATE_GAME_OBJECTS == True:
            # Clear existing game objects
            player_list.empty()
            all_sprites_list.empty()
            player_projectile_list.empty()
            enemy_projectile_list.empty()
            enemy_list.empty()
            enemy_shield_list.empty()

            # Print Episode no and Mutation Rate on screen
            episode_info_count = episode_info_text.render('Episode:'+str(EPISODE_COUNT), 1, COLOR_WHITE)
            episode_info_mutation_rate = episode_info_text.render('Mutation Rate:'+str(MUTATION_RATE), 1, COLOR_WHITE)
            EPISODE_COUNT = EPISODE_COUNT + 1

            # Generating game objects and necessary sprite groups
            genetic_algorithm = Genetic_Algorithm(current_enemy_population, MUTATION_RATE, chromosome_length)
            generated_population = genetic_algorithm.generate_new_population()
            player = Player(512, 650)
            selected_chromosome_list=[]
            no_of_chromosomes_to_be_selected=4

            # Selecting 4 unique chromosome indices from a population of 6
            # This loop runs until four unique chromosome indices are selected
            while True:

                if no_of_chromosomes_to_be_selected == 0:
                    break

                selected_chromosome_index=random.randint(0, 5)

                if selected_chromosome_list.count(selected_chromosome_index) == 0:
                    selected_chromosome_list.append(selected_chromosome_index)
                    no_of_chromosomes_to_be_selected = no_of_chromosomes_to_be_selected -1

            enemy0 = Enemy_Ship(generated_population[selected_chromosome_list[0]], 100, 10, 0)
            enemy1 = Enemy_Ship(generated_population[selected_chromosome_list[1]], 600, 140, 1)
            enemy2 = Enemy_Ship(generated_population[selected_chromosome_list[2]], 200, 270, 2)
            enemy3 = Enemy_Ship(generated_population[selected_chromosome_list[3]], 800, 400, 3)
            enemy_ship_list = [enemy0, enemy1, enemy2, enemy3]
            player_list.add(player)
            all_sprites_list.add(player)
            all_sprites_list.add(enemy0)
            all_sprites_list.add(enemy1)
            all_sprites_list.add(enemy2)
            all_sprites_list.add(enemy3)
            enemy_list.add(enemy0)
            enemy_list.add(enemy1)
            enemy_list.add(enemy2)
            enemy_list.add(enemy3)

            GENERATE_GAME_OBJECTS = False

        # Check for Pygame events
        playevents = pygame.event.get()
        for event in playevents:

            # Exit game if window is closed
            if event.type == pygame.QUIT:
                RUN_GAME = False
                exit()

            # Check if Space Bar is pressed
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:

                # Fire no of projectiles according to player firing rate
                # Player firing rate decreases as game difficulty increases
                if len(player_projectile_list) < PLAYER_TORPEDO_FIRING_RATE:
                    player_projectile = Player_Projectile(player.rect.x + 25, player.rect.y - 35)
                    all_sprites_list.add(player_projectile)
                    player_projectile_list.add(player_projectile)

            # If Esc key is pressed, enable Main Menu and remove game objects from screen
            if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE and main_menu.is_disabled():
                main_menu.enable()
                GENERATE_GAME_OBJECTS = False

                # Exit this function and return to Main Loop on line 931
                return

        # Pass Pygame event to Main Menu
        main_menu.mainloop(playevents)

        # Generate the Star Field
        # Creates Star sprites at random points on the screen
        if pygame.time.get_ticks() - STAR_FIELD_TIMER >= 500:
            for star in range(10):
                star_x = random.randint(1, 1020)
                star_y = random.randint(-1000, 0)
                star0 = Star_Field(star_x, star_y)
                star_field_list.add(star0)
            STAR_FIELD_TIMER = pygame.time.get_ticks()

        # Draw screen background and episode info
        screen.fill(COLOR_BLACK)
        screen.blit(episode_info_count, (850,5))
        screen.blit(episode_info_mutation_rate, (850, 30))

        # Call update functions of the sprite groups
        star_field_list.update(screen)
        all_sprites_list.update(screen)

        # Check all the player projectiles for collisions with enemy
        for projectile in player_projectile_list:
            # If a projectile hits enemy or shield,
            # 1. call relevant fitness update functions
            # 2. draw explosion
            # 3. remove colliding game objects from screen
            # Tags are used to identify which object was hit
            player_projectile_hit_enemy_list = pygame.sprite.spritecollide(projectile, enemy_list, True)
            player_projectile_hit_enemy_shield_list = pygame.sprite.spritecollide(projectile, enemy_shield_list, True)

            for enemy_hit in player_projectile_hit_enemy_list:
                enemy_hit.update_fitness("Enemy_Hit")
                projectile.player_projectile_explosion()
                player_projectile_list.remove(projectile)
                all_sprites_list.remove(projectile)

            for shield_hit in player_projectile_hit_enemy_shield_list:
                shield_enemy_list = enemy_ship_list
                projectile.player_projectile_explosion()
                for enemy in shield_enemy_list:
                    if enemy.enemy_ship_tag == shield_hit.enemy_ship_tag:
                        enemy.update_fitness("Shield_Hit")

                player_projectile_list.remove(projectile)
                all_sprites_list.remove(projectile)

            # Remove player projectile if it is off screen
            if projectile.rect.y < -20:
                player_projectile_list.remove(projectile)
                all_sprites_list.remove(projectile)

        # Check all the enemy projectiles for collisions with player
        for enemy_projectile in enemy_projectile_list:
            enemy_projectile_hit_list = pygame.sprite.spritecollide(enemy_projectile, player_list, True)

            # If a projectile hits player,
            # 1. draw explosion
            # 2. call relevant fitness update functions
            # 3. remove colliding game objects from screen
            for player_hit in enemy_projectile_hit_list:
                enemy_projectile.enemy_projectile_explosion()
                firing_enemy_list = enemy_ship_list

                for enemy in firing_enemy_list:
                    if enemy.enemy_ship_tag == enemy_projectile.enemy_ship_tag:
                        enemy.update_fitness("Player_Hit")

                enemy_projectile_list.remove(enemy_projectile)
                all_sprites_list.remove(enemy_projectile)

            # Remove enemy projectile if it is off screen
            if enemy_projectile.rect.y > 768:
                enemy_projectile_list.remove(enemy_projectile)
                all_sprites_list.remove(enemy_projectile)

        # Draw relevant sprite groups on screen and update
        star_field_list.draw(screen)
        all_sprites_list.draw(screen)
        pygame.display.update()


# Used by menus to fill background color
def main_background():
    screen.fill(COLOR_BACKGROUND)

# Change game difficulty
# Player firing rate and enemy firing rate will change according to difficulty
def change_game_difficulty(d):
    global PLAYER_TORPEDO_FIRING_RATE
    global ENEMY_MISSILE_TIMER

    GAME_DIFFICULTY[0] = d
    if GAME_DIFFICULTY[0]=='EASY':
        PLAYER_TORPEDO_FIRING_RATE = 5
        ENEMY_MISSILE_TIMER = 5000

    elif GAME_DIFFICULTY[0]=='MEDIUM':
        PLAYER_TORPEDO_FIRING_RATE = 3
        ENEMY_MISSILE_TIMER = 3000

    elif GAME_DIFFICULTY[0]=='HARD':
        PLAYER_TORPEDO_FIRING_RATE = 1
        ENEMY_MISSILE_TIMER = 1000

# Change mutation rate of the algorithm
def change_mutation_rate(d):
    global MUTATION_RATE

    MUTATION_RATE_MATRIX[0] = d
    MUTATION_RATE = MUTATION_RATE_MATRIX[0]

# Main Menu of the game
main_menu = pygameMenu.Menu(screen,
                            bgfun = main_background,
                            color_selected = COLOR_RED,
                            font = pygameMenu.fonts.FONT_BEBAS,
                            font_color = COLOR_BLACK,
                            font_size = 30,
                            menu_alpha = 50,
                            menu_color = MENU_BACKGROUND_COLOR,
                            menu_color_title = COLOR_BLUE,
                            menu_height = int(SCREEN_HEIGHT * 0.6),
                            menu_width = int(SCREEN_WIDTH * 0.6),
                            onclose = PYGAME_MENU_DISABLE_CLOSE,
                            option_shadow = False,
                            title = 'Main menu',
                            window_height = SCREEN_HEIGHT,
                            window_width = SCREEN_WIDTH
                            )

# About Menu where players can see information about the game
about_menu = pygameMenu.TextMenu(screen,
                                 bgfun = main_background,
                                 color_selected = COLOR_RED,
                                 font = pygameMenu.fonts.FONT_BEBAS,
                                 font_color = COLOR_BLACK,
                                 font_size_title = 30,
                                 font_title = pygameMenu.fonts.FONT_8BIT,
                                 menu_alpha = 50,
                                 menu_color = MENU_BACKGROUND_COLOR,
                                 menu_color_title = COLOR_BLUE,
                                 menu_height = int(SCREEN_HEIGHT * 0.6),
                                 menu_width = int(SCREEN_WIDTH * 0.6),
                                 onclose = PYGAME_MENU_DISABLE_CLOSE,
                                 option_shadow = False,
                                 text_color = COLOR_BLACK,
                                 text_fontsize = 20,
                                 title = 'About',
                                 window_height = SCREEN_HEIGHT,
                                 window_width = SCREEN_WIDTH
                                 )

# Help Menu where players can see information about game controls
help_menu = pygameMenu.TextMenu(screen,
                                 bgfun = main_background,
                                 color_selected = COLOR_RED,
                                 font = pygameMenu.fonts.FONT_BEBAS,
                                 font_color = COLOR_BLACK,
                                 font_size_title = 30,
                                 font_title = pygameMenu.fonts.FONT_8BIT,
                                 menu_alpha = 50,
                                 menu_color = MENU_BACKGROUND_COLOR,
                                 menu_color_title = COLOR_BLUE,
                                 menu_height = int(SCREEN_HEIGHT * 0.6),
                                 menu_width = int(SCREEN_WIDTH * 0.6),
                                 onclose = PYGAME_MENU_DISABLE_CLOSE,
                                 option_shadow = False,
                                 text_color = COLOR_BLACK,
                                 text_fontsize = 20,
                                 title = 'Help',
                                 window_height = SCREEN_HEIGHT,
                                 window_width = SCREEN_WIDTH
                                 )

# Play Menu where players can change game difficulty and mutation rate
play_menu = pygameMenu.Menu(screen,
                            bgfun = main_background,
                            color_selected = COLOR_RED,
                            font = pygameMenu.fonts.FONT_BEBAS,
                            font_color = COLOR_BLACK,
                            font_size = 30,
                            menu_alpha = 50,
                            menu_color = MENU_BACKGROUND_COLOR,
                            menu_color_title = COLOR_BLUE,
                            menu_height = int(SCREEN_HEIGHT * 0.6),
                            menu_width = int(SCREEN_WIDTH * 0.6),
                            onclose = PYGAME_MENU_DISABLE_CLOSE,
                            option_shadow = False,
                            title = 'Play menu',
                            window_height = SCREEN_HEIGHT,
                            window_width = SCREEN_WIDTH
                            )

# Calls play_function when Start Game is pressed
play_menu.add_option('Start Game', play_function)

# Selector to select game dificulty
# On change calls change_game_difficulty function
play_menu.add_selector('Select Game Difficulty', [('Easy', 'EASY'),
                                             ('Medium', 'MEDIUM'),
                                             ('Hard', 'HARD')],
                       onreturn = None,
                       onchange = change_game_difficulty)

# Selector to select mutation rate
# On change calls change_mutation_rate function
play_menu.add_selector('Select Mutation Rate', [('0.2', 0.2),
                                             ('0.4', 0.4),
                                             ('0.6', 0.6),
                                             ('0.8', 0.8),],
                       onreturn = None,
                       onchange = change_mutation_rate)

# Return to Main Menu when this option is selected
play_menu.add_option('Return to main menu', PYGAME_MENU_BACK)

# Adding options to the Main Menu
main_menu.add_option('Play Game', play_menu)
main_menu.add_option('Help', help_menu)
main_menu.add_option('About', about_menu)
main_menu.add_option('Quit', PYGAME_MENU_EXIT)

# Write the game info on About Menu
for line in ABOUT:
    about_menu.add_line(line)
about_menu.add_line(PYGAMEMENU_TEXT_NEWLINE)

# Return to Main Menu when this option is selected
about_menu.add_option('Return to main menu', PYGAME_MENU_BACK)

# Write the game controls info on Help Menu
for line in HELP:
    help_menu.add_line(line)
help_menu.add_line(PYGAMEMENU_TEXT_NEWLINE)

# Return to Main Menu when this option is selected
help_menu.add_option('Return to main menu', PYGAME_MENU_BACK)

# Main loop of the program
while True:

    # Set Frame Rate to 60 FPS
    clock.tick(60)

    # Check for Pygame events
    events = pygame.event.get()
    # Exit game if window is closed
    for event in events:
        if event.type == pygame.QUIT:
            exit()

    # Pass Pygame event to Main Menu
    main_menu.mainloop(events)

    # Update screen
    pygame.display.update()


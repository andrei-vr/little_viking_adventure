from constants import *
from functions import *

from pygame import *
import pygame
import pyganim
import re
import os
import math

class Goblin(sprite.Sprite):

    # Control FSM states
    STATE_IDLE = 0
    STATE_ALARMED = 1
    STATE_ATTACKING = 2
    STATE_FLEEING = 3
    STATE_DEAD = 4

    def __init__(self, current_level, x, y):
        sprite.Sprite.__init__(self)

        # Setup image and rectangle
        self.image = Surface((BLOCK_SIZE, BLOCK_SIZE))
        self.image.fill(Color(TP_COLOR))
        self.image.set_colorkey(Color(TP_COLOR))  # make the background transparent

        self.rect = Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
        self.collide_rect = Rect(x + BLOCK_SIZE/2 - GOB_HITBOX_WIDTH/2,
                                 y + BLOCK_SIZE/2 - GOB_HITBOX_HEIGHT/2,
                                 GOB_HITBOX_WIDTH, GOB_HITBOX_HEIGHT) # This rect is for collision detection

        # Starting values
        self.hp = 1
        self.vel_x = 0   # x velocity
        self.vel_y = 0   # y velocity
        self.current_level = current_level
        self.current_speed = 0
        self.radius = 250
        self.state = self.STATE_IDLE
        self.next_state = self.STATE_IDLE
        self.angle = 0
        self.last_angle = 0

        # Create standing animation
        self.anim_standing = pyganim.PygAnimation(get_list_of_frames('goblin', 'standing'))
        self.anim_standing.play()
        self.anim_standing.blit(self.image, (0, 0))  # Default animation

        # Create running animation
        self.anim_running = pyganim.PygAnimation(get_list_of_frames('goblin', 'running'))
        self.anim_running.play()

        # Create fighting animation
        self.anim_fighting = pyganim.PygAnimation(get_list_of_frames('goblin', 'fighting'))
        self.anim_fighting.play()

        # Create dying animation
        self.anim_dying = pyganim.PygAnimation(get_list_of_frames('goblin', 'dying'))

        # Load alarmed sound
        path = os.path.join( GAME_FOLDER, 'sounds', 'goblin_alarmed.wav')
        self.alarmed_sound = pygame.mixer.Sound(path)

        # Load attacking sound
        path = os.path.join( GAME_FOLDER, 'sounds', 'goblin_attack.wav')
        self.attack_sound = pygame.mixer.Sound(path)

    def collide(self, walls, dt):
        for w in walls:
            if self.collide_rect.colliderect(w.rect):
                if self.vel_x > 0:
                    self.rect.centerx -= self.current_speed*dt
                    self.collide_rect.centerx -= self.current_speed*dt
                if self.vel_x < 0:
                    self.rect.centerx += self.current_speed*dt
                    self.collide_rect.centerx += self.current_speed*dt
                if self.vel_y > 0:
                    self.rect.centery -= self.current_speed*dt
                    self.collide_rect.centery -= self.current_speed*dt
                if self.vel_y < 0:
                    self.rect.centery += self.current_speed*dt
                    self.collide_rect.centery += self.current_speed*dt

    def update(self, hero, ui, dt):

        self.image.fill( Color( TP_COLOR ) ) # Delete previous animation frame
        self.state = self.next_state      # Get a new state

        # --------------------------------------- IDLE STATE -----------------------------------------
        if self.state == self.STATE_IDLE:
            self.current_speed = 0
            self.vel_x = 0
            self.vel_y = 0
            self.anim_standing.blit( self.image, (0, 0) )
            if pygame.sprite.spritecollide( self, [hero], False, pygame.sprite.collide_circle): # IDLE -> ATTACKING
                self.next_state = self.STATE_ATTACKING
                self.attack_sound.play(loops=-1)
                self.alarmed_sound.play()
        # --------------------------------------- ATTACKING STATE -----------------------------------------
        elif self.state == self.STATE_ATTACKING:
            self.current_speed = GOB_RUNNING_MS
            self.anim_fighting.blit( self.image, (0, 0) )
            # Rotate the image
            self.angle = math.degrees( math.atan2( self.collide_rect.centery - hero.rect.centery, hero.rect.centerx - self.collide_rect.centerx ) )
            if (hero.rect.centerx - self.collide_rect.centerx != 0):
                self.image = rot_center( self.image, self.angle )
            self.vel_x = -int(round(self.current_speed * (math.sin(math.radians(self.angle)-90))))
            self.vel_y = -int(round(self.current_speed * (math.cos(math.radians(self.angle)-90))))
        # --------------------------------------- DEAD STATE -----------------------------------------
        elif self.state == self.STATE_DEAD:
            self.anim_dying.blit( self.image, (0, 0) )
            self.image = rot_center( self.image, self.last_angle )

        # Determine coordinates
        self.rect.centerx += self.vel_x*dt
        self.rect.centery += self.vel_y*dt
        self.collide_rect.centerx += self.vel_x*dt
        self.collide_rect.centery += self.vel_y*dt

        # Check for collision
        self.collide( self.current_level.walls, dt)

        # Check for death
        if self.hp <= 0:
            self.attack_sound.stop()
            self.next_state = self.STATE_DEAD
            self.vel_x = 0
            self.vel_y = 0
            self.last_angle = self.angle
            self.anim_dying.play()

from constants import *
from functions import *

from pygame import *
import pygame
import pyganim
import re
import os
import math

class Viking(sprite.Sprite):

    # Control FSM states
    STATE_IDLE = 0
    STATE_MOVING = 1
    STATE_ATTACKING = 2


    def __init__(self, x, y, current_level):

        sprite.Sprite.__init__(self)

        # Setup image and rectangle
        self.image = Surface((BLOCK_SIZE, BLOCK_SIZE))
        self.image.fill(Color(TP_COLOR))
        self.image.set_colorkey(Color(TP_COLOR))  # make the background transparent

        self.rect = Rect(x, y, BLOCK_SIZE, BLOCK_SIZE) # This rect is for drawing
        self.collide_rect = Rect(x + BLOCK_SIZE/2 - HERO_HITBOX_WIDTH/2,
                                 y + BLOCK_SIZE/2 - HERO_HITBOX_HEIGHT/2,
                                 HERO_HITBOX_WIDTH, HERO_HITBOX_HEIGHT) # This rect is for collision detection

        # Starting values
        self.vel_x = 0   # x velocity
        self.vel_y = 0   # y velocity
        self.angle = 0
        self.attack_mouse_x = 0 # mouse coordinates saved in the moment of attack start
        self.attack_mouse_y = 0 # to calculate attack vector in the moment of dmg dealing
        self.current_level = current_level
        self.state = self.STATE_IDLE
        self.next_state = self.STATE_IDLE

        # Load footsteps sound
        path = os.path.join( GAME_FOLDER, 'sounds', 'viking_footsteps.wav')
        self.footsteps_sound = pygame.mixer.Sound(path)

        # Load strike sound
        path = os.path.join( GAME_FOLDER, 'sounds', 'viking_strike.wav')
        self.strike_sound = pygame.mixer.Sound(path)

        # Create standing animation
        self.anim_standing = pyganim.PygAnimation(get_list_of_frames('viking', 'standing'))
        self.anim_standing.play()
        self.anim_standing.blit(self.image, (0, 0))  # Default animation

        # Create running animation
        self.anim_running = pyganim.PygAnimation(get_list_of_frames('viking', 'running'))
        self.anim_running.play()

        # Create striking animation
        self.anim_striking = pyganim.PygAnimation(get_list_of_frames('viking', 'striking'))

        # Create throwing animation
        self.anim_throwing = pyganim.PygAnimation(get_list_of_frames('viking', 'throwing'))
        self.anim_throwing.play()

    def turn(self, ui):
        if (self.state != self.STATE_ATTACKING):
            self.angle = math.degrees( math.atan2( self.collide_rect.centery - ui.mouse_y, ui.mouse_x - self.collide_rect.centerx ) )
        if (ui.mouse_x - self.collide_rect.centerx != 0):
            self.image = rot_center(self.image, self.angle)

    def collide(self, walls, dt):
        for w in walls:
            if self.collide_rect.colliderect(w.rect):
                if self.vel_x > 0:
                    self.rect.centerx -= HERO_MOVE_SPEED*dt+1
                    self.collide_rect.centerx -= HERO_MOVE_SPEED*dt+1
                if self.vel_x < 0:
                    self.rect.centerx += HERO_MOVE_SPEED*dt+1
                    self.collide_rect.centerx += HERO_MOVE_SPEED*dt+1
                if self.vel_y > 0:
                    self.rect.centery -= HERO_MOVE_SPEED*dt+1
                    self.collide_rect.centery -= HERO_MOVE_SPEED*dt+1
                if self.vel_y < 0:
                    self.rect.centery += HERO_MOVE_SPEED*dt+1
                    self.collide_rect.centery += HERO_MOVE_SPEED*dt+1

    def update(self, ui, dt):

        self.image.fill( Color( TP_COLOR ) ) # Delete previous animation frame
        self.state = self.next_state         # Get a new state

        # --------------------------------------- IDLE STATE -----------------------------------------
        if self.state == self.STATE_IDLE:
            self.vel_x = 0
            self.vel_y = 0
            self.anim_standing.blit( self.image, (0, 0) )
            if ui.attack:                                    # IDLE -> ATTACKING
                pygame.time.set_timer( ATTACK_OVER, HERO_ATTACK_TIME )
                pygame.time.set_timer( ATTACK_DMG, HERO_DMG_TIME )
                self.attack_mouse_x = ui.mouse_x
                self.attack_mouse_y = ui.mouse_y
                self.strike_sound.play()
                self.anim_striking.play()
                self.next_state = self.STATE_ATTACKING
            elif (ui.up or ui.down or ui.left or ui.right):  # IDLE -> MOVING
                self.next_state = self.STATE_MOVING
                self.footsteps_sound.play( loops=-1 )
        # --------------------------------------- MOVING STATE -----------------------------------------
        elif self.state == self.STATE_MOVING:
            self.anim_running.blit( self.image, (0, 0) )
            # Calculate speed
            if ui.left:
                self.vel_x = -HERO_MOVE_SPEED
            if ui.right:
                self.vel_x = HERO_MOVE_SPEED
            if not (ui.left or ui.right) or (ui.left and ui.right):
                self.vel_x = 0
            if ui.up:
                self.vel_y = -HERO_MOVE_SPEED
            if ui.down:
                self.vel_y = HERO_MOVE_SPEED
            if not (ui.down or ui.up) or (ui.down and ui.up):
                self.vel_y = 0
            # Calculate coordinates
            self.rect.centerx += self.vel_x*dt
            self.rect.centery += self.vel_y*dt
            self.collide_rect.centerx += self.vel_x*dt
            self.collide_rect.centery += self.vel_y*dt
            # Check for collision
            self.collide( self.current_level.walls, dt )
            if ui.attack:                                     # MOVING -> ATTACKING
                pygame.time.set_timer( ATTACK_OVER, HERO_ATTACK_TIME )
                pygame.time.set_timer( ATTACK_DMG, HERO_DMG_TIME )
                self.attack_mouse_x = ui.mouse_x
                self.attack_mouse_y = ui.mouse_y
                self.strike_sound.play()
                self.anim_striking.play()
                self.footsteps_sound.stop()
                self.next_state = self.STATE_ATTACKING
            elif not (ui.up or ui.down or ui.left or ui.right):   # MOVING -> IDLE
                self.next_state = self.STATE_IDLE
                self.footsteps_sound.stop()
        # --------------------------------------- ATTACKING STATE -----------------------------------------
        if self.state == self.STATE_ATTACKING:
            self.anim_striking.blit( self.image, (0, 0) )
            #if ui.attack_dmg:
            pygame.time.set_timer( ATTACK_DMG, 0 )
            attack_vector = (self.attack_mouse_x - self.collide_rect.centerx,
                             self.attack_mouse_y - self.collide_rect.centery)
            attack_vector_length = math.sqrt(pow(attack_vector[0], 2) + pow(attack_vector[1], 2))
            norm_attack_vector = (attack_vector[0]/attack_vector_length, attack_vector[1]/attack_vector_length)
            dmg_pixel = (int(self.collide_rect.centerx + norm_attack_vector[0]*60), int(self.collide_rect.centery + norm_attack_vector[1]*60))
            print('self: ' + str((self.collide_rect.centerx, self.collide_rect.centery)))
            print('dmg pixel: ' + str(dmg_pixel))
            for monster in self.current_level.enemies:
                if monster.collide_rect.collidepoint(dmg_pixel[0], dmg_pixel[1]):
                    monster.hp -= 1
            if ui.attack_over:                             # ATTACK -> IDLE
                self.next_state = self.STATE_IDLE
                self.anim_striking.stop()
                pygame.time.set_timer( ATTACK_OVER, 0 )

        # Turn the image
        self.turn(ui)

import pygame
import os
import math

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, range):
        super().__init__()
        self.game = game
        self.settings = self.game.settings
        self.speed = self.settings.enemy_speed
        self.screen = self.game.screen
        self.screen_rect = self.screen.get_rect()
        # enemy image lists
        self.image_names = ['blastoise_1', 'blastoise_2', 'blastoise_3', 'blastoise_4', 'blastoise_5', 'blastoise_6', 'blastoise_7', 'blastoise_8']
        self.l_imgs = [pygame.image.load(os.path.join('images', 'blastoise_walk', f'{img}.png')) for img in self.image_names]
        self.r_imgs = [pygame.transform.flip(pygame.image.load(os.path.join('images', 'blastoise_walk', f'{img}.png')), True, False) for img in self.image_names]
        # blastoise ATTACK sequence pictures (3 thru 5 are actually spraying water)
        self.attack_img_names = ['images/blastoise_walk/blastoise_attack_pics/b_pre_'+str(x)+'.png' for x in [1,2,3,4,5,6,7,8,9]]

        self.l_attack_imgs = [pygame.image.load(img) for img in self.attack_img_names]
        # attack imgs for when facing RIGHT
        self.r_attack_imgs = [pygame.transform.flip(img, True, False) for img in self.l_attack_imgs]

        # load in blastoise's close combat attack imgs (the belly bump), we'll refer to it as BUMP from here on out
        # NOTE - going to try doing a bite sequence of 4 pics instead
        # self.bump_img_names = ['images/blastoise_walk/blastoise_belly_bump/blast_bump_'+str(x)+'.png' for x in [1,2,3,4,5,6,7,8]]
        # self.l_bump_imgs = [pygame.image.load(img) for img in self.bump_img_names]
        # self.r_bump_imgs = [pygame.transform.flip(img, True, False) for img in self.l_bump_imgs]
        # now - when do I want blastoise to do this close combat attack?

        # load blastoise's bite sequence:
        self.bite_img_names = ['images/blastoise_walk/bite/b_punch_'+str(x)+'.png' for x in [1,2,3,4]]
        self.l_bite_imgs = [pygame.image.load(img) for img in self.bite_img_names]
        self.r_bite_imgs = [pygame.transform.flip(img, True, False) for img in self.l_bite_imgs]
        # bite index variable:
        self.bite_index = 0
        # if blastoise IS biting, self.biting = True
        self.biting = False
        # if enemy has just bitten, has_bitten is set to True, in 2 seconds, it's set to False, allowing him to bite again
        self.has_bitten = False

        self.images = self.l_imgs
        self.index = 0
        self.image = self.images[self.index]
        # create rect variable
        self.rect = self.image.get_rect()

        self.moving_left = True
        self.moving_right = False
        self.distance = 0
        # boolean to say if enemy is attacking (w/hydropump)
        self.attacking = False
        # facing variable
        self.facing = 'left'
        # create hydropump instance
        self.hydropump = self.HydroPump(self.game, self)
        # create instance of health meter
        self.health_meter = self.HealthBar(self.game, self)
        self.health = self.settings.enemy_max_health
        # create distance variable - range enemy will walk back/forth (left/right)
        self.range = range

        # variable to signal when enemy is in view of screen
        self.on = False
        # index variable - for the index of the attack img sequences (L/R)
        self.attack_index = 0

        # boolean to signify that PIKACHU is NEARBY, and therefore, blastoise should attack with hydropump
        self.pikachu_near = False

        # boolean for after blastoise has used hydropump:
        self.attack_wait = False

    def update(self, pikachu):
        if self.rect.left >= self.screen_rect.right:
            self.rect.x -= self.settings.scroll_speed
        # set the enemy to 'on' when they enter view (they scroll over threshold of right side of
        # screen)
        elif self.rect.left < self.screen_rect.right:
            self.on = True

        if self.on:
            self.rect.x -= self.settings.scroll_speed
            # if blastoise is 'on', then check how far away pikachu is: absolute value of self.rect-pikachu.rect
            # acceptable distance is saved into settings as 'can_see_pikachu', it's 175 right now

            pika_distance = self.rect.x-pikachu.rect.x
            # if pikachu is within the distance (in settings) - set attacking to True, and set event timer to stop
            # attacking - cannot currently be attacking either, or else blastoise would infinitely attack as long as
            # pikachu was nearby - also have to make sure blastoise isn't currently doing belly bump attack
            if abs(pika_distance) <= self.settings.can_see_pikachu and (not self.attacking) and (not self.attack_wait):
                # if pika_distance is positive, that means pikachu is to blastoise's left:
                if pika_distance >= 0:
                    self.facing = 'left'
                # if pika_distance is negative, then pikachu is to blastoise's right
                elif pika_distance <= 0:
                    self.facing = 'right'
                self.attacking = True
                pygame.time.set_timer(self.game.enemy_stop_attack, 2500, True)
            
            # now we'll check if pikachu's sprite rect is colliding with enemy sprite rect - actually we'll do this in
            # MAIN in a FUNCTION since we can use pikachu's sprite with the enemy_group sprite Group, then below, we can
            # say - if doing_bump: (since enemy.doing_bump will be set to True if pikachu's colliding and blastoise isn't
            # currently doing hydropump)



            # if (not self.attacking) and (not self.doing_bump):
            if (not self.attacking) and (not self.biting):
                if self.moving_left:
                    # if moving left, then make sure blastoise is FACING left too:
                    self.facing = 'left'
                    self.rect.x -= self.speed
                    self.distance += 1
                    if self.distance == self.range:
                        self.moving_left = False
                        self.facing = 'right'
                        self.moving_right = True
                        self.distance = 0
                elif self.moving_right:
                    # if moving right, make sure he's FACING right:
                    self.facing = 'right'
                    self.rect.x += self.speed
                    self.distance += 1
                    if self.distance == self.range:
                        self.moving_right = False
                        self.facing = 'left'
                        self.moving_left = True
                        self.distance = 0
            
            # set correct image list based on which direction self is facing, and whether self is attacking
            # if (not self.attacking) and (not self.doing_bump):
            if (not self.attacking) and (not self.biting):
                if self.facing=='right':
                    self.images = self.r_imgs
                elif self.facing=='left':
                    self.images = self.l_imgs
                # +++++++++
                self.image = self.images[self.index]
            # elif self.attacking and (not self.doing_bump):
            elif self.attacking and (not self.biting):
                if self.facing=='right':
                    self.images = self.r_attack_imgs
                elif self.facing=='left':
                    self.images = self.l_attack_imgs
                # +++++++++++
                self.image = self.images[self.attack_index]
            # a line changing self.images to the belly_bump images if doing_bump is True:
            # elif self.doing_bump:
            elif self.biting:
                if self.facing=='right':
                    self.images = self.r_bite_imgs
                elif self.facing=='left':
                    self.images = self.l_bite_imgs
                # ++++++++++++++++
                self.image = self.images[self.bite_index]
        
        # **THROW IN A FEW LINES HERE - IF IMAGES=NORMAL_IMGS AND INDEX IS TOO HIGH, SET TO 0, IF YOU'RE ATTACKING AND
        # ATTAKC_INDEX TOO HIGH, SET TO 0 - EVERY IMAGE LIST - CHECK AND SET TO 0 IF NECESSARY TO AVOID THE ERROR i'M
        # GETTING RIGHT NOW


        # update hydropump and health_meter so they all stay synched
        if self.attacking:
            self.hydropump.update(self, pikachu)
        self.health_meter.update(self)
                
    def blitme(self):
        self.screen.blit(self.image, self.rect)
        # if enemy is attacking, show the attack
        if self.attacking:
            self.hydropump.blitme()
        else:
            self.hydropump.index = 0
        # always show the health bar
        self.health_meter.blitme()

    # this function is supposed to delete the enemy sprite, and all associated sprites - the attack sprite, the health
    # bar sprite, etc., but I'm not sure if it works
    def _im_dead(self):
        self.health_meter.kill()
        self.hydropump.kill()
        pygame.sprite.Sprite.kill(self.hydropump)
        self.kill()
        pygame.sprite.Sprite.kill(self)

    # Enemy attack class (in Blastoise's case, his attack is HydroPump)
    class HydroPump(pygame.sprite.Sprite):
        def __init__(self, game, enemy_sprite):
            super().__init__()
            self.game = game
            self.screen = self.game.screen
            self.settings = self.game.settings
            self.screen_rect = self.screen.get_rect()

            self.image_names = ['blank.png','water_attack_1.png','water_attack_2.png', 'water_attack_3.png', 
                                'water_attack_4.png', 'water_attack_5.png', 'water_attack_6.png', 'water_attack_7.png', 
                                'water_attack_8.png', 'water_attack_9.png', 'water_attack_10.png', 'water_attack_11.png', 
                                'water_attack_12.png', 'water_attack_13.png', 'water_attack_14.png']
            self.l_imgs = [pygame.image.load(os.path.join('images', 'water', x)) for x in self.image_names]
            self.r_imgs = [pygame.transform.flip(pygame.image.load(os.path.join('images', 'water', x)), True, False) 
                           for x in self.image_names]
            self.images = self.l_imgs
            self.index = 0
            self.image = self.images[self.index]
            self.rect = self.image.get_rect()
            # creating a rect for hitbox - actual picture of hydropump attack is high up near blastoise's guns, but
            # hitbox should really be lower since pikachu is so short
            self.hitbox_rect = self.rect
            self.hitbox_rect.y = self.rect.y+25
            self.enemy_sprite = enemy_sprite
            if enemy_sprite.facing == 'right':
                self.rect.midleft = enemy_sprite.rect.midright
            else:
                self.rect.midright = enemy_sprite.rect.midleft

        def update(self, enemy_sprite, pikachu):
            # if enemy_sprite isn't attacking, set index to 0
            if not enemy_sprite.attacking:
                self.index = 0
            # going to try switching this to .facing == 'right' instead of moving
            # if enemy_sprite.moving_right:
            if enemy_sprite.facing == 'right' and enemy_sprite.attacking==True:
                self.image = self.r_imgs[self.index]
                self.rect = self.image.get_rect()
                self.rect.midleft = enemy_sprite.rect.midright
                
            elif enemy_sprite.facing == 'left' and enemy_sprite.attacking==True:
                self.image = self.l_imgs[self.index]
                self.rect = self.image.get_rect()
                self.rect.midright = enemy_sprite.rect.midleft
            self.rect.top = enemy_sprite.rect.top+5

            # changing the angle calculation thing to just if pikachu is alot higher than blastoise, blastoise will
            # angle the hydropump pointing upwards (30 deg)
            if (enemy_sprite.rect.y-pikachu.rect.y)>75:
                # if pikachu is to left of blastoise:
                if enemy_sprite.facing=='left':
                    self.angle = 330
                # else (if pikachu is to right of blastoise):
                elif enemy_sprite.facing=='right':
                    self.angle = 210
                self.rect.y = self.rect.y - 100
            else:
                self.angle = 0

            self.rotated_image = pygame.transform.rotate(self.image, self.angle)
            rotated_rect = self.rotated_image.get_rect()
            # make hitbox_rect = rect except lower (+25), we'll go with 25 for now:
            self.hitbox_rect = rotated_rect
            self.hitbox_rect.y = rotated_rect.y+25

        def blitme(self):

            self.screen.blit(self.rotated_image, self.rect)

    
    class HealthBar(pygame.sprite.Sprite):
        def __init__(self, game, enemy_sprite):
            super().__init__()
            # self.game = game
            self.screen = game.screen
            self.screen_rect = game.screen.get_rect()
            self.settings = game.settings
            self.enemy = enemy_sprite
            self.red = self.settings.red
            self.green = self.settings.green

            self.health_bar = pygame.Rect(self.settings.enemy_health_rect)
            self.bg_bar = pygame.Rect(self.settings.enemy_health_rect)

            self.health_bar.bottom = enemy_sprite.rect.top - 10
            self.health_bar.left = enemy_sprite.rect.left
            self.bg_bar.bottom = enemy_sprite.rect.top - 10
            self.bg_bar.left = enemy_sprite.rect.left
            self.health_bar.width = self.settings.enemy_max_health

        def update(self, enemy_sprite):
            self.health_bar.bottom = enemy_sprite.rect.top - 10
            self.health_bar.left = enemy_sprite.rect.left
            self.bg_bar.bottom = enemy_sprite.rect.top - 10
            self.bg_bar.left = enemy_sprite.rect.left
            self.health_bar.width = enemy_sprite.health
        
        def blitme(self):
            pygame.draw.rect(self.screen, self.red, self.bg_bar)
            pygame.draw.rect(self.screen, self.green, self.health_bar)     
            
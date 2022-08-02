import pygame
import os

class Pikachu(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.screen_rect = self.screen.get_rect()

        self.image_names = ['pika-one.png', 'pika-two.png', 'pika-three.png', 'pika-four.png', 'pika-five.png', 'pika-six.png']
        self.right_images = [pygame.image.load(f"images/{name}") for name in self.image_names]
        self.left_images = [pygame.transform.flip(pygame.image.load(f"images/{name}"), True, False) for name in self.image_names]
        
        self.jumping_img_names = ['pika_jump_1.png', 'pika_jump_2.png', 'pika_jump_3.png', 'pika_jump_4.png', 'pika_jump_5.png']
        self.r_jump_imgs = [pygame.image.load(f"images/{name}") for name in self.jumping_img_names]
        self.l_jump_imgs = [pygame.transform.flip(pygame.image.load(f"images/{name}"), True, False) for name in self.jumping_img_names]

        self.index = 0
        self.images = self.right_images
        self.image = self.images[self.index]
        # image rect
        self.rect = self.image.get_rect()
        self.rect.bottom = 540
        self.rect.left = 0
        # real rect object - represents everything but pikachu's tail
        self.real_rect = pygame.Rect(0,0,60,55)
        self.real_rect.bottom = self.rect.bottom
        self.real_rect.left = self.rect.left+37
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.ground_level = self.settings.ground_level

        self.shock_attack = False

        self.moving_left = False
        self.moving_right = False
        self.jump_pic_index = 0
        self.facing = 'R' # either 'R' or 'L'

        self.ground_rect = pygame.Rect(0,0,800,20)
        self.ground_rect.bottom = self.screen_rect.bottom

        self.hit_rect = ''

        self.jumping = False
        # create jump_list variable using the jump_list from settings.py
        self.jump_list = self.settings.pika_jump_list
        self.jump_index = 0
        # grounded variable - if pikachu is on top of a platform, then it's True
        self.grounded = True

        # holds the rect of platform pikachu is on top of
        self.ground_plat_rect = ''
        # if hit_right = True, moving_right cannot be True, same for hit_left
        self.hit_right = False
        self.hit_left = False
        # boolean for tbolt shot attack
        self.tbolt_attack = False
        # boolean for if pikachu is falling (not jumping, but still falling)
        self.falling = False

        # boolean for if pikachu's been bitten in past 2 seconds - if he's next to blastoise when blastoise bites,
        # he loses health, and was_bitten is set to True, pikachu only takes damage if was_bitten is False - it gets
        # set to false again inside the self.allow_enemy_bite event that allows blastoise to bite again
        self.was_bitten = False

    def update(self, game):
        if self.shock_attack == False and self.settings.electricity<150:
            self.settings.electricity += 0.05
        if self.jumping:
            self.real_rect.y += self.jump_list[self.jump_index]
            self.rect.y += self.jump_list[self.jump_index]
            # keep from going over the number of indices in jump_list
            if self.jump_index < 84:
                self.jump_index += 1
            # if we reach index 84 - reset to 0, pikachu's not jumping
            else:
                self.jump_index = 0
                self.jump_pic_index = 0
                self.jumping = False
        platform_hits = self.real_rect.collidelist(game.platform_rect_list)            
        if platform_hits != -1:
            the_rect = game.platform_rect_list[platform_hits]
            if self.real_rect.bottom <= the_rect.top+20:
                # pikachu has hit a platform, and he's on top, it's not possible
                # for his rect.bottom to be greater than
                self.rect.bottom = the_rect.top-1
                self.real_rect.bottom = the_rect.top-1
                # pikachu is grounded because he's on top of a platform
                self.grounded = True
                self.jumping = False
                self.jump_index = 0
                self.ground_plat_rect = game.platform_rect_list[platform_hits]
            if self.real_rect.bottom > the_rect.top+20:
                self.hit_rect = game.platform_rect_list[platform_hits]
                # if pikachu hits the left of platform and not on top
                if self.real_rect.right >= the_rect.left and self.real_rect.left < the_rect.left:
                    self.rect.right = the_rect.left - 2
                    if self.facing == 'R':
                        self.real_rect.right = the_rect.left - 2
                    else:
                        self.real_rect.right = the_rect.left - 39
                    self.moving_right = False
                    self.hit_right = True
                # if pikachu hits the right of platform and not on top
                elif self.real_rect.left <= the_rect.right and self.real_rect.right > the_rect.right:
                    self.rect.left = the_rect.right + 2
                    if self.facing == 'L':
                        self.real_rect.left = the_rect.right + 2
                    else:
                        self.real_rect.left = the_rect.right + 39
                    self.moving_left = False
                    self.hit_left = True
                    
        # if not hitting a platform and NOT grounded, and NOT jumping, then let pikachu
        # fall by 15 r 20 a frame
        elif platform_hits == -1 and self.jumping == False and self.grounded == False:
            self.rect.bottom += self.settings.gravity_pull
            self.real_rect.bottom += self.settings.gravity_pull
        # if hit_rect != '', that means pikachu has hit a platform
        if self.hit_rect != '':
            # if pikachu hit right side of platform
            if self.rect.left<self.hit_rect.right and self.rect.right > self.hit_rect.right:
                self.moving_left = False
                self.hit_right = True
                self.rect.left = self.hit_rect.right+5
                # pikachu's probably facing L, but..
                if self.facing == 'L':
                   self.real_rect.left = self.hit_rect.right+5
                # if pikachu's facing R, gotta take tail length into account (37)
                else:
                    self.real_rect.left = self.hit_rect.right + 42
               
                self.hit_rect = ''
            # if hit left side of platform
            elif self.rect.right>self.hit_rect.left and self.rect.left < self.hit_rect.left:
                self.moving_right = False
                self.hit_left = True
                self.rect.right = self.hit_rect.left-5
                if self.facing == 'R':
                    self.real_rect.right = self.hit_rect.left-5
                else:
                    self.real_rect.right = self.hit_rect.left-42
            # if hasn't hit left/right side, and still has hit, and pika-rect.top under the platform
            # bottom - it means pikachu is under platform
            elif self.rect.bottom < self.hit_rect.top or self.rect.top > self.hit_rect.bottom:
                self.hit_rect = ''
                self.hit_left = False
                self.hit_right = False

        # if ground_plat_rect != '', that means pikachu is on top of a platform
        if self.ground_plat_rect != '':
            # if pikachu goes over left/right edge of platform - he's no longer grounded, and also
            # ground_plat_rect is reset to ''
            # MIGHT BE ABLE TO KEEP THIS AND JUST ALTER IS LIKE ADD/SUBTRACT THE TAIL LENGTH, but for now,
            # well go with the real_rect idea
            if self.real_rect.right<self.ground_plat_rect.left or self.real_rect.left>self.ground_plat_rect.right:
                self.grounded = False
                self.ground_plat_rect = ''
            # this is the original if statement below -->
            # if self.rect.right < self.ground_plat_rect.left or self.rect.left > self.ground_plat_rect.right:
            #     self.grounded = False
            #     self.ground_plat_rect = ''

        # also, if ground_plat_rect = '', that means pikachu isn't grounded
        if self.ground_plat_rect == '':
            self.grounded = False

        # basic left/right movement, - scroll_speed if not moving
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.rect.x += self.settings.pikachu_speed
            self.real_rect.x += self.settings.pikachu_speed
        elif self.moving_left:
            self.rect.x -= (self.settings.pikachu_speed+self.settings.scroll_speed)
            self.real_rect.x -= (self.settings.pikachu_speed+self.settings.scroll_speed)
        elif not self.moving_right and not self.moving_left:
            self.rect.x -= self.settings.scroll_speed
            self.real_rect.x -= self.settings.scroll_speed

        # throwing a statement underneath this that will decrement the electric_bar while you hold w and increase it while you don't
        if self.shock_attack and self.settings.electricity>0:
            self.settings.electricity -= 1
        if self.settings.electricity < 0:
            self.settings.electricity = 0
        # pikachu can't shock if he doesn't have electricity (blue bar)
        if self.settings.electricity == 0:
            self.shock_attack = False
        self._change_imgs()
        self._check_pika_death()
        
        # put a statement that will update real_rect based on pikachu's rect position:
        if self.facing == 'R':
            self.real_rect.right = self.rect.right
        elif self.facing == 'L':
            self.real_rect.left = self.rect.left
        self.real_rect.bottom = self.rect.bottom

    def _change_imgs(self):
        # ------------------------------------------------------------------------------
        # ALL OF THIS STUFF IS IN THE FUNCTION RIGHT ABOVE (MOSTLY)
        # NEED TO CONSOLIDATE THIS WITH ABOVE FUNCTION AS WELL AS LOOK AT WHAT'S IN MAIN,
        # SUCH AS THE CHANGE_PIKA_IMGS FUNCTION
        # ------------------------------------------------------------------------------
        if self.jumping:
            if self.jump_index <= 17:
                self.jump_pic_index = 0
            elif self.jump_index <= 38:
                self.jump_pic_index = 1
            elif self.jump_index < 47:
                self.jump_pic_index = 2
            elif self.jump_index < 64:
                self.jump_pic_index = 3
            elif self.jump_index < 85:
                self.jump_pic_index = 4
            # if pikachu's jumping and facing right - use r_jump_imgs
            if self.facing == 'R':
                self.images = self.r_jump_imgs
            # if pikachu's jumping and facing left - use l_jump_imgs
            elif self.facing == 'L':
                self.images = self.l_jump_imgs
            self.image = self.images[self.jump_pic_index]
        elif self.jumping == False  and self.grounded == True:
            if self.facing == 'R':
                self.images = self.right_images
            elif self.facing == 'L':
                self.images = self.left_images
            # self.image = self.images[self.index]
        
        # if self.jumping == False:
            if self.moving_left == False and self.moving_right == False:
                self.index = 3
            self.image = self.images[self.index]

        # if not jumping, and not grounded:
        elif self.jumping == False and self.grounded == False:
            if self.facing == 'R':
                self.images = self.r_jump_imgs
            elif self.facing == 'L':
                self.images = self.l_jump_imgs
            self.image = self.images[-1]
        

    def _check_pika_death(self):
        # if pikachu runs into enemy/vice versa - pikachu loses health
        enemy_hits = pygame.sprite.spritecollide(self, self.game.enemy_group, False)
        if enemy_hits:
            # SET ENEMY_HITS[0].doing_bump to True if enemy isn't .attacking already
            if (not enemy_hits[0].attacking) and (not enemy_hits[0].has_bitten):
                # if pikachu's hit on the right side:
                if self.rect.left<=enemy_hits[0].rect.right and self.rect.right>enemy_hits[0].rect.right:
                    # then set enemy to be facing right
                    enemy_hits[0].facing='right'
                elif self.rect.right>=enemy_hits[0].rect.left and self.rect.left<enemy_hits[0].rect.left:
                    enemy_hits[0].facing='left'
                # now we set doing_bump to True - so the enemy can being the belly bump
                enemy_hits[0].biting = True
            # the section below is the part I was working on to make pikachu NOT go right through enemies - it's a work
            # in progress and not going to come back to it until I've improved actual enemy attack
            # ---------------------------------------------------------------------------------------------------------
            # if pikachu is below the enemy/on same level (basically just not falling onto blastoise's head - have to
            # allow the 15 for falling into)
            if self.rect.bottom>enemy_hits[0].rect.top+15:
                if self.rect.right>=enemy_hits[0].rect.left and self.rect.left<enemy_hits[0].rect.left:
                    self.rect.right = enemy_hits[0].rect.left-5
                elif self.rect.left<=enemy_hits[0].rect.right and self.rect.right>enemy_hits[0].rect.right:
                    self.rect.left = enemy_hits[0].rect.right+5
            # if pikachu IS falling on top of blastoise:
            elif self.rect.bottom<=enemy_hits[0].rect.top+15:
                self.rect.bottom = enemy_hits[0].rect.top-5
                # set jumping to False, grounded to True, reset jump_index because landing on top of an enemy is the
                # same as landing on a platform and walking on it (at least for the moment)
                self.grounded = True
                self.jumping = False
                self.jump_index = 0
                # set ground_plat_rect to be the enemy's rect:
                self.ground_plat_rect = enemy_hits[0].rect
                # set pikachu's ground image list as the images
                if self.facing == 'R':
                    self.images = self.right_images
                elif self.facing == 'L':
                    self.images = self.left_images
            # ---------------------------------------------------------------------------------------------------------
            self.settings.pika_health -= 1
        # if the screen scroll catches up to pikachu and he goes off left side of screen - he dies, but there is some
        # margin for error - he can fall 250 px behind left side of screen
        if self.rect.right <= self.screen_rect.left-250:
            self.settings.pikachu_lives -= 1
            self.game.game_active = False
        # if pikachu falls below bottom of screen - quickly loses health i.e. he dies
        if self.rect.top > self.screen_rect.height:
            self.settings.pika_health -= 10

    def blitme(self):
        self.screen.blit(self.image, self.rect)

# class for pikachu's lives in top left of screen (pikachu heads)
class PikaLives:
    def __init__(self, game):
        self.game = game
        self.settings = self.game.settings
        self.screen = self.game.screen
        self.screen_rect = self.screen.get_rect()

        self.image = pygame.image.load(os.path.join('images', 'death', 'pika_head.png'))
        self.rect = self.image.get_rect()

    def prep_heads(self):
        for lives_left in range(self.settings.pikachu_lives):
            self.rect.x = 10 + lives_left * 50
            self.rect.y = 10
            self.screen.blit(self.image, (self.rect.x, self.rect.y))
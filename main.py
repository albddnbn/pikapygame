import pygame
import sys
import os
import random
from settings import Settings
from pikachu import Pikachu, PikaLives
from background import Background, Ground
from platform import Platform
from shock_attack import ShockAttack
from enemy import Enemy
from status_bar import StatusBar, ScreenMsg, Button
from power_ups import PowerUp
from tbolt_shot import TboltShot

# main game class - contains game loop and other important functions
class PikaMassacre:
    def __init__(self):
        # most important variables:
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption("Pikachu!")
        # boolean to hold whether game is active or not - if not then play button comes up along with some other stuff
        # depending on which game loop the program is in
        self.game_active = False

        # set pygame clock
        self.clock = pygame.time.Clock()

        # **CREATE INSTANCES**:
        # create play button instance
        self.play_button = Button(self, "Start!")
        # background and ground(2)
        self.background = Background(self)
        self.ground_1 = Ground(self, 0)
        self.ground_2 = Ground(self, 801)
        # create pikachu
        self.pikachu = Pikachu(self)
        # create status_bars - health and electricity
        self.health_bar = StatusBar(self, self.settings.health_bar_rect, self.settings.green)
        self.electric_bar = StatusBar(self, self.settings.electric_bar_rect, self.settings.blue)
        # create pika_lives instance - pikachu heads symbolizing lives left (top left of screen)
        self.player_lives = PikaLives(self)

        # **SPRITE GROUPS**:
        # ground sprites
        self.ground_group = pygame.sprite.Group()
        self.ground_group.add(self.ground_1)
        self.ground_group.add(self.ground_2)
        # sprite group for pikachu's shock attacks
        self.shock_group = pygame.sprite.Group()
        # group to hold platforms, this group is used to scroll the platforms, the platform_rect_list is used for
        # collision detection (platform_rect_list is rect for groups of platform tiles)
        self.platform_group = pygame.sprite.Group()
        self.whole_rect = ''
        # list to keep platform rects (tiles joined together to form platforms)
        self.platform_rect_list = []
        # sprite group to hold hydropump sprites
        self.hydro_group = pygame.sprite.Group()
        # sprite group for enemy sprites
        self.enemy_group = pygame.sprite.Group()
        # create group for shock powerup sprites
        self.shock_powerup_group = pygame.sprite.Group()
        # create health_potion group for potions
        self.potion_group = pygame.sprite.Group()

        # **PIKACHU DYING/END GAME/WIN GAME VARIABLES**:
        self.end_game_its_over = False
        # message to blit to screen if user beats level
        self.you_won_msg = ScreenMsg(self, 'images/you_won.png')
        # create instance of ScreenMsg and blit to end of level - if pikachu hits it he wins the level
        self.end_level_one = ScreenMsg(self, 'images/pokeball_finish.png')
        self.end_level_one.rect.bottom = 540
        # as of aug 3 - end of level is 11370 (a ground platform, which means the top/y coord = 540)
        self.end_level_one.rect.right = 11300
        # boolean to signify the end of a level - when pikachu hits the pokeball at the end - it will switch to True
        self.beat_level = False

        # **PYGAME USEREVENTS**:
        # event to change pikachu images (moving) - every 1/4 second
        self.change_pika_image_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.change_pika_image_event, 150)
        # change enemy images event (when moving/not attacking)
        self.enemy_img_event = pygame.USEREVENT + 2
        pygame.time.set_timer(self.enemy_img_event, 200)
        # end game and life lost event - when pikachu dies and has lives left
        self.you_died_replay_event = pygame.USEREVENT + 3
        # now, we have to create an event for enemy_attack
        self.enemy_attack_event = pygame.USEREVENT + 4
        # define another event that I will use to stop attacking, I'll set a timer
        # when the enemy_attack_event is triggered which will stop attack in 3 seconds
        # or something
        self.enemy_stop_attack = pygame.USEREVENT + 5

        self.exit_after_win = pygame.USEREVENT + 6

        # VARIABLES FOR COUNTDOWN AT START OF GAME/END OF LIFE:
        # event for beginning countdown
        self.countdown_num_event = pygame.USEREVENT + 7
        # countdown index variable
        self.countdown_index = -1
        self.countdown_list = self.settings.countdown_list
        self.countdown_string = ''
        # set countdown font size/font type
        self.countdown_font = pygame.font.SysFont("comicsans", 120, True)

        # event to change tbolt imgs
        self.tbolt_img_change_event = pygame.USEREVENT + 8
        # event to change tbolt_move to True
        self.tbolt_move_event = pygame.USEREVENT + 9

        # event to change the shock attack img (not the tbolt shot attack)
        self.shock_img_event = pygame.USEREVENT + 10

        # set event which will set blastoise's (enemys) has_bitten variable back to False to allow him to bite again,
        # don't want him biting over and over again without any pause
        self.allow_enemy_bite = pygame.USEREVENT + 11

        # hydropump wait event - blastoise can't do hydro pump after hydro pump:
        self.hydropump_wait_event = pygame.USEREVENT + 12

        # **PLAYER SETTINGS VARIABLES:**
        # set player's score to 0 at start of game
        self.player_score = 0
        # if self.tbolt != '', then a tbolt instance has been created, pikachu has fired a tbolt
        self.tbolt = ''
        # boolean for tbolt shot to move - it stays still for very short period of time then moves
        self.tbolt_move = False
        # going to create this variable so that when user presses 'w' - it changes to 1, and if it's one - no more shock 
        # instances will be created
        self.shock_created = False
        # dictionary to keep enemies in - *this might not be necessary, but it does make it so all the enemies aren't
        # named 'self.enemy' in the loop that generates all of them
        self.enemy_dict = {}

    def _game_loop_one(self):
        while self.loop == 1:
            self.clock.tick(self.settings.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()               
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # when mouse is clicked - check position - if they clicked play button, change game to active
                    mouse_pos = pygame.mouse.get_pos()
                    self._check_play_button(mouse_pos)
                elif event.type == self.countdown_num_event:
                    # play button is drawn when game isn't active, when game is active - countdown begins, either way,
                    # countdown_num_event is triggered every second
                    if self.game_active:
                        self.countdown_index += 1
                        self.countdown_string = self.countdown_list[self.countdown_index]
                        if self.countdown_index == 4:
                            pygame.time.set_timer(self.countdown_num_event, 0)
                            self.loop = 2
            self._draw_screen()

    # this is GAME LOOP - includes code for loop 2, and calls to all other loops
    def run_game(self):
        # generate platforms, enemies, potions
        self._gen_plat_list()
        self._generate_enemies()
        self._gen_potions()
        self._gen_shock_powerups()
        # set event timer for countdown
        self.loop = 1
        while True:
            # reset countdown_index to -1
            self.countdown_index = -1
            # set timer for countdown num event (every second)
            pygame.time.set_timer(self.countdown_num_event, 1000)
            if self.loop == 1:
                self._game_loop_one()
            if self.loop == 2:
                # *UNNECESSARY:
                # self.game_active = True

                # *UNNECESSARY:
                # random_num = random.randrange(1000,4000,500)
                # trigger enemy_attack_event after random time:
                pygame.time.set_timer(self.enemy_attack_event, random.randrange(1000,4000,500), True)
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            sys.exit()
                        elif event.type == pygame.KEYUP:
                            self._check_keyup_events(event)
                        elif event.type == pygame.KEYDOWN:
                            self._check_keydown_events(event)
                        # ***WTF IS THIS DOING HERE??***
                        # elif event.type == pygame.MOUSEBUTTONDOWN:
                        #     mouse_pos = pygame.mouse.get_pos()
                        #     self._check_play_button(mouse_pos)

                        elif event.type == self.change_pika_image_event:
                            # increments pikachu's index variable - changes image for normal movement (not jumping, etc)
                            if self.pikachu.moving_left == True or self.pikachu.moving_right == True:
                                if self.pikachu.index >= len(self.pikachu.right_images)-1:
                                    self.pikachu.index = 0
                                else:
                                    self.pikachu.index += 1

                        elif event.type == self.enemy_img_event:
                            # self._change_enemy_imgs()
                            for enemy in self.enemy_group:
                                self._change_enemy_imgs(enemy)

                                # ** PROBABLY UNNECESSARY:***
                                # if enemy.attacking:
                                #     self._change_enemy_attack_imgs(enemy)
                                # quoting this doing_bump stuff out for now, putting in bite instead
                                # elif enemy.doing_bump:
                                #     self._change_enemy_bump_imgs(enemy)
                                # elif not enemy.attacking:
                                #     enemy.hydropump.index = 0

                        # enemy starts hydropump attack
                        elif event.type == self.enemy_attack_event:
                            for enemy in self.enemy_group:
                                # if enemy is on screen and not currently attacking:
                                if enemy.on and (not enemy.attacking) and (not enemy.attack_wait):
                                    enemy.attacking = True
                            pygame.time.set_timer(self.enemy_stop_attack, 2500, True)

                        # triggered to happen 2.5s after any enemy starts an attack
                        elif event.type == self.enemy_stop_attack:
                            for enemy in self.enemy_group:
                                if enemy.attacking:
                                    enemy.attacking = False
                                    # make sure hydropump index is set back to 0 since blastoise is done attacking
                                    enemy.hydropump.index = 0
                                    enemy.attack_wait = True
                            # make enemy wait to use hydropump again
                            pygame.time.set_timer(self.hydropump_wait_event, random.randrange(2000,4000,500), True)

                        elif event.type == self.hydropump_wait_event:
                            # schedule another enemy attack to occur in 1.5-3 seconds (500ms intervals):
                            for enemy in self.enemy_group:
                                if enemy.attack_wait:
                                    enemy.attack_wait = False
                            pygame.time.set_timer(self.enemy_attack_event, random.randrange(1500,3000,500), True)
                        
                        # event to allow blastoise to bite again:
                        elif event.type == self.allow_enemy_bite:
                            for enemy in self.enemy_group:
                                if enemy.has_bitten:
                                    enemy.has_bitten = False
                                    self.pikachu.was_bitten = False

                        elif event.type == self.tbolt_img_change_event:
                            self._change_tbolt_img()
                        # event that starts tbolt shot moving
                        elif event.type == self.tbolt_move_event:
                            self.tbolt_move = True
                        elif event.type == self.shock_img_event:
                            for shock in self.shock_group:
                                if shock.index >= len(shock.l_imgs)-1:
                                    shock.index = 0
                                else:
                                    shock.index += 1
                    # check tbolt shot hits
                    self._check_tbolt_hits()
                    # check if pikachu has hit any potions
                    self._check_potions()
                    # check if pikachu has hit any shock powerups
                    self._check_shock_powerup_hits()
                    # key presses as opposed to key up/down
                    self._key_press_function()
                    # check if pikachu's shock has hit enemies, or if enemys' hydropump
                    # has hit pikachu, or if enemy themselves has hit pikachu
                    self._check_enemy_attack_collisions()
                    # check if pikachu has hit the end-level pokeball thing
                    self._check_beat_level()

                    self._update_screen()
                    self._draw_screen()
                    # if game isn't active, break - when pikachu dies game isn't active, breaks
                    # into game over or lost life routine
                    if not self.game_active:
                        break
                # check if pikachu has lost health/life
                self._pika_life_lost()
            if self.loop == 3:
                self._game_loop_three()
            if self.end_game_its_over:
                self._game_over_loop()
                # sys.exit()
            if self.loop == 'beat level':
                self._you_won_loop()

    def _game_loop_three(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == self.you_died_replay_event:
                    self.loop = 1
                    # restart level:
                    self.platform_rect_list = []
                    self.platform_group.empty()
                    self.shock_group.empty()
                    self.enemy_group.empty()
                    self.hydro_group.empty()
                    self.potion_group.empty()
                    self._gen_plat_list()
                    self._generate_enemies()
                    self._gen_potions()
                    self.player_score = 0
                    break
            if self.loop == 1:
                break
            # update health/eletricity bars so that they refill when restarting level after dying:
            self.health_bar.update(self.settings.pika_health)
            self.electric_bar.update(self.settings.electricity)
            self._draw_screen()

    def _game_over_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == self.you_died_replay_event:
                    sys.exit()
            self._draw_screen()

    def _you_won_loop(self):
        # this event will exit the game after the 'you won!' message has been showing
        # on screen for ~5 seconds
        pygame.time.set_timer(self.exit_after_win, 5000, True)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == self.exit_after_win:
                    sys.exit()
            # you_won_msg.blitme()
            self._draw_screen()

    def _key_press_function(self):
        keyboard_state = pygame.key.get_pressed()
        if keyboard_state[pygame.K_LEFT]:
            self.pikachu.facing = 'L'
            if not self.pikachu.hit_left:
                self.pikachu.moving_left = True
                self.pikachu.hit_right = False
        if keyboard_state[pygame.K_RIGHT]:
            self.pikachu.facing = 'R'
            if not self.pikachu.hit_right:
                self.pikachu.moving_right = True
                self.pikachu.hit_left = False

    def _check_keydown_events(self, event):
        if event.key == pygame.K_SPACE:
            if self.pikachu.jumping == False and self.pikachu.grounded == True:
                self.pikachu.jumping = True
                self.pikachu.grounded = False
        elif event.key == pygame.K_e:
            if self.settings.electricity >= 30 and self.pikachu.tbolt_attack == False and self.tbolt == '':
                self.settings.electricity -= 30
                # tbolt shot will wait 1/2 second before starting to move horizontally across screen
                pygame.time.set_timer(self.tbolt_move_event, 250, True)
                self.pikachu.tbolt_attack = True
                self.tbolt = TboltShot(self, self.pikachu.rect.x)
                # self.tbolt_group.add(self.tbolt)
                # set timer for tbolt shot images to change - every 150 milliseconds
                pygame.time.set_timer(self.tbolt_img_change_event, 150)

        elif event.key == pygame.K_w:
            # only let pikachu shock if he's not jumping and has electricity in his attack bar
            # got rid of thing this makes it so pikachu can't shock if jumping...for now
            if self.settings.electricity > 0:
                self.pikachu.shock_attack = True
                if not self.shock_created:
                    self.shock = ShockAttack(self)
                    self.shock_group.add(self.shock)
                    pygame.time.set_timer(self.shock_img_event,75)
                    self.shock_created = False

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.pikachu.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.pikachu.moving_left = False
        elif event.key == pygame.K_w:
            self.pikachu.shock_attack = False
            self.shock.kill()
            self.shock_group.empty()
            pygame.time.set_timer(self.shock_img_event,0)
        elif event.key == pygame.K_e:
            self.pikachu.tbolt_attack = False

    # check if tbolt has hit any enemies, any platforms, or gone off screen
    def _check_tbolt_hits(self):
        # if a tbolt exists - check if it hit any enemies:
        if self.tbolt != '':
            # for tbolt in self.tbolt_group:
            tbolt_hits = pygame.sprite.spritecollide(self.tbolt, self.enemy_group, False)
            if tbolt_hits:
                tbolt_hits[0].health -= 20
                if tbolt_hits[0].health <= 0:
                    self.player_score += 10
                    tbolt_hits[0]._im_dead()
                    tbolt_hits[0].hydropump.kill()
                    tbolt_hits[0].health_meter.kill()
                    tbolt_hits[0].kill()
                self.tbolt_move = False
                self.pikachu.tbolt_attack = False
                self.tbolt.kill()
                self.tbolt = ''

        # if a tbolt exists - check if it hit any platforms
        if self.tbolt != '':
            # check if tbolt has hit platforms
            tbolt_platf_hits = self.tbolt.rect.collidelist(self.platform_rect_list)
            if tbolt_platf_hits != -1:
                self.tbolt_move = False
                self.pikachu.tbolt_attack = False
                self.tbolt.kill()
                self.tbolt = ''

        # if tbolt exists - check if it's gone off screen
        if self.tbolt != '':
            # if tbolt goes off right/left side of screen:
            if self.tbolt.rect.right <= 0:
                self.tbolt_move = False
                self.pikachu.tbolt_attack = False
                self.tbolt.kill()
                self.tbolt = ''
            elif self.tbolt.rect.left >= 800:
                self.tbolt_move = False
                self.pikachu.tbolt_attack = False
                self.tbolt.kill()
                self.tbolt = ''

    def _change_tbolt_img(self):
        # only one tbolt sprite can exist at any given time - if it does - cycle through indices
        if self.tbolt != '':
            # for tbolt in self.tbolt_group:
                if self.tbolt.index >= len(self.tbolt.l_imgs)-1:
                    self.tbolt.index = 0
                else:
                    self.tbolt.index += 1

    # create game score object
    def _prep_score(self, score):
        font = pygame.font.SysFont("comicsans", 60, True)
        text = font.render(str(score), 1, self.settings.red)
        self.screen.blit(text, (700,10))

    # check if pikachu has hit the end-of-level pokeball
    def _check_beat_level(self):
        level_won = self.pikachu.rect.colliderect(self.end_level_one.rect)
        if level_won:
            self.game_active = False
            self.loop = 'beat level'

    def _gen_plat_list(self):
        for x in range(len(self.settings.ground_plot_list)):
            self._gen_platforms(x, 'ground', 600)
        for x in range(len(self.settings.plat1_num_list)):
            self._gen_platforms(x, '1', 540)
        for x in range(len(self.settings.plat1_5_num_list)):
            self._gen_platforms(x, '1.5', 510)
        for x in range(len(self.settings.plat2_num_list)):
            self._gen_platforms(x, '2', 480)
        for x in range(len(self.settings.plat2_5_num_list)):
            self._gen_platforms(x, '2.5', 450)
        for x in range(len(self.settings.plat3_num_list)):
            self._gen_platforms(x, '3', 420)

    # this function generates the platforms
    def _gen_platforms(self, index, level, bottom_rect):
        if level == 'ground':
            plot_list = self.settings.ground_plot_list
            num_list = self.settings.ground_num_list
        elif level == '1':
            plot_list = self.settings.plat1_plot_list
            num_list = self.settings.plat1_num_list
        elif level == '1.5':
            plot_list = self.settings.plat1_5_plot_list
            num_list = self.settings.plat1_5_num_list
        elif level == '2':
            plot_list = self.settings.plat2_plot_list
            num_list = self.settings.plat2_num_list
        elif level == '2.5':
            plot_list = self.settings.plat2_5_plot_list
            num_list = self.settings.plat2_5_num_list
        elif level == '3':
            plot_list = self.settings.plat3_plot_list
            num_list = self.settings.plat3_num_list
        self.num_plats = num_list[index]
        for x in range(self.num_plats):
            if level == 'ground':
                platform = Platform(os.path.join('platforms', 'more_real_grass.png'), x+1, self)
            else:
                platform = Platform(os.path.join('platforms', 'cartoon_grass_strip.png'), x+1, self)
            platform.rect.bottom = bottom_rect
            platform.rect.left = plot_list[index]+(x*platform.rect.width)
            self.platform_group.add(platform)
        self.whole_rect = pygame.Rect(((plot_list[index]), bottom_rect-52), (120*self.num_plats, 52))
        self.platform_rect_list.append(self.whole_rect)

    def _generate_enemies(self):
        for x in range(len(self.settings.enemy_distance_list)):
            self._generate_enemy(str(x), self.settings.enemy_distance_list[x], 
                                 self.settings.enemy_ground_lvl_list[x], 
                                 self.settings.enemy_rect_list[x])
        # moved the set_timer for the enemy_attack event to right before the actual game loop begins,
        # when it's done here it starts when enemies are generated, which is before the countdown even starts...

    def _generate_enemy(self, enemy_name, range, bottom_rect, right_rect):
        self.enemy_dict[enemy_name] = Enemy(self, range)
        self.enemy_dict[enemy_name].rect.bottom = bottom_rect
        self.enemy_dict[enemy_name].rect.right = right_rect
        self.enemy_group.add(self.enemy_dict[enemy_name])
        self.hydro_group.add(self.enemy_dict[enemy_name].hydropump)

    # generate health potions
    def _gen_potions(self):
        for x in range(len(self.settings.potion_plot_list)):
            potion = PowerUp(self,'images/health_powerups/potion.png')
            potion.rect.bottom = self.settings.potion_height_list[x]
            potion.rect.right = self.settings.potion_plot_list[x]
            self.potion_group.add(potion)

    # function to generate electricity powerups
    def _gen_shock_powerups(self):
        for x in range(len(self.settings.shock_powerup_plot_list)):
            shock_up = PowerUp(self, 'images/health_powerups/blue_bolt.png')
            shock_up.rect.bottom = self.settings.shock_powerup_height_list[x]
            shock_up.rect.right = self.settings.shock_powerup_plot_list[x]
            self.shock_powerup_group.add(shock_up)

    # took out DEF CHANGE_ENEMY_ATTACK_IMGS - all the functionality is covered in change_enemy_imgs()

    def _change_enemy_imgs(self, enemy):
        # for enemy in self.enemy_group:
        # 'on' means on screen
        if enemy.on:
            # if not attacking or biting, then use normal images
            if (not enemy.attacking) and (not enemy.biting):
                enemy.hydropump.index = 0
                if enemy.index >= len(enemy.l_imgs)-1:
                    enemy.index = 0
                else:
                    enemy.index += 1
            # if attacking (hydropump), not biting just put there for safety, but shouldn't be necessary
            if enemy.attacking and (not enemy.biting):
                if enemy.attack_index >= len(enemy.l_attack_imgs)-1:
                    enemy.attack_index = 0
                else:
                    enemy.attack_index += 1
                if enemy.hydropump.index >= len(enemy.hydropump.l_imgs)-1:
                    enemy.hydropump.index = 1
                else:
                    enemy.hydropump.index += 1
            # if biting (close combat), not attacking just put there for safety purposes
            elif enemy.biting and (not enemy.attacking):
                if enemy.bite_index >= len(enemy.l_bite_imgs)-1:
                    enemy.bite_index = 0
                    enemy.biting = False
                    # set enemy.HAS_BITTEN to True, then set timer for event to set it back to false - blastoise
                    # can only bite if has_bitten is false - so that he doesn't just keep biting pikachu
                    enemy.has_bitten = True
                    pygame.time.set_timer(self.allow_enemy_bite, 2000, True)
                else:
                    enemy.bite_index += 1
                # if enemy's index is greater than 1 that means it's the 2 pics with blastoise's mouth open, so
                # that's when pikachu will take damage
                # if blastoise is biting AND currently colliding with pikachu:
                if enemy.bite_index > 1 and pygame.sprite.collide_rect(self.pikachu, enemy):
                    self.settings.pika_health -= 40
                    self.pikachu.was_bitten = True

    # function to remove whole_rects from platform_rect_list once they pass left side of screen:
    def update_whole_rect_list(self):
        for platf_rect in self.platform_rect_list:
            if platf_rect.right <= 0:
                self.platform_rect_list.remove(platf_rect)

    # check if pikachu hit any health potions
    def _check_potions(self):
        for potion in self.potion_group:
            hits = potion.rect.colliderect(self.pikachu.rect)
            # if pikachu comes in contact with health potion, boost health by 30
            if hits:
                if self.settings.pika_health > 120:
                    self.settings.pika_health = 150
                else:
                    self.settings.pika_health += 30
                potion.kill()

    # check if pikachu hit the shock powerup
    def _check_shock_powerup_hits(self):
        for shock in self.shock_powerup_group:
            hits = shock.rect.colliderect(self.pikachu.rect)
            # if pikachu comes in contact with shock powerup, boost pikachu's electricity by 50
            if hits:
                if self.settings.electricity >= 100:
                    self.settings.electricity = 150
                else:
                    self.settings.electricity += 50
                shock.kill()

    def _check_enemy_attack_collisions(self):
        # decrement enemy health if enemy hit by pika's shock
        for shock in self.shock_group:
            shock_hits = pygame.sprite.spritecollide(shock, self.enemy_group, False)
            if shock_hits and self.pikachu.shock_attack:
                # shock_hits[0] = the enemy that pikachu's shock has come into contact with
                shock_hits[0].health -= self.settings.shock_attack_power
                # kill enemy if enemy's health gets to 0 or below
                if shock_hits[0].health <= 0:
                    self.player_score += 10
                    shock_hits[0]._im_dead()

        # test if pikachu rect hits any of the hydro's hitbox_rects:
        for hydro in self.hydro_group:
            hydro_hits = hydro.rect.colliderect(self.pikachu.real_rect)
            if hydro_hits and hydro.enemy_sprite.attacking == True:
                self.settings.pika_health -= 1


    def _update_screen(self):
        # if pikachu's health drops to 0 or below - subtract a life, and set game_active to False, which will trigger
        # the next loop, which will either be game over loop, or you died/replay loop (I think they're both loop 3)
        if self.settings.pika_health <= 0:
            self.settings.pikachu_lives -= 1
            self.game_active = False
        # update position of background, platforms, and pikachu
        self.background.update()
        self.platform_group.update()
        self.pikachu.update(self)
        # if tbolt attack is happening (not ''), then update it
        if self.tbolt != '':
            self.tbolt.update()
        # update pikachu's health bar/electricity bar
        self.health_bar.update(self.settings.pika_health)
        self.electric_bar.update(self.settings.electricity)
        if self.pikachu.shock_attack:
            self.shock_group.update()
        self.enemy_group.update(self.pikachu)
        # update potion and shock powerup groups
        for potion in self.potion_group:
            potion.update(self.settings.pika_health)
        for shock in self.shock_powerup_group:
            shock.update(self.settings.electricity)
        # scroll pokeball backwards with level - if pikachu hits it, level 1 is beaten
        self.end_level_one.rect.x -= self.settings.scroll_speed
        self.update_whole_rect()

    # draw countdown to screen - 3,2,1, GO
    def _draw_countdown(self, count):
        text = self.countdown_font.render(count, 1, self.settings.red)
        self.screen.blit(text, (400,300))

    def _draw_screen(self):
        self.background.render()
        self.platform_group.draw(self.screen)
        self.pikachu.blitme()
        if self.pikachu.shock_attack:
            self.shock_group.draw(self.screen)
        # if self.tbolt_group:
        #     self.tbolt_group.draw(self.screen)
        if self.tbolt != '':
            self.tbolt.blitme()
        # wait for user to press play button
        if self.loop == 1 and self.game_active == False:
            self.play_button.draw_button()
        if self.loop == 1 and self.game_active == True:
            self._draw_countdown(self.countdown_string)
        if self.loop == 3 and self.settings.pikachu_lives > 0:
            self.you_died.blitme()
        # elif self.loop == 3 and self.settings.pikachu_lives == 0:
        # lost all lives - game over
        elif self.end_game_its_over:
            self.game_over.blitme()
        # if beat level 1 - make you won msg appear on screen
        elif self.loop == 'beat level':
            self.you_won_msg.blitme() 
        for enemy in self.enemy_group:
            enemy.blitme()
        self.potion_group.draw(self.screen)
        self.shock_powerup_group.draw(self.screen)
        # draw player_lives (pikachu heads), pikachu's health bar and electricity bar
        self.player_lives.prep_heads()
        self.health_bar.blitme()
        self.electric_bar.blitme()
        self.end_level_one.blitme()
        self._prep_score(self.player_score)
        pygame.display.flip()

    def update_whole_rect(self):
        # cycle through platform rect list and move them using scroll speed
        for platf_rect in self.platform_rect_list:
            platf_rect.x -= self.settings.scroll_speed
            # if platform rect is past left side of screen - remove it from the list
            if platf_rect.right <= 0:
                self.platform_rect_list.remove(platf_rect)

    def _pika_life_lost(self):
        if self.loop != 'beat level':
            if self.settings.pikachu_lives == 0:
                # signify end of game - exit program after posting 'game over' to screen
                self.end_game_its_over = True
                self.game_over = ScreenMsg(self, os.path.join('images', 'death', 'game_over.png'))
            else:
                # otherwise - you just lost a life, and level restarts
                self.you_died = ScreenMsg(self, os.path.join('images', 'death', 'you_died.png'))
                self.settings.pika_health = 150
                self.settings.electricity = 150
            self.loop = 3
            pygame.time.set_timer(self.you_died_replay_event, 5000, True)
            self.pikachu = Pikachu(self)
            self.shock_group.empty()
            self.enemy_group.empty()
            self.potion_group.empty()
            self.shock_powerup_group.empty()
            pygame.mouse.set_visible(True)

    def _check_play_button(self, pos):
        button_clicked = self.play_button.rect.collidepoint(pos)
        if button_clicked and not self.game_active and self.loop == 1:
            self.game_active = True
            pygame.mouse.set_visible(False)


if __name__=="__main__":
    pikachu_game = PikaMassacre()
    pikachu_game.run_game()
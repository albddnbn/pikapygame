class Settings:
    def __init__(self):
        self.screen_height = 600
        self.screen_width = 800
        self.scroll_speed = 1
        # framerate
        self.fps = 30
        self.countdown_list = ['3','2','1','GO','']
        # colors
        self.red = (255,0,0)
        self.green = (0,128,0)
        self.blue = (0,0,255)
        # health bar rect
        self.health_bar_rect = (10,60,150,20)
        self.electric_bar_rect = (10,80,150,20)
        # pikachu settings
        self.pikachu_speed = 2
        self.ground_level = 580
        self.max_jump_height = 250
        self.pikachu_lives = 3 # _life_lost function in main.py will restart game -1 life
        self.pika_jump_list = [-20,-15,-15,-15,-10,-10,-10,-9,-9,-9,-9,-7,-7,-7,-7,-7,-7,-5,-5,
                               -5,-5,-5,-5,-4,-4,-4,-4,-3,-3,-3,-3,-3,-3,-3,-2,-2,-1,-1,0,0,0,0,
                                0,0,0,0,0,1,1,2,2,3,3,3,3,3,3,3,4,4,4,4,5,5,5,5,5,5,7,7,7,7,7,7,9,
                                9,9,9,10,10,10,15,15,15,20]
        # speed for the tbolt shot
        self.tbolt_shot_speed = 3
        # pull of gravity if pikachu is falling
        self.gravity_pull = 4
        self.pika_health = 150
        # going to make electricity gradually go up - in the pikachu class
        self.electricity = 150
        self.shock_attack_power = 2
        # set attack power for tbolt_shot
        self.tbolt_attack_power = 20
        # enemy sprite settings
        self.enemy_speed = 1
        self.enemy_max_health = 60
        self.enemy_health_rect = (0,0,60,20)

        # platform creation lists
        self.ground_plot_list = [0,1770,2180,3350,4640,6350,8200,10050,10910]
        self.ground_num_list = [5,3,2,4,2,3,4,1,4]
        self.plat1_plot_list = [360,750,2420,2690,3980,4370,8830,10320]
        self.plat1_num_list = [1,3,1,2,2,1,2,1]
        self.plat2_plot_list = [3080,5690,10590]
        self.plat2_num_list = [1,1,1]
        self.plat3_plot_list = [3350,5960,7370,8080,9730]
        self.plat3_num_list = [1,2,2,1,1]

        self.plat1_5_plot_list = [1260,5030,6860]
        self.plat1_5_num_list = [1,2,3]
        self.plat2_5_plot_list = [1380,5420,7810,9220]
        self.plat2_5_num_list = [2,1,1,3]
        # this list is the rect.bottom points of each enemy
        self.enemy_ground_lvl_list = [480,540,480,540,540,420,360,450,540,390,540]
        # this list is the rect.right points of each enemy
        self.enemy_rect_list = [1110,2030,2930,3710,4880,5810,6200,7160,8560,9520,11290]
        self.enemy_distance_list = [240,240,120,240,120,60,120,300,350,300,350]
        # plot list for the health_potions
        self.potion_plot_list = [1560,3470,5480,8140,9400,10380]
        self.potion_height_list = [390,540,390,360,390,480]
        # plot list for electricity powerups
        self.shock_powerup_plot_list = [1900,3410,7870,9790,10650]
        self.shock_powerup_height_list = [540,360,390,360,420]

        # distance pikachu has to be away from enemy, before enemy considers him 'nearby'
        self.can_see_pikachu = 175
        
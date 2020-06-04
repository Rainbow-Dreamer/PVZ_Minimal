def sounds(x):
    return pygame.mixer.Sound(x).get_raw()


def get_plant(plant_obj, rows=None, columns=None):
    result = deepcopy(plant_obj)
    if result.bullet_sound:
        result.bullet_sound = [
            pygame.mixer.Sound(j)
            if type(j) != list else [pygame.mixer.Sound(k) for k in j]
            for j in result.bullet_sound
        ]
        whole_sounds.extend(result.bullet_sound)
    if result.bullet_sound and result.sound_volume:
        for j in range(len(result.bullet_sound)):
            result.bullet_sound[j].set_volume(result.sound_volume[j])
    result.rows = rows
    result.columns = columns
    return result


def get_zombies(zombies_obj, rows=None, columns=None, appear_time=None):
    result = deepcopy(zombies_obj)
    result.rows = rows
    result.columns = columns
    result.appear_time = appear_time
    return result


class Stage:
    def __init__(self, num_of_waves):
        # number of waves means number of flags (when a big wave of zombies will come)
        self.num_of_waves = num_of_waves
        self.normal_zombies = [[] for i in range(num_of_waves + 1)]
        self.big_waves_zombies = [[] for i in range(num_of_waves)]

    def set_normal(self, num, zombie_ls):
        if num in range(self.num_of_waves + 1):
            self.normal_zombies[num] = zombie_ls

    def set_waves(self, num, zombie_ls):
        if num in range(self.num_of_waves):
            self.big_waves_zombies[num] = zombie_ls

    def set_normal_all(self, *zombie_ls):
        for k in range(len(zombie_ls)):
            self.normal_zombies[k] = zombie_ls[k]

    def set_waves_all(self, *zombie_ls):
        for k in range(len(zombie_ls)):
            self.big_waves_zombies[k] = zombie_ls[k]

    def get(self, num, mode=0):
        if mode == 0:
            return self.normal_zombies[num]
        elif mode == 1:
            return self.big_waves_zombies[num]


class lawnmower:
    def __init__(self, rows, columns, mode=0, move_speed=500, attack=None):
        # if mode == 0, the lawn mower will kill all zombies in the row by setting their hp to 0
        # if mode == 1, the lawn mower will have only give an attack to all of the zombies i the row
        self.rows = rows
        self.columns = columns
        self.mode = mode
        self.move_speed = move_speed
        self.attack = attack


whole_plants_name = None
if whole_plants_name is None:
    whole_plants_name = os.listdir('plant_scripts')
    except_ls = ['__pycache__', '__init__.py', 'plant.py', 'bullets.py']
    for each in except_ls:
        if each in whole_plants_name:
            whole_plants_name.remove(each)
    whole_plants_name = [x[:-3] for x in whole_plants_name]
whole_plants = [(
    x,
    eval(f"__import__('plant_scripts.{x}', fromlist=['plant_scripts']).{x}.img"
         )) for x in whole_plants_name]
modified_file = None
stage_file = os.listdir('stages')
stage_file.remove('__init__.py')
stage_file = [x[:-3] for x in stage_file]

os.chdir('resource/')

lawnmower_rows = [0, 1, 2, 3, 4]
default_lawnmower_rows = deepcopy(lawnmower_rows)
lawnmower_mode = 0
lawnmower_speed = 200
lawnmower_atack = None
lawnmower_img = 'Lawn_mower_2.PNG.png'
no_lawnmower_img = 'no_lawnmower.png'

background_music = 'sounds/Laura Shigihara - Ultimate Battle IN-GAME.ogg'
action_text_place_x = 270
lawn_size = 60
icon_name = 'pvz.ico'
title_name = "PVZ极简版"
screen_size = 900, 650
sunshine_img = 'sun.png'
fall_sunshine_img = 'Sun_PvZ2.png'
shovel_img = 'Shovel.png'
paused_img = 'paused.png'
map_size = 5, 9
default_map_size = deepcopy(map_size)
first_time = True
lawn_photo = 'Almanac_GroundDay.png'
map_img_dict = {'day': 'Almanac_GroundDay.png', 'pool': 'Almanac_GroundPool.jpg', 'empty': 'empty.png'}
map_content = [['day' for i in range(map_size[1])] for j in range(map_size[0])]
default_map_content = deepcopy(map_content)
init_sunshine = 50
sunshine_cooling_time = 10
zombie_explode = 'explode.png'
flag_img = 'Zombie_flagpole.png'
damaged_flag_img = 'Zombie_flagpole2.png'
zombie_head_img = 'Zombatar_Normal_Zombie.PNG.png'
sky_sunshine = 25

choose_seed_volume = 0.5
background_volume = 0.6
sunshine_not_enough = pygame.mixer.Sound("sounds/buzzer.ogg")
choose_plants_sound = pygame.mixer.Sound("sounds/bleep.ogg")
set_plants_sound = pygame.mixer.Sound("sounds/plant.ogg")
unset_plants_sound = pygame.mixer.Sound("sounds/plant2.ogg")
pick_shovel_sound = pygame.mixer.Sound("sounds/shovel.ogg")
get_sunshine_sound = pygame.mixer.Sound("sounds/points.ogg")
plant_bite_sound = pygame.mixer.Sound('sounds/gulp.ogg')

reset_sound = [
    pygame.mixer.Sound('sounds/tap.ogg'),
    pygame.mixer.Sound('sounds/tap2.ogg')
]
pause_sound = pygame.mixer.Sound('sounds/pause.ogg')
lose_sound = pygame.mixer.Sound('sounds/losemusic.ogg')
choose_plants_music = 'sounds/Laura Shigihara - Choose Your Seeds IN-GAME.mp3'
choose_plant_sound = pygame.mixer.Sound('sounds/seedlift.ogg')
zombies_coming_sound = pygame.mixer.Sound('sounds/awooga.ogg')
huge_wave_sound = pygame.mixer.Sound('sounds/hugewave.ogg')
lawnmower_sound = pygame.mixer.Sound('sounds/lawnmower.ogg')
win_sound = pygame.mixer.Sound('sounds/winmusic.ogg')

NULL, PLACE, REMOVE, PAUSE = 0, 1, 2, 3
show_zombies = True
choosed_plants = []
whole_sounds = [
    sunshine_not_enough, choose_plants_sound, set_plants_sound,
    unset_plants_sound, pick_shovel_sound, get_sunshine_sound,
    plant_bite_sound, reset_sound, pause_sound, lose_sound, choose_plant_sound,
    zombies_coming_sound, huge_wave_sound, lawnmower_sound, win_sound
]

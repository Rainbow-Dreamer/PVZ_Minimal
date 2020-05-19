whole_plants_name = ['窝瓜', '豌豆射手', '火炬树桩', '向日葵', '土豆雷', '坚果墙', '爆炸坚果']
zombies_names = ['普通僵尸', '路障僵尸', '读报僵尸', '铁桶僵尸', '撑杆僵尸']


def sounds(x):
    return pygame.mixer.Sound(x).get_raw()

pygame.mixer.init()

with open('common.py', encoding='utf-8') as f:
    exec(f.read())

choosed_zombies = zombies_sample



def get_plant(plant_obj, rows=None, columns=None):
    result = deepcopy(plant_obj)
    if result.bullet_sound:
        result.bullet_sound = [
            pygame.mixer.Sound(j)
            if type(j) != list else [pygame.mixer.Sound(k) for k in j]
            for j in result.bullet_sound
        ]
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


lawnmower_rows = [0, 1, 2, 3, 4]
lawnmower_mode = 0
lawnmower_speed = 200
lawnmower_atack = None
lawnmower_img = 'Lawn_mower_2.PNG.png'
no_lawnmower_img = 'no_lawnmower.png'

background_music = 'sounds/Laura Shigihara - Cerebrawl.mp3'
action_text_place_x = 270

icon_name = 'pvz.ico'
title_name = "PVZ极简版"
screen_size = 900, 600
sunshine_img = 'sun.png'
fall_sunshine_img = 'Sun_PvZ2.png'
shovel_img = 'Shovel.png'
paused_img = 'paused.png'
map_size = 5, 9
lawn_img = 'Almanac_GroundDay.png'
init_sunshine = 150
sunshine_cooling_time = 10
zombie_explode = 'explode.png'
flag_img = 'Zombie_flagpole.png'
damaged_flag_img = 'Zombie_flagpole2.png'
zombie_head_img = 'Zombatar_Normal_Zombie.PNG.png'
brain_img = 'BrainPvZH.png'
sky_sunshine = 25

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
choose_plant_sound = pygame.mixer.Sound('sounds/seedlift.ogg')
zombies_coming_sound = pygame.mixer.Sound('sounds/awooga.ogg')
huge_wave_sound = pygame.mixer.Sound('sounds/hugewave.ogg')
lawnmower_sound = pygame.mixer.Sound('sounds/lawnmower.ogg')
plant_line = 5
NULL, PLACE, REMOVE, PAUSE = 0, 1, 2, 3
choosed_plants = []
os.chdir(abs_path + '/我是僵尸/')
plants_path = 'plant_scripts/'
os.chdir(plants_path)
sys.path.append('.')
whole_plants = [eval(f'__import__("{x}").{x}') for x in whole_plants_name]
stage_file = '我是僵尸关卡.py'
os.chdir('..')
with open(stage_file, encoding='utf-8') as f:
    stage_file_contents = f.read()
os.chdir('../../resource/')
exec(stage_file_contents)

modified_file = None

pygame.mixer.init()
now_time = time.time()
start_time = 5
os.chdir('resource/')


def sounds(x):
    return pygame.mixer.Sound(x).get_raw()


class plant:
    def __init__(self,
                 name,
                 img,
                 price,
                 hp,
                 cooling_time,
                 hp_img=None,
                 attack_interval=None,
                 bullet_img=None,
                 bullet_speed=None,
                 bullet_attack=None,
                 bullet_sound=None,
                 sound_volume=None,
                 self_attack=None,
                 change_mode=0,
                 rows=None,
                 columns=None):
        self.name = name
        self.img = img
        self.price = price
        self.hp = hp
        self.full_hp = hp
        self.cooling_time = cooling_time
        self.hp_img = hp_img
        self.attack_interval = attack_interval
        self.bullet_img = bullet_img
        self.bullet_speed = bullet_speed
        self.bullet_attack = bullet_attack
        self.bullet_sound = bullet_sound
        self.sound_volume = sound_volume
        self.self_attack = self_attack
        self.change_mode = change_mode
        self.rows = rows
        self.columns = columns
        self.status = 1

    def __repr__(self):
        attr_dict = vars(self)
        return '\n'.join([f'{x}: {attr_dict[x]}' for x in attr_dict])


class zombies:
    def __init__(self,
                 name,
                 img,
                 hp,
                 move_speed,
                 attack,
                 attack_speed,
                 attack_sound,
                 dead_sound,
                 hit_sound,
                 hit_sound_ls=None,
                 hp_img=None,
                 rows=None,
                 columns=None,
                 appear_time=None,
                 change_mode=0):
        self.name = name
        self.img = img
        self.hp = hp
        self.full_hp = hp
        self.move_speed = move_speed
        self.attack = attack
        self.attack_speed = attack_speed
        self.attack_sound = attack_sound
        self.dead_sound = dead_sound
        self.hit_sound = hit_sound
        self.hit_sound_ls = hit_sound_ls
        self.hp_img = hp_img
        self.rows = rows
        self.columns = columns
        self.appear_time = appear_time
        self.change_mode = change_mode
        self.status = 0
        self.adjust_col = -1

    def alive(self):
        self.status = 1

    def dead(self):
        self.status = 0

    def __repr__(self):
        attr_dict = vars(self)
        return '\n'.join([f'{x}: {attr_dict[x]}' for x in attr_dict])

    def configure(self, attr, value):
        self.__dict__[attr] = value
        return self


def get_plant(name, rows=None, columns=None):
    result = deepcopy(plant_dict[name])
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


def get_zombies(name, rows=None, columns=None, appear_time=None):
    result = deepcopy(zombies_dict[name])
    result.attack_sound = [pygame.mixer.Sound(j) for j in result.attack_sound]
    result.dead_sound = [
        pygame.mixer.Sound(j)
        if type(j) != list else [pygame.mixer.Sound(k) for k in j]
        for j in result.dead_sound
    ]
    result.hit_sound = [pygame.mixer.Sound(j) for j in result.hit_sound]
    if result.hit_sound_ls:
        for k in range(len(result.hit_sound_ls)):
            current = result.hit_sound_ls[k][1]
            result.hit_sound_ls[k][1] = pygame.mixer.Sound(current) if type(
                current) != list else [pygame.mixer.Sound(y) for y in current]
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

    def get(self, num, mode=0):
        if mode == 0:
            return self.normal_zombies[num]
        elif mode == 1:
            return self.big_waves_zombies[num]


background_music = 'sounds/Laura Shigihara - Ultimate Battle IN-GAME.ogg'
action_text_place_x = 270
action_text_place_y = 440

icon_name = 'pvz.ico'
title_name = "PVZ极简版"
screen_size = 900, 600
sunshine_img = 'sun.png'
fall_sunshine_img = 'Sun_PvZ2.png'
shovel_img = 'Shovel.png'
paused_img = 'paused.png'
map_size = 5, 9
lawn_img = 'Almanac_GroundDay.png'
init_sunshine = 50
sunshine_cooling_time = 10
zombie_explode = 'explode.png'
flag_img = 'Zombie_flagpole.png'
damaged_flag_img = 'Zombie_flagpole2.png'
zombie_head_img = 'Zombatar_Normal_Zombie.PNG.png'
# stage 1-6
#stage_name = '1 - 6'
stage_name = '人海战术'

choose_seed_volume = 0.5
background_volume = 0.6
sunshine_not_enough = pygame.mixer.Sound("sounds/buzzer.ogg")
choose_plants_sound = pygame.mixer.Sound("sounds/bleep.ogg")
set_plants_sound = pygame.mixer.Sound("sounds/plant.ogg")
unset_plants_sound = pygame.mixer.Sound("sounds/plant2.ogg")
pick_shovel_sound = pygame.mixer.Sound("sounds/shovel.ogg")
get_sunshine_sound = pygame.mixer.Sound("sounds/points.ogg")
plant_bite_sound = pygame.mixer.Sound('sounds/gulp.ogg')
regular_attack_sound = [
    sounds(x)
    for x in ['sounds/chomp.ogg', 'sounds/chomp2.ogg', 'sounds/chompsoft.ogg']
]
regular_dead_sound = [
    sounds('sounds/limbs_pop.ogg'),
    [
        sounds('sounds/zombie_falling_1.ogg'),
        sounds('sounds/zombie_falling_1.ogg')
    ]
]
regular_hit_sound = [
    sounds(x)
    for x in ['sounds/splat.ogg', 'sounds/splat2.ogg', 'sounds/splat3.ogg']
]
reset_sound = [
    pygame.mixer.Sound('sounds/tap.ogg'),
    pygame.mixer.Sound('sounds/tap2.ogg')
]
pause_sound = pygame.mixer.Sound('sounds/pause.ogg')
lose_sound = pygame.mixer.Sound('sounds/losemusic.ogg')
choose_plants_music = pygame.mixer.music.load(
    'sounds/Laura Shigihara - Choose Your Seeds IN-GAME.mp3')
choose_plant_sound = pygame.mixer.Sound('sounds/seedlift.ogg')
zombies_coming_sound = pygame.mixer.Sound('sounds/awooga.ogg')
huge_wave_sound = pygame.mixer.Sound('sounds/hugewave.ogg')

plant_dict = {
    '豌豆射手':
    plant(name='豌豆射手',
          img='Peashooter1.png',
          price=100,
          hp=5,
          cooling_time=7.5,
          attack_interval=2,
          bullet_img='pea.png',
          bullet_speed=200,
          bullet_attack=1,
          bullet_sound=(sounds('sounds/throw.ogg'), )),
    '向日葵':
    plant(name='向日葵',
          img='Sunflower1.png',
          price=50,
          hp=5,
          cooling_time=7.5,
          attack_interval=10,
          bullet_img='sun.png'),
    '坚果墙':
    plant(name='坚果墙',
          img='Wall-nut1.png',
          price=50,
          hp=72,
          cooling_time=30,
          hp_img=((2 / 3, 'Wallnut_cracked1.png'), (1 / 3,
                                                    'Wallnut_cracked2.png'))),
    '樱桃炸弹':
    plant(name='樱桃炸弹',
          img='Cherry_Bomb1.png',
          price=150,
          hp=5,
          cooling_time=30,
          attack_interval=2,
          bullet_attack=90,
          bullet_sound=(sounds('sounds/cherrybomb.ogg'), ),
          sound_volume=(0.5, )),
    '窝瓜':
    plant(name='窝瓜',
          img='Squash1.png',
          price=50,
          hp=5,
          cooling_time=30,
          attack_interval=1.5,
          bullet_attack=90,
          bullet_sound=([
              sounds('sounds/squash_hmm.ogg'),
              sounds('sounds/squash_hmm2.ogg')
          ], sounds('sounds/gargantuar_thump.ogg'))),
    '土豆雷':
    plant(name='土豆雷',
          img='Potato_Mine1.png',
          price=25,
          hp=5,
          cooling_time=30,
          attack_interval=15,
          bullet_img='UnarmedPotatoMine.png',
          bullet_attack=90,
          bullet_sound=(sounds('sounds/dirt_rise.ogg'),
                        sounds('sounds/potato_mine.ogg'))),
    '火炬树桩':
    plant(name='火炬树桩',
          img='Torchwood1.png',
          price=175,
          hp=5,
          cooling_time=7.5,
          bullet_img='FirePea.png'),
    '火爆辣椒':
    plant(name='火爆辣椒',
          img='Jalapeno1.png',
          price=125,
          hp=5,
          cooling_time=50,
          attack_interval=2,
          bullet_img='Fire1_1.png',
          bullet_attack=90,
          bullet_sound=(sounds('sounds/jalapeno.ogg'), ))
}

whole_plants = [get_plant(i) for i in plant_dict]
NULL, PLACE, REMOVE, PAUSE = 0, 1, 2, 3
choosed_plants = []
zombies_dict = {
    '普通僵尸':
    zombies(
        name='普通僵尸',
        img='0.png',
        hp=10,
        move_speed=9000,
        attack=1,
        attack_speed=1000,
        attack_sound=regular_attack_sound,
        dead_sound=regular_dead_sound,
        hit_sound=regular_hit_sound,
    ),
    '路障僵尸':
    zombies(name='路障僵尸',
            img='Conehead_Zombie1.png',
            hp=28,
            move_speed=9000,
            attack=1,
            attack_speed=1000,
            attack_sound=regular_attack_sound,
            dead_sound=regular_dead_sound,
            hit_sound=[
                sounds('sounds/plastichit.ogg'),
                sounds('sounds/plastichit2.ogg')
            ],
            hit_sound_ls=[[19, regular_hit_sound]],
            hp_img=((19, '0.png'), ),
            change_mode=2),
    '铁桶僵尸':
    zombies(name='铁桶僵尸',
            img='bucket.png',
            hp=66,
            move_speed=9000,
            attack=1,
            attack_speed=1000,
            attack_sound=regular_attack_sound,
            dead_sound=regular_dead_sound,
            hit_sound=[
                sounds('sounds/shieldhit.ogg'),
                sounds('sounds/shieldhit2.ogg')
            ],
            hit_sound_ls=[[56, regular_hit_sound]],
            hp_img=[(19, 'bucket_first_damage.png'),
                    (38, 'bucket_second_damage.png'), (56, '0.png')],
            change_mode=2)
}

part1 = [
    get_zombies(random.choice(['普通僵尸', '路障僵尸']), random.randint(0, 4),
                8, random.randint(1, 120)) for i in range(20)
]

part2 = [
    get_zombies(random.choice(['普通僵尸', '路障僵尸']), random.randint(0, 4),
                8, random.randint(1, 120)) for i in range(20)
]

part3 = [
    get_zombies(random.choices(['普通僵尸', '路障僵尸','铁桶僵尸'],[0.45,0.45,0.1])[0], random.randint(0, 4), 8,
                random.randint(1, 60)) for i in range(20)
]
big_wave1 = [
    get_zombies('普通僵尸', random.randint(0, 4), 8,
                random.randint(1, 5)) for i in range(25)
]
big_wave2 = [
    get_zombies(random.choice(['普通僵尸', '路障僵尸']), random.randint(0, 4), 8,
                random.randint(1, 5)) for i in range(25)
]
current_stage = Stage(2)
current_stage.set_normal(0, part1)
current_stage.set_normal(1, part2)
current_stage.set_normal(2, part3)
current_stage.set_waves(0, big_wave1)
current_stage.set_waves(1, big_wave2)

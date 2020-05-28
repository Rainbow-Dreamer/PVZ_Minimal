class zombies:
    def __init__(self,
                 name,
                 img,
                 hp,
                 price,
                 move_speed,
                 attack,
                 attack_speed,
                 attack_sound,
                 dead_sound,
                 hit_sound,
                 hit_sound_ls=None,
                 hp_img=None,
                 start_func=None,
                 eachtime_func=None,
                 repause_func=None,
                 other_sound=None,
                 img_transparent=False,
                 rows=None,
                 columns=None,
                 appear_time=None,
                 change_mode=0):
        self.name = name
        self.img = img
        self.hp = hp
        self.full_hp = hp
        self.price = price
        self.move_speed = move_speed
        self.attack = attack
        self.attack_speed = attack_speed
        self.attack_sound = attack_sound
        self.dead_sound = dead_sound
        self.hit_sound = hit_sound
        self.hit_sound_ls = hit_sound_ls
        self.hp_img = hp_img
        self.start_func = start_func
        self.eachtime_func = eachtime_func
        self.repause_func = repause_func
        self.other_sound = other_sound
        self.img_transparent = img_transparent
        self.rows = rows
        self.columns = columns
        self.appear_time = appear_time
        self.change_mode = change_mode
        self.status = 0
        self.adjust_col = -1
        self.stop = False

    def alive(self):
        self.status = 1

    def dead(self):
        self.status = 0

    def __repr__(self):
        attr_dict = vars(self)
        return '\n'.join([f'{x}: {attr_dict[x]}' for x in attr_dict])

    def configure(self, **kwargs):
        self.__dict__.update(**kwargs)
        return self

    def runs(self, games, num=0):
        if num == 0:
            self.start_func(self, games)
        elif num == 1:
            self.eachtime_func(self, games)
        elif num == 2:
            self.repause_func(self, games)


regular_attack_sound = [
    'sounds/chomp.ogg', 'sounds/chomp2.ogg', 'sounds/chompsoft.ogg'
]
regular_dead_sound = [
    'sounds/limbs_pop.ogg',
    ['sounds/zombie_falling_1.ogg', 'sounds/zombie_falling_1.ogg']
]
regular_hit_sound = [
    'sounds/splat.ogg', 'sounds/splat2.ogg', 'sounds/splat3.ogg'
]

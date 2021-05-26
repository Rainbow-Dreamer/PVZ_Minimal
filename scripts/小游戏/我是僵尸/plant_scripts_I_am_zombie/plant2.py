class plant2:
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
                 func=None,
                 bullet_func=None,
                 effects=None,
                 no_cooling_start=False,
                 is_bullet=True,
                 dead_normal=True,
                 img_transparent=False,
                 use_bullet_img_first=False,
                 other_img=None,
                 information=None,
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
        self.bullet_img_name = bullet_img
        self.bullet_speed = bullet_speed
        self.bullet_attack = bullet_attack
        self.bullet_sound = bullet_sound
        self.sound_volume = sound_volume
        self.self_attack = self_attack
        self.change_mode = change_mode
        self.func = func
        self.bullet_func = bullet_func
        self.effects = effects
        self.no_cooling_start = no_cooling_start
        self.is_bullet = is_bullet
        self.dead_normal = dead_normal
        self.img_transparent = img_transparent
        self.use_bullet_img_first = use_bullet_img_first
        self.other_img = other_img
        self.information = information
        self.rows = rows
        self.columns = columns
        self.status = 1

    def __repr__(self):
        attr_dict = vars(self)
        return '\n'.join([f'{x}: {attr_dict[x]}' for x in attr_dict])

    def runs(self, games):
        self.func(self, games)
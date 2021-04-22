from copy import deepcopy


def day_check(games, block):
    if block.types == 'pool':
        if block.plants and block.plants.name == '荷叶' and not block.plants.contain_plants:
            return True
        else:
            games.action_text.set('这个植物需要种植在荷叶上')
            return False
    return block.plants is None


def when_plant(games, block, self):
    if block.types == 'pool' and block.plants and block.plants.name == '荷叶':
        block.plants.contain_plants = self
    elif block.types == 'day':
        block.plants = self


class plant:
    def __init__(self,
                 name=None,
                 img=None,
                 price=None,
                 hp=None,
                 cooling_time=None,
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
                 away_func=None,
                 away_self_func=None,
                 effects=None,
                 no_cooling_start=False,
                 is_bullet=True,
                 dead_normal=True,
                 img_transparent=False,
                 use_bullet_img_first=False,
                 other_img=None,
                 information=None,
                 plant_range=[day_check],
                 plant_func=when_plant,
                 rows=None,
                 columns=None):
        self.name = name
        self.img = img
        self.img_name = deepcopy(img)
        self.price = price
        self.hp = hp
        self.full_hp = hp
        self.cooling_time = cooling_time
        self.hp_img = hp_img
        self.attack_interval = attack_interval
        self.bullet_img = bullet_img
        self.bullet_img_name = deepcopy(bullet_img)
        self.bullet_speed = bullet_speed
        self.bullet_attack = bullet_attack
        self.bullet_sound = bullet_sound
        self.sound_volume = sound_volume
        self.self_attack = self_attack
        self.change_mode = change_mode
        self.func = func
        self.bullet_func = bullet_func
        self.away_func = away_func
        self.away_self_func = away_self_func
        self.effects = effects
        self.no_cooling_start = no_cooling_start
        self.is_bullet = is_bullet
        self.dead_normal = dead_normal
        self.img_transparent = img_transparent
        self.use_bullet_img_first = use_bullet_img_first
        self.other_img = other_img
        if other_img:
            self.other_img_name = [deepcopy(t) for t in other_img]
        else:
            self.other_img_name = None
        self.information = information
        self.plant_range = plant_range
        self.plant_func = plant_func
        self.rows = rows
        self.columns = columns
        self.status = 1

    def __repr__(self):
        attr_dict = vars(self)
        return '\n'.join([f'{x}: {attr_dict[x]}' for x in attr_dict])

    def __deepcopy__(self, memo):
        if type(self.img) != str:
            self.img = deepcopy(self.img_name)
            self.bullet_img = deepcopy(self.bullet_img_name)
            if self.other_img:
                self.other_img = deepcopy(self.other_img_name)
            del self.button
        result = plant()
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result

    def runs(self, games):
        self.func(self, games)
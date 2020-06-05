from plant import plant
from copy import deepcopy


info = '''
坚果小队

特性：占据地图的一整个竖排，在自己被吃光之前，所有列上的僵尸都过不来。
所有列的僵尸都可以啃咬坚果小队，整个坚果小队的生命值是共享的，
每一列的僵尸的啃咬都会影响这个生命值。
'''

def start_plant_wallnut(self, games):
    i, j = self.rows, self.columns
    other_rows = list(range(games.map_rows))
    other_rows.remove(i)
    if all(games.blocks[x][j].plants is None for x in other_rows):
        wallnut_plant = [k for k in games.plants_generate if k.name == '坚果小队'][0]
        self.whole_wallnuts = []
        
        self.share_hp = [400]
        for each in other_rows:
            current = games.blocks[each][j]
            current.plants = games.get_plant(wallnut_plant, each, j)
            games.make_img(current.plants)
            current.configure(image=current.plants.img)
            current.plants.time = games.current_time
            current.plants.button = self.button
            self.whole_wallnuts.append(current.plants)
        self.pre_hp = deepcopy(self.hp)
        for each in self.whole_wallnuts:
            each.func = long_wallnut_check
            each.pre_hp = deepcopy(each.hp)
            each.share_hp = self.share_hp
            each.whole_wallnuts = self.whole_wallnuts
        self.whole_wallnuts.append(self)
        self.func = long_wallnut_check
        
    
    

def long_wallnut_check(self, games):
    if self.share_hp[0] <= 0:
        whole_rows = list(range(games.map_rows))
        for each in whole_rows:
            current = games.blocks[each][self.columns]
            current.plants = None
            current.configure(image=games.lawn_photo)       
        games.plant_bite_sound.play()
        games.action_text.set(
            f'第{self.columns+1}列的植物坚果小队被吃掉了'
        )
        return
    if self.pre_hp - self.hp > 0:
        diff = self.pre_hp - self.hp
        self.share_hp[0] -= diff
        self.pre_hp = deepcopy(self.hp)
        for each in self.whole_wallnuts:
            if each != self:
                each.hp -= diff
                each.pre_hp -= diff
        

def away(self, games):
    i, j = self.rows, self.columns
    other_rows = list(range(games.map_rows))
    other_rows.remove(i)
    for each in other_rows:
        current = games.blocks[each][j]
        current.plants = None
        current.configure(image=games.lawn_photo)    

坚果小队 = plant(name='坚果小队',
            img='坚果小队.png',
            price=250,
            hp=400,
            cooling_time=30,
            func=start_plant_wallnut,
            away_func=away,
            dead_normal=False,
            information=info,
            hp_img=((2 / 3, 'long_wallnut_crack1.png'), (1 / 3,
                                                      'long_wallnut_crack2.png')))

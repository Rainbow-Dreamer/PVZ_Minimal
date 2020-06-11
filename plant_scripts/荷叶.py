from plant import plant
def lily_check(games, block):
    if block.types != 'pool':
        games.action_text.set('荷叶需要种植在水面上')
        return False
    return block.plants is None

def lily_func(self, games):
    if self.contain_plants:
        if self.contain_plants.func:
            self.contain_plants.runs(games)
def lily_away(self, games, block):
    j, k = self.rows, self.columns
    if self.contain_plants:
        if self.contain_plants.away_func:
            self.contain_plants.away_func(self.contain_plants, games)
        if self.contain_plants.away_self_func:
            self.contain_plants.away_self_func(self.contain_plants, games, block)
        else:
            block.configure(image=self.img)
            games.unset_plants_sound.play()
            games.action_text.set(
                f'你铲除了第{j+1}行，第{k+1}列的植物{self.contain_plants.name}')
        self.contain_plants.status = 0
        self.contain_plants = None
    else:
        block.configure(image=games.map_img_dict['pool'])
        games.unset_plants_sound.play()
        games.action_text.set(
            f'你铲除了第{j+1}行，第{k+1}列的植物{self.name}')
        block.plants.status = 0
        block.plants = None
    

荷叶 = plant(name='荷叶',
            img='荷叶.png',
            price=25,
            hp=5,
            cooling_time=7.5,
            plant_range=[lily_check],
            func=lily_func,
            plant_func=None,
            away_self_func=lily_away)
荷叶.contain_plants = None

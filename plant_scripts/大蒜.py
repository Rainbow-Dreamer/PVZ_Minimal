from plant import plant
import random
def garlic_check(self, obj, games):
    if hasattr(obj, 'garlic_used') and obj.garlic_used:
        if games.current_time - self.start_time >= 1.5:
            available_rows = [obj.rows-1, obj.rows+1]
            available_rows = [x for x in available_rows if 0 <= x < games.map_rows]
            obj.garlic_used = False
            obj.stop = False
            obj.rows = random.choice(available_rows)
            obj.start_func(obj, games)
            return
    else:
        obj.stop = True
        obj.garlic_used = True
        self.start_time = games.current_time
        random.choice(self.bullet_sound).play()
    games.after(10, lambda: garlic_check(self, obj, games))
        
        
大蒜 = plant(name='大蒜',
             img='Garlic1.png',
             price=50,
             hp=21,
             cooling_time=7.5,
             attack_interval=1.5,
             bullet_attack=0,
             bullet_sound=('sounds/yuck.ogg', 'sounds/yuck2.ogg'),
             sound_volume=(0.5, 0.5),
             effects={'zombies':garlic_check})
大蒜.used = 0
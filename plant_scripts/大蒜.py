from plant import plant
import random
def garlic_check(self, obj, games):
    obj.stop = True
    obj.nexted_plants = None
    self.start_time = games.current_time
    random.choice(self.bullet_sound).play()
    goto_another_row(self, obj, games)
    
def goto_another_row(self, obj, games):
    if obj.hp <= 0:
        return
    if games.current_time - self.start_time >= 1.5:
        available_rows = [obj.rows-1, obj.rows+1]
        available_rows = [x for x in available_rows if 0 <= x < games.map_rows]
        obj.stop = False
        obj.rows = random.choice(available_rows)
        obj.button.grid(row=obj.rows, column=obj.columns)
        obj.start_func(obj, games)
        return
    else:
        games.after(10, lambda: goto_another_row(self, obj, games)) 
        return
        
大蒜 = plant(name='大蒜',
             img='大蒜.png',
             price=50,
             hp=21,
             cooling_time=7.5,
             attack_interval=1.5,
             bullet_attack=0,
             bullet_sound=('sounds/yuck.ogg', 'sounds/yuck2.ogg'),
             sound_volume=(0.5, 0.5),
             effects={'zombies':garlic_check})
大蒜.used = 0
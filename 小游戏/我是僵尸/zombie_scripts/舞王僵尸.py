from zombies import *
from regular import *
import random
from 普通僵尸 import 普通僵尸 as 舞伴僵尸
舞伴僵尸.img = 'Old_Backup_Dancer.png'
舞伴僵尸.name = '舞伴僵尸'
舞伴僵尸.with_stop = False

def dance_with_move(self, games, columns_move=0, rows_move=0):
    if self.hp <= 0 or self.status == 0:
        return    
    if self.with_stop or games.mode == games.PAUSE:
        return
    if self.status == 0:
        return
    check_if_plants = games.blocks[self.rows][self.columns + columns_move].plants
    if check_if_plants is not None:
        self.eating = True
        self.adjust_col = -1
        self.nexted_plants = check_if_plants
        dance_with_eat_plants(games, self.nexted_plants, self)
        return      
    self.rows += rows_move
    self.columns += columns_move
    if self.columns < 0:
        if games.brains[self.rows] > 0:
            if type(self.attack_sound) == list:
                random.choice(self.attack_sound).play()
            else:
                self.attack_sound.play()
            games.brains[self.rows] -= 1
            if games.brains[self.rows] <= 0:
                games.brains_show[self.rows].configure(image=games.no_brain_img)
                games.plant_bite_sound.play()
            games.after(self.attack_speed,
                        lambda: zombie_move(self, games))
        else:
            self.button.destroy()     
        return        

    i, j = self.rows, self.columns
    self.button.grid(row=i, column=j)
    i, j = self.rows, self.columns
    current_grid = games.maps.grid_slaves(row=i, column=j)
    current_bullets = [
        x for x in current_grid if hasattr(x, 'bullet_img_name')
        and x.bullet_img_name in games.bullets_ls
    ]
    if current_bullets:
        attack_bullet = current_bullets[0]
        attack_bullet.bullet_sound[0].play()
        self.hp -= attack_bullet.attack
        attack_bullet.stop = True




def dance_with_eat_plants(games, plants, self):
    if games.mode != games.PAUSE:
        if plants is None or plants.hp <= 0 or plants.status == 0 or self.hp <= 0:
            self.columns += self.adjust_col
            self.button.grid(row=self.rows, column=self.columns)
            self.eating = False
            return
        else:
            if type(self.attack_sound) == list:
                random.choice(self.attack_sound).play()
            else:
                self.attack_sound.play()
            if plants.name == '向日葵':
                for t in range(2):
                    flower_sunshine = games.make_button(games.maps,image=games.flower_sunshine_img)
                    flower_sunshine.configure(command=lambda sun=flower_sunshine, obj=plants: games.flower_get_sunshine(sun, obj))
                    flower_sunshine.image = games.fall_sunshine_img
                    flower_sunshine.grid(row=plants.rows, column=plants.columns)
            plants.hp -= self.attack
            if plants.effects:
                if 'zombies' in plants.effects:
                    plants.effects['zombies'](plants, self, games)
            if self.stop:
                self.columns += self.adjust_col
                self.button.grid(row=self.rows, column=self.columns)        
                self.eating = False
                return
            games.after(self.attack_speed,
                        lambda: dance_with_eat_plants(games, plants, self))


def dance_with_repause(self, games):
    if self.next_to_plants:
        games.after(self.attack_speed,
                    lambda: dance_eat_plants(games, self.nexted_plants, self))

  


舞伴僵尸.start_func = zombie_move
舞伴僵尸.eachtime_func = None
舞伴僵尸.repause_func = dance_with_repause
舞伴僵尸.eating = False


def calls(self, games, i, j):
    available_rows = [[i - 1, j], [i + 1, j], [i, j - 1], [i, j + 1]]
    available_rows = [
        x for x in available_rows
        if 0 <= x[0] < games.map_rows and 0 <= x[1] < games.map_columns
    ]
    for each_place in available_rows:
        current_obj = games.get_zombies(舞伴僵尸, *each_place)
        current_obj.appear_time = games.current_time - games.zombie_time
        current_obj.adjust_col = 0
        games.make_img(current_obj)
        games.set_zombies(current_obj)
        current_obj.alive()
        current_obj.replace = False
        current_obj.with_stop = True
        current_obj.button.grid(row=current_obj.rows,
                                column=current_obj.columns)
        self.calls_zombies.append(current_obj)
        games.whole_zombies.append(current_obj)
    self.first_plant = True


def dance_move(self, games, columns_move=0, rows_move=0):
    if self.stop or games.mode == games.PAUSE:
        return
    if self.status == 0:
        return

    check_if_plants2 = games.blocks[self.rows][self.columns].plants
    if check_if_plants2:
        self.next_to_plants = True
        self.nexted_plants = check_if_plants2
        self.adjust_col = 0        
        if not self.first_plant:
            calls(self, games, self.rows, self.columns)   
            self.time = games.current_time
        
        return
    self.rows += rows_move
    self.columns += columns_move
    if self.columns < 0:
        if games.brains[self.rows] > 0:
            if type(self.attack_sound) == list:
                random.choice(self.attack_sound).play()
            else:
                self.attack_sound.play()
            games.brains[self.rows] -= 1
            if games.brains[self.rows] <= 0:
                games.brains_show[self.rows].configure(image=games.no_brain_img)
                games.plant_bite_sound.play()
            games.after(self.attack_speed,
                        lambda: zombie_move(self, games))
        else:
            self.button.destroy()     
        return        

    i, j = self.rows, self.columns
    self.button.grid(row=i, column=j)
    current_grid = games.maps.grid_slaves(row=i, column=j)
    current_bullets = [
        x for x in current_grid if hasattr(x, 'bullet_img_name')
        and x.bullet_img_name in games.bullets_ls
    ]
    if current_bullets:
        attack_bullet = current_bullets[0]
        attack_bullet.bullet_sound[0].play()
        self.hp -= attack_bullet.attack
        attack_bullet.stop = True


def call_new(self, games, each, k):
    if self.hp > 0:
        current_obj = games.get_zombies(舞伴僵尸, each.rows, each.columns)
        current_obj.appear_time = games.current_time - games.zombie_time
        current_obj.adjust_col = 0
        self.calls_zombies[k] = current_obj
        games.make_img(current_obj)
        games.set_zombies(current_obj)
        current_obj.alive()
        current_obj.replace = False
        current_obj.button.grid(row=current_obj.rows,
                                column=current_obj.columns)
        games.whole_zombies.append(current_obj)


def dance_next_to_plant(self, games):
    if self.hp <= 0 or self.status == 0:
        for each in self.calls_zombies:
            each.stop = False
            each.eachtime_func = next_to_plant
            each.repause_func = repause
            each.start_func(each, games)
            
    
    if self.next_to_plants:
        self.next_to_plants = False
        self.eating = True
        self.eat_time = games.current_time
        games.after(self.attack_speed,
                    lambda: dance_eat_plants(games, self.nexted_plants, self))        
    if self.first_plant:
        for k in range(len(self.calls_zombies)):
            each = self.calls_zombies[k]
            if each.hp <= 0:
                if not each.replace:
                    each.replace = True
                    games.after(3000, lambda each=each, k=k: call_new(self, games, each, k))
    
    if self.eating or any(x.eating for x in self.calls_zombies):
        self.time = games.current_time
        for each in self.calls_zombies:
            each.with_stop = True
    else:
        for each in self.calls_zombies:
            each.with_stop = False   
        if games.current_time - self.time >= self.move_speed:
            self.time = games.current_time
            dance_move(self, games, -1)
            for each in self.calls_zombies:
                dance_with_move(each, games, -1)   

def dance_repause(self, games):
    if self.next_to_plants:
        games.after(self.attack_speed,
                    lambda: dance_eat_plants(games, self.nexted_plants, self))
    else:
        dance_move(self, games)


def dance_eat_plants(games, plants, self):
    
    if self.stop:
        self.time += (games.current_time - self.eat_time)
        self.next_to_plants = False
        self.eating = False
        return
    if games.mode != games.PAUSE:
        if plants is None or plants.hp <= 0 or plants.status == 0 or self.hp <= 0:
            self.time += (games.current_time - self.eat_time)
            self.next_to_plants = False
            self.eating = False
            return
        else:
            if type(self.attack_sound) == list:
                random.choice(self.attack_sound).play()
            else:
                self.attack_sound.play()
            if plants.name == '向日葵':
                for t in range(2):
                    flower_sunshine = games.make_button(games.maps,image=games.flower_sunshine_img)
                    flower_sunshine.configure(command=lambda sun=flower_sunshine, obj=plants: games.flower_get_sunshine(sun, obj))
                    flower_sunshine.image = games.fall_sunshine_img
                    flower_sunshine.grid(row=plants.rows, column=plants.columns)
            plants.hp -= self.attack
            if plants.effects:
                if 'zombies' in plants.effects:
                    plants.effects['zombies'](plants, self, games)
            if self.stop:
                self.time += (games.current_time - self.eat_time)
                self.next_to_plants = False
                self.eating = False
                return
            games.after(self.attack_speed,
                        lambda: dance_eat_plants(games, plants, self))    
    


舞王僵尸 = zombies(name='舞王僵尸',
               img='Old_Dancing_Zombie1.png',
               hp=17,
               move_speed=5,
               price=350,
               attack=1,
               attack_speed=1000,
               attack_sound=regular_attack_sound,
               dead_sound=regular_dead_sound,
               hit_sound=regular_hit_sound,
               start_func=dance_move,
               eachtime_func=dance_next_to_plant,
               repause_func=dance_repause)
舞王僵尸.calls_zombies = []
舞王僵尸.first_plant = False
舞伴僵尸.move_speed = 舞王僵尸.move_speed
舞王僵尸.eating = False
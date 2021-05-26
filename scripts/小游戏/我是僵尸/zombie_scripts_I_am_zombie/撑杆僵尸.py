from zombies2 import *
from regular import *


def pole_zombies_move(self,
                      games,
                      columns_move=0,
                      rows_move=0):
    if self.stop or games.mode == games.PAUSE:
        return
    if self.hp <= 0 or self.status == 0:
        return
    check_if_plants = games.blocks[self.rows][self.columns].plants
    if check_if_plants:
        if self.has_pole:
            self.other_sound[0].play()
            self.has_pole = 0
            if columns_move == 0:
                self.columns -= 1            
        else:
            self.next_to_plants = True
            self.nexted_plants = check_if_plants
            self.adjust_col = -1
            return
    else:
        check_if_plants2 = games.blocks[self.rows][self.columns +
                                                   columns_move].plants
        if check_if_plants2:
            if self.has_pole:
                self.columns -= 1
                self.other_sound[0].play()
                self.has_pole = 0
            else:
                self.columns += columns_move
                self.next_to_plants = True
                self.nexted_plants = check_if_plants2
                self.adjust_col = 0
                return
   
    self.rows += rows_move
    self.columns += columns_move
    if self.columns < 0:
        self.button.grid(row=self.rows, column=0)
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


撑杆僵尸 = zombies2(name='撑杆僵尸',
               img='Pole_Vaulting_Zombie1.png',
               hp=17,
               price=75,
               move_speed=6,
               attack=1,
               attack_speed=1000,
               attack_sound=regular_attack_sound,
               dead_sound=regular_dead_sound,
               hit_sound=regular_hit_sound,
               start_func=pole_zombies_move,
               eachtime_func=lambda self, games: next_to_plant(self, games, move_func=pole_zombies_move),
               repause_func=repause,
               other_sound=['sounds/polevault.ogg'])
撑杆僵尸.has_pole = 1

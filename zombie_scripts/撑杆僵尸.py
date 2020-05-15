from zombies import *
from regular import *


def pole_zombies_move(self,
                      games,
                      columns_move=0,
                      rows_move=0,
                      stop=False,
                      reset=False):
    if reset:
        self.adjust_col = -1
    if stop or games.mode == games.PAUSE:
        return
    if self.status == 0:
        return
    check_if_plants = games.blocks[self.rows][self.columns].plants
    if check_if_plants is not None:
        if self.has_pole:
            self.other_sound[0].play()
            self.has_pole = 0
        else:
            self.next_to_plants = True
            self.nexted_plants = check_if_plants
            self.adjust_col = -1
            return
    check_if_plants2 = games.blocks[self.rows][self.columns +
                                               columns_move].plants
    if check_if_plants2 is not None:
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
        lawnmower_here = games.lawnmowers[self.rows]
        if lawnmower_here != 0:
            generate_lawnmower = games.make_button(
                games.maps,
                image=games.lawnmower_img,
                command=lambda: games.action_text.set('我是一辆小推车'))
            generate_lawnmower.image = games.lawnmower_img
            generate_lawnmower.__dict__.update(lawnmower_here.__dict__)
            if generate_lawnmower.mode == 0:
                self.hp = 0
                self.status = 0
                games.killed_zombies += 1
                games.current_killed_zombies += 1
                games.killed_zombies_text.set(f'杀死僵尸数: {games.killed_zombies}')
                games.zombie_dead_normal(self)
            elif generate_lawnmower.mode == 1:
                self.hp -= generate_lawnmower.attack
            games.lawnmower_move(generate_lawnmower)
            lawnmower_here.show.configure(
                image=games.no_lawnmower_img,
                command=lambda: games.action_text.set('这里没有小推车了'))
            lawnmower_here.show.grid(row=self.rows, column=0)
            games.lawnmowers[self.rows] = 0
            return

        else:
            games.lose()
            games.mode = games.PAUSE
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
    games.after(self.move_speed, lambda: pole_zombies_move(self, games, -1))


撑杆僵尸 = zombies(name='撑杆僵尸',
               img='Pole_Vaulting_Zombie1.png',
               hp=17,
               move_speed=6000,
               attack=1,
               attack_speed=1000,
               attack_sound=regular_attack_sound,
               dead_sound=regular_dead_sound,
               hit_sound=regular_hit_sound,
               start_func=pole_zombies_move,
               eachtime_func=next_to_plant,
               repause_func=repause,
               other_sound=['sounds/polevault.ogg'])
撑杆僵尸.has_pole = 1

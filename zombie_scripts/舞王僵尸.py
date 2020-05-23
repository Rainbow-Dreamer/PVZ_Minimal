from zombies import *
from regular import *
import random
from 普通僵尸 import 普通僵尸 as 舞伴僵尸
舞伴僵尸.img = 'Old_Backup_Dancer.png'
舞伴僵尸.name = '舞伴僵尸'


def dance_with_move(self, games, columns_move=0, rows_move=0, reset=False):
    if reset:
        self.adjust_col = -1
    if self.stop or games.mode == games.PAUSE:
        return
    if self.status == 0:
        return
    check_if_plants = games.blocks[self.rows][self.columns].plants
    if check_if_plants is not None:
        self.next_to_plants = True
        self.nexted_plants = check_if_plants
        self.adjust_col = -1
        return
    check_if_plants2 = games.blocks[self.rows][self.columns +
                                               columns_move].plants
    if check_if_plants2 is not None:
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


def dance_with_next_to_plant(self, games):
    if self.next_to_plants:
        self.next_to_plants = False
        self.eating = True
        games.after(
            self.attack_speed,
            lambda: dance_with_eat_plants(games, self.nexted_plants, self))


def dance_with_eat_plants(games, plants, self):
    if games.mode != games.PAUSE:
        if plants is None or plants.hp <= 0 or plants.status == 0 or self.hp <= 0:
            self.next_to_plants = False
            self.eating = False
            return
        else:
            if type(self.attack_sound) == list:
                random.choice(self.attack_sound).play()
            else:
                self.attack_sound.play()
            plants.hp -= self.attack
            if plants.effects:
                if 'zombies' in plants.effects:
                    plants.effects['zombies'](plants, self, games)
            games.after(self.attack_speed,
                        lambda: dance_with_eat_plants(games, plants, self))


def dance_with_repause(self, games):
    if self.next_to_plants:
        games.after(self.attack_speed,
                    lambda: dance_eat_plants(games, self.nexted_plants, self))


舞伴僵尸.start_func = None
舞伴僵尸.eachtime_func = dance_with_next_to_plant
舞伴僵尸.repause_func = dance_with_repause
舞伴僵尸.eating = False


def calls(self, games, i, j):
    available_rows = [[i - 1, j], [i + 1, j], [i, j - 1], [i, j + 1]]
    available_rows = [
        x for x in available_rows
        if 0 <= x[0] < games.map_rows and 0 <= x[1] < games.map_columns
    ]
    for each_place in available_rows:
        games.current_zombies_num += 1
        current_obj = games.get_zombies(舞伴僵尸, *each_place)
        games.set_zombies(current_obj)
        current_obj.alive()
        current_obj.button.grid(row=current_obj.rows,
                                column=current_obj.columns)
        self.calls_zombies.append(current_obj)
        games.whole_zombies.append(current_obj)
    self.first_plant = True


def dance_move(self, games, columns_move=0, rows_move=0, reset=False):
    if self.hp <= 0:
        for each in self.calls_zombies:
            each.start_func = zombie_move
            each.eachtime_func = next_to_plant
            each.repause_func = repause
            each.start_func(each, games)
    if reset:
        self.adjust_col = -1
    if self.stop or games.mode == games.PAUSE:
        return
    if self.status == 0:
        return

    check_if_plants = games.blocks[self.rows][self.columns].plants
    if check_if_plants:
        if not self.first_plant:
            calls(self, games, self.rows, self.columns)
        self.next_to_plants = True
        self.nexted_plants = check_if_plants
        self.adjust_col = -1
        return
    check_if_plants2 = games.blocks[self.rows][self.columns +
                                               columns_move].plants
    if check_if_plants2:
        self.columns += columns_move
        if not self.first_plant:
            calls(self, games, self.rows, self.columns)
        self.next_to_plants = True
        self.nexted_plants = check_if_plants2
        self.adjust_col = 0
        return
    if (games.map_columns -
        (self.columns + columns_move) >= 4) and (not self.first_plant):
        calls(self, games, self.rows, self.columns + columns_move)
    if not any(x.eating for x in self.calls_zombies):
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
                    games.killed_zombies_text.set(
                        f'杀死僵尸数: {games.killed_zombies}')
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
    for each in self.calls_zombies:
        games.after(each.move_speed,
                    lambda each=each: dance_with_move(each, games, -1))
    games.after(self.move_speed, lambda: dance_move(self, games, -1))


def dance_next_to_plant(self, games):
    if self.first_plant:
        for each in self.calls_zombies:
            if each.hp <= 0:
                games.current_zombies_num += 1
                current_obj = games.get_zombies(舞伴僵尸, each.rows, each.columns)
                games.set_zombies(current_obj)
                current_obj.alive()
                current_obj.button.grid(row=current_obj.rows,
                                        column=current_obj.columns)
                self.calls_zombies.append(current_obj)
                games.whole_zombies.append(current_obj)
    if any(x.eating for x in self.calls_zombies) or self.next_to_plants:
        for each in self.calls_zombies:
            each.stop = True
    else:
        for each in self.calls_zombies:
            each.stop = False
    if self.next_to_plants:
        self.next_to_plants = False
        self.eating = True
        games.after(self.attack_speed,
                    lambda: dance_eat_plants(games, self.nexted_plants, self))


def dance_repause(self, games):
    if self.next_to_plants:
        games.after(self.attack_speed,
                    lambda: dance_eat_plants(games, self.nexted_plants, self))
    else:
        dance_move(self, games)


def dance_eat_plants(games, plants, self):
    if self.stop:
        self.next_to_plants = False
        return
    if games.mode != games.PAUSE:
        if plants is None or plants.hp <= 0 or plants.status == 0 or self.hp <= 0:
            self.eating = False
            self.next_to_plants = False
            games.after(
                self.move_speed,
                lambda: dance_move(self, games, self.adjust_col, reset=True))
            return
        else:
            if type(self.attack_sound) == list:
                random.choice(self.attack_sound).play()
            else:
                self.attack_sound.play()
            plants.hp -= self.attack
            if plants.effects:
                if 'zombies' in plants.effects:
                    plants.effects['zombies'](plants, self, games)
            if self.stop:
                self.next_to_plants = False
                return
            games.after(self.attack_speed,
                        lambda: dance_eat_plants(games, plants, self))


舞王僵尸 = zombies(name='舞王僵尸',
               img='Old_Dancing_Zombie1.png',
               hp=17,
               move_speed=2000,
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
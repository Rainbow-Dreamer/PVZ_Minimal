import random


def zombie_move(self, games, columns_move=0, rows_move=0):
    if self.stop or games.mode == games.PAUSE:
        return
    if self.hp <= 0 or self.status == 0:
        return
    check_if_plants = games.blocks[self.rows][self.columns].plants
    if check_if_plants is not None:
        if check_if_plants.name == '荷叶' and check_if_plants.contain_plants:
            self.nexted_plants = check_if_plants.contain_plants
        else:
            self.nexted_plants = check_if_plants
        self.next_to_plants = True
        self.adjust_col = -1
        return
    check_if_plants2 = games.blocks[self.rows][self.columns +
                                               columns_move].plants
    if check_if_plants2 is not None:
        if check_if_plants2.name == '荷叶' and check_if_plants2.contain_plants:
            self.nexted_plants = check_if_plants2.contain_plants
        else:
            self.nexted_plants = check_if_plants2
        self.next_to_plants = True
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


def next_to_plant(self, games, move_func=0):
    if self.hp > 0:
        if not self.eating and not self.stop:
            if games.current_time - self.time >= self.move_speed:
                self.time = games.current_time
                if move_func == 0:
                    zombie_move(self, games, -1)
                else:
                    move_func(self, games, -1)
        if self.next_to_plants:
            self.next_to_plants = False
            self.eat_time = games.current_time
            self.eating = True
            games.after(
                self.attack_speed,
                lambda: zombie_eat_plants(games, self.nexted_plants, self))


def repause(self, games):
    if self.next_to_plants:
        games.after(self.attack_speed,
                    lambda: zombie_eat_plants(games, self.nexted_plants, self))
    else:
        zombie_move(self, games, 0)


def zombie_eat_plants(games, plants, self):
    if self.stop:
        self.time += (games.current_time - self.eat_time)
        self.next_to_plants = False
        self.eating = False
        self.adjust_col = -1
        return
    if games.mode != games.PAUSE:
        if plants is None or plants.hp <= 0 or plants.status == 0 or self.hp <= 0:
            self.time += (games.current_time - self.eat_time)
            self.next_to_plants = False
            self.eating = False
            self.adjust_col = -1
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
                self.time += (games.current_time - self.eat_time)
                self.next_to_plants = False
                self.eating = False
                self.adjust_col = -1
                return
            games.after(self.attack_speed,
                        lambda: zombie_eat_plants(games, plants, self))

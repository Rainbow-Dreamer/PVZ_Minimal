import random


def zombie_move(self, games, columns_move=0, rows_move=0, reset=False):
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
    games.after(self.move_speed, lambda: zombie_move(self, games, -1))


def next_to_plant(self, games):
    if self.next_to_plants:
        self.next_to_plants = False
        games.after(self.attack_speed,
                    lambda: zombie_eat_plants(games, self.nexted_plants, self))


def repause(self, games):
    if self.next_to_plants:
        games.after(self.attack_speed,
                    lambda: zombie_eat_plants(games, self.nexted_plants, self))
    else:
        zombie_move(self, games, 0)


def zombie_eat_plants(games, plants, self):
    if self.stop:
        self.next_to_plants = False
        return    
    if games.mode != games.PAUSE:
        if plants is None or plants.hp <= 0 or plants.status == 0 or self.hp <= 0:
            self.next_to_plants = False
            games.after(
                self.move_speed,
                lambda: zombie_move(self, games, self.adjust_col, reset=True))
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
                self.next_to_plants = False
                return    
            games.after(self.attack_speed,
                        lambda: zombie_eat_plants(games, plants, self))